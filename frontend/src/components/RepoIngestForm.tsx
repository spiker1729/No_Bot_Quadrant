import React, { useState } from 'react'

interface RepoIngestFormProps {
  onLoading: (loading: boolean) => void
  onIngestDone?: (repoPath: string) => void
}

export const RepoIngestForm: React.FC<RepoIngestFormProps> = ({ onLoading, onIngestDone }) => {
  const [repoUrl, setRepoUrl] = useState('')
  const [githubToken, setGithubToken] = useState('')
  const [result, setResult] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    onLoading(true)
    
    // Clean the repository URL
    let cleanRepoUrl = repoUrl.trim()
    
    // Remove @ prefix if present
    if (cleanRepoUrl.startsWith('@')) {
      cleanRepoUrl = cleanRepoUrl.substring(1)
    }
    
    // Ensure it's a proper GitHub URL
    if (!cleanRepoUrl.startsWith('https://github.com/')) {
      if (cleanRepoUrl.startsWith('github.com/')) {
        cleanRepoUrl = `https://${cleanRepoUrl}`
      } else if (cleanRepoUrl.includes('/') && !cleanRepoUrl.startsWith('http')) {
        cleanRepoUrl = `https://github.com/${cleanRepoUrl}`
      }
    }
    
    try {
      const response = await fetch('/api/ingest_repo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_url: cleanRepoUrl,
          github_token: githubToken || undefined,
        }),
      })
      
      const data = await response.json()
      setResult(data)
      if (data && data.repo_path && onIngestDone) {
        onIngestDone(data.repo_path)
      }
    } catch (error) {
      setResult({ error: 'Failed to ingest repository' })
    } finally {
      onLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="repoUrl" className="block text-sm font-medium text-gray-700">
            Repository URL
          </label>
          <input
            type="text"
            id="repoUrl"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/owner/repo or django/django"
            className="input"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Supports: https://github.com/owner/repo, github.com/owner/repo, or owner/repo
          </p>
        </div>
        
        <div>
          <label htmlFor="githubToken" className="block text-sm font-medium text-gray-700">
            GitHub Token (Optional)
          </label>
          <input
            type="password"
            id="githubToken"
            value={githubToken}
            onChange={(e) => setGithubToken(e.target.value)}
            placeholder="ghp_xxxxxxxxxxxx"
            className="input"
          />
        </div>
        
        <button type="submit" className="btn btn-primary">
          Ingest Repository
        </button>
      </form>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-medium mb-2">Result:</h3>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

