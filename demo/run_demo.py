#!/usr/bin/env python3
"""
Demo script for the Impact Analysis Tool.
This script demonstrates the complete workflow of ingesting a repository,
analyzing a diff, and getting impact analysis results.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the backend src to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "src"))

import httpx
from impact_analysis.config import settings


class ImpactAnalysisDemo:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def check_health(self):
        """Check if the backend is running."""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Backend is running")
                return True
            else:
                print(f"❌ Backend returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return False
    
    async def ingest_sample_repo(self):
        """Ingest the sample repository."""
        print("\n📥 Ingesting sample repository...")
        
        # Get the sample repo path
        sample_repo_path = Path(__file__).parent / "sample_repo"
        
        # Create a simple file structure for demo
        sample_repo_path.mkdir(exist_ok=True)
        
        # Create directories first
        (sample_repo_path / "utils").mkdir(exist_ok=True)
        (sample_repo_path / "tests").mkdir(exist_ok=True)
        
        # Create sample Python files
        (sample_repo_path / "main.py").write_text("""
def calculate_sum(a, b):
    '''Calculate the sum of two numbers.'''
    return a + b

def calculate_product(a, b):
    '''Calculate the product of two numbers.'''
    return a * b

def main():
    '''Main function that uses other functions.'''
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
    
    product = calculate_product(4, 6)
    print(f"Product: {product}")

if __name__ == "__main__":
    main()
""")
        
        (sample_repo_path / "utils" / "helper.py").write_text("""
def format_number(num):
    '''Format a number with commas.'''
    return f"{num:,}"

def validate_input(value):
    '''Validate that input is a number.'''
    try:
        float(value)
        return True
    except ValueError:
        return False
""")
        
        (sample_repo_path / "tests" / "test_main.py").write_text("""
import unittest
from main import calculate_sum, calculate_product

class TestMain(unittest.TestCase):
    def test_calculate_sum(self):
        self.assertEqual(calculate_sum(2, 3), 5)
    
    def test_calculate_product(self):
        self.assertEqual(calculate_product(2, 3), 6)

if __name__ == "__main__":
    unittest.main()
""")
        
        (sample_repo_path / "tests").mkdir(exist_ok=True)
        
        # For demo purposes, we'll simulate the ingestion
        print("✅ Sample repository structure created")
        return str(sample_repo_path)
    
    async def analyze_sample_diff(self):
        """Analyze a sample diff."""
        print("\n🔍 Analyzing sample diff...")
        
        # Sample diff that changes the calculate_sum function
        sample_diff = """diff --git a/main.py b/main.py
index 1234567..abcdefg 100644
--- a/main.py
+++ b/main.py
@@ -1,6 +1,6 @@
 def calculate_sum(a, b):
     '''Calculate the sum of two numbers.'''
-    return a + b
+    return a + b + 1  # Add 1 to the result
 
 def calculate_product(a, b):
     '''Calculate the product of two numbers.'''
@@ -8,6 +8,7 @@ def calculate_product(a, b):
     return a * b
 
 def main():
+    # Updated main function
     '''Main function that uses other functions.'''
     result = calculate_sum(5, 3)
     print(f"Sum: {result}")
"""
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/analyze_diff",
                json={"diff_patch": sample_diff}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Diff analysis completed")
                return result
            else:
                print(f"❌ Diff analysis failed: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ Error during diff analysis: {e}")
            return None
    
    async def ask_question(self, question: str):
        """Ask a question about the codebase."""
        print(f"\n❓ Asking: {question}")
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/ask",
                json={"question": question}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Question answered")
                return result
            else:
                print(f"❌ Question failed: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ Error asking question: {e}")
            return None
    
    def print_results(self, results, title: str):
        """Print formatted results."""
        print(f"\n📊 {title}")
        print("=" * 50)
        print(json.dumps(results, indent=2, default=str))
        print("=" * 50)


async def main():
    """Run the complete demo."""
    print("🚀 Impact Analysis Tool Demo")
    print("=" * 50)
    
    async with ImpactAnalysisDemo() as demo:
        # Check if backend is running
        if not await demo.check_health():
            print("\n❌ Please start the backend first:")
            print("   docker-compose up backend")
            return
        
        # Ingest sample repository
        repo_path = await demo.ingest_sample_repo()
        print(f"📁 Sample repository created at: {repo_path}")
        
        # Analyze sample diff
        diff_results = await demo.analyze_sample_diff()
        if diff_results:
            demo.print_results(diff_results, "Diff Analysis Results")
        
        # Ask some questions
        questions = [
            "What functions are affected by changes to calculate_sum?",
            "What tests might need to be updated?",
            "What is the overall impact of the changes?"
        ]
        
        for question in questions:
            answer = await demo.ask_question(question)
            if answer:
                demo.print_results(answer, f"Answer: {question}")
        
        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("1. Start the full application: docker-compose up")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Try ingesting your own repository")


if __name__ == "__main__":
    asyncio.run(main())
