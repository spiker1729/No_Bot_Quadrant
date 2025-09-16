import React, { useState } from 'react'

interface AskPanelProps {
  onLoading: (loading: boolean) => void
  repoPath?: string
}

export const AskPanel: React.FC<AskPanelProps> = ({ onLoading, repoPath }) => {
  const [question, setQuestion] = useState('')
  const [contextIds, setContextIds] = useState('')
  const [result, setResult] = useState<any>(null)
  const [prettify, setPrettify] = useState(true)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    onLoading(true)
    
    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          context_ids: contextIds ? contextIds.split(',').map(id => id.trim()) : undefined,
          repo_path: repoPath || undefined,
        }),
      })
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({ error: 'Failed to get answer' })
    } finally {
      onLoading(false)
    }
  }

  const sampleQuestions = [
    "What functions are affected by changes to the authentication module?",
    "What tests might need to be updated?",
    "What is the overall impact of the changes?",
    "Which files depend on the modified functions?",
  ]

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-sm font-medium text-gray-700">
            Question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about the codebase..."
            className="input h-32"
            required
          />
        </div>
        
        <div>
          <label htmlFor="contextIds" className="block text-sm font-medium text-gray-700">
            Context IDs (Optional)
          </label>
          <input
            type="text"
            id="contextIds"
            value={contextIds}
            onChange={(e) => setContextIds(e.target.value)}
            placeholder="chunk1,chunk2,chunk3"
            className="input"
          />
          <p className="text-sm text-gray-500 mt-1">
            Comma-separated list of chunk IDs to provide context
          </p>
        </div>
        
        <div className="flex space-x-4">
          <button type="submit" className="btn btn-primary">
            Ask Question
          </button>
          <label className="flex items-center space-x-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={prettify}
              onChange={(e) => setPrettify(e.target.checked)}
            />
            <span>Prettify</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {sampleQuestions.map((q, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setQuestion(q)}
                className="btn btn-secondary text-xs"
              >
                {q.substring(0, 30)}...
              </button>
            ))}
          </div>
        </div>
      </form>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-medium mb-2">Answer:</h3>
          <pre className="text-sm overflow-auto whitespace-pre-wrap">
            {prettify ? JSON.stringify(result, null, 2) : JSON.stringify(result)}
          </pre>
        </div>
      )}
    </div>
  )
}

