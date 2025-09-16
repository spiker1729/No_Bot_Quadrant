import React, { useState } from 'react'
import { RepoIngestForm } from './components/RepoIngestForm'
import { DiffAnalyzeForm } from './components/DiffAnalyzeForm'
import { AskPanel } from './components/AskPanel'
import { GraphView } from './components/GraphView'
import { FullGraph } from './components/FullGraph'
import { LoadingSpinner } from './components/LoadingSpinner'

function App() {
  const [activeTab, setActiveTab] = useState('ingest')
  const [isLoading, setIsLoading] = useState(false)
  const [repoPath, setRepoPath] = useState<string | null>(null)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900 text-center">
              Impact Analysis Tool
            </h1>
          </div>
          <div className="flex justify-center space-x-4">
              <button
                onClick={() => setActiveTab('ingest')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'ingest'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Ingest Repo
              </button>
              <button
                onClick={() => setActiveTab('analyze')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'analyze'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Analyze Diff
              </button>
              <button
                onClick={() => setActiveTab('ask')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'ask'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Ask Questions
              </button>
              <button
                onClick={() => setActiveTab('graph')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'graph'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                View Graph
              </button>
              <button
                onClick={() => setActiveTab('full')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'full'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Full Graph
              </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading && <LoadingSpinner />}
        
        <div className="space-y-6">
          {activeTab === 'ingest' && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Repository Ingestion</h2>
              <RepoIngestForm
                onLoading={setIsLoading}
                onIngestDone={(path) => {
                  setRepoPath(path)
                  setActiveTab('graph')
                }}
              />
            </div>
          )}

          {activeTab === 'analyze' && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Diff Analysis</h2>
              <DiffAnalyzeForm onLoading={setIsLoading} />
            </div>
          )}

          {activeTab === 'ask' && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Ask Questions</h2>
              <AskPanel onLoading={setIsLoading} repoPath={repoPath || undefined} />
            </div>
          )}

          {activeTab === 'graph' && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Code Graph Visualization</h2>
              <GraphView onLoading={setIsLoading} repoPath={repoPath || undefined} />
            </div>
          )}

          {activeTab === 'full' && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Full Repository Graph</h2>
              <FullGraph onLoading={setIsLoading} repoPath={repoPath || undefined} />
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App

