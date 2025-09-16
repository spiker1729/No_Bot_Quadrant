#!/bin/bash

# Example script to generate a git diff for testing
# This creates a sample diff that can be used with the analyze_diff endpoint

echo "🔍 Generating example git diff..."

# Create a temporary directory for the example
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Initialize git repo
git init
git config user.name "Demo User"
git config user.email "demo@example.com"

# Create initial files
mkdir -p src/utils tests

cat > src/main.py << 'EOF'
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

def calculate_product(a, b):
    """Calculate the product of two numbers."""
    return a * b

def main():
    """Main function that uses other functions."""
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
    
    product = calculate_product(4, 6)
    print(f"Product: {product}")

if __name__ == "__main__":
    main()
EOF

cat > src/utils/helper.py << 'EOF'
def format_number(num):
    """Format a number with commas."""
    return f"{num:,}"

def validate_input(value):
    """Validate that input is a number."""
    try:
        float(value)
        return True
    except ValueError:
        return False
EOF

cat > tests/test_main.py << 'EOF'
import unittest
from src.main import calculate_sum, calculate_product

class TestMain(unittest.TestCase):
    def test_calculate_sum(self):
        self.assertEqual(calculate_sum(2, 3), 5)
    
    def test_calculate_product(self):
        self.assertEqual(calculate_product(2, 3), 6)

if __name__ == "__main__":
    unittest.main()
EOF

# Commit initial version
git add .
git commit -m "Initial commit"

# Make changes
cat > src/main.py << 'EOF'
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b + 1  # Add 1 to the result

def calculate_product(a, b):
    """Calculate the product of two numbers."""
    return a * b

def main():
    """Main function that uses other functions."""
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
    
    product = calculate_product(4, 6)
    print(f"Product: {product}")

if __name__ == "__main__":
    main()
EOF

# Generate the diff
echo "📝 Generated diff:"
echo "=================="
git diff HEAD

echo ""
echo "📋 Copy the diff above and use it with:"
echo "curl -X POST 'http://localhost:8000/analyze_diff' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"diff_patch\": \"<paste diff here>\"}'"

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"
