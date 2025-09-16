import React, { useState } from 'react'

interface DiffAnalyzeFormProps {
  onLoading: (loading: boolean) => void
}

export const DiffAnalyzeForm: React.FC<DiffAnalyzeFormProps> = ({ onLoading }) => {
  const [diffPatch, setDiffPatch] = useState('')
  const [result, setResult] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    onLoading(true)
    
    try {
      const response = await fetch('/api/analyze_diff', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          diff_patch: diffPatch,
        }),
      })
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({ error: 'Failed to analyze diff' })
    } finally {
      onLoading(false)
    }
  }

  const sampleDiff = `diff --git a/main.py b/main.py
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
     print(f"Sum: {result}")`

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="diffPatch" className="block text-sm font-medium text-gray-700">
            Git Diff Patch
          </label>
          <textarea
            id="diffPatch"
            value={diffPatch}
            onChange={(e) => setDiffPatch(e.target.value)}
            placeholder="Paste your git diff here..."
            className="input h-64"
            required
          />
        </div>
        
        <div className="flex space-x-4">
          <button type="submit" className="btn btn-primary">
            Analyze Diff
          </button>
          <button 
            type="button" 
            onClick={() => setDiffPatch(sampleDiff)}
            className="btn btn-secondary"
          >
            Use Sample Diff
          </button>
        </div>
      </form>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-medium mb-2">Analysis Result:</h3>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

