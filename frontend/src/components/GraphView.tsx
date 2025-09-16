import React, { useState, useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'
// @ts-ignore
import fcose from 'cytoscape-fcose'
// @ts-ignore  
import cola from 'cytoscape-cola'

// Register layout extensions
cytoscape.use(fcose)
cytoscape.use(cola)

interface GraphViewProps {
  onLoading: (loading: boolean) => void
  repoPath?: string
}

export const GraphView: React.FC<GraphViewProps> = ({ onLoading, repoPath }) => {
  const [nodeId, setNodeId] = useState('')
  const [graphData, setGraphData] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [availableNodes, setAvailableNodes] = useState<string[]>([])
  const [currentLayout, setCurrentLayout] = useState('fcose')
  const cyRef = useRef<any>(null)

  // Render cytoscape when graphData changes
  useEffect(() => {
    if (!containerRef.current || !graphData) return
    const elements: any[] = []
    ;(graphData.nodes || []).forEach((n: any) => {
      if (typeof n === 'string') {
        elements.push({ data: { id: n, label: n } })
      } else {
        elements.push({ data: { id: n.id, label: n.label || n.id } })
      }
    })
    ;(graphData.edges || []).forEach((e: any, idx: number) => {
      elements.push({ data: { id: e.id || `e${idx}`, source: e.source, target: e.target, label: e.label } })
    })
    
    const getLayoutConfig = (layoutName: string) => {
      switch (layoutName) {
        case 'fcose':
          return {
            name: 'fcose',
            randomize: false,
            animate: true,
            animationDuration: 1000,
            fit: true,
            padding: 50,
            nodeDimensionsIncludeLabels: true,
            uniformNodeDimensions: false,
            packComponents: true,
            stepSize: 30,
            nodeRepulsion: () => 4500,
            idealEdgeLength: () => 100,
            edgeElasticity: () => 0.45,
            nestingFactor: 0.1,
            gravity: 0.25,
            numIter: 2500,
            tile: true,
            tilingPaddingVertical: 10,
            tilingPaddingHorizontal: 10
          } as any
        case 'cola':
          return {
            name: 'cola',
            animate: true,
            refresh: 1,
            maxSimulationTime: 4000,
            ungrabifyWhileSimulating: false,
            fit: true,
            padding: 30,
            nodeDimensionsIncludeLabels: false,
            randomize: false,
            avoidOverlap: true,
            handleDisconnected: true,
            convergenceThreshold: 0.01,
            nodeSpacing: () => 80,
            flow: undefined,
            alignment: undefined,
            gapInequalities: undefined
          } as any
        case 'circle':
          return {
            name: 'circle',
            fit: true,
            padding: 30,
            boundingBox: undefined,
            avoidOverlap: true,
            nodeDimensionsIncludeLabels: false,
            spacingFactor: 1.75,
            radius: undefined,
            startAngle: 3 / 2 * Math.PI,
            sweep: undefined,
            clockwise: true,
            sort: undefined,
            animate: true,
            animationDuration: 500
          }
        case 'cose':
          return {
            name: 'cose',
            animate: true,
            refresh: 20,
            fit: true,
            padding: 30,
            randomize: false,
            componentSpacing: 100,
            nodeRepulsion: () => 400000,
            nodeOverlap: 20,
            idealEdgeLength: () => 80,
            edgeElasticity: () => 100,
            nestingFactor: 5,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
          } as any
        default:
          return { name: 'grid', fit: true, padding: 30 }
      }
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        { 
          selector: 'node', 
          style: { 
            'label': 'data(label)', 
            'font-size': '8px', 
            'background-color': '#2563eb', 
            'color': '#000000', 
            'text-wrap': 'wrap', 
            'text-max-width': '140px', 
            'width': '20px', 
            'height': '20px',
            'text-valign': 'center',
            'text-halign': 'center',
            'border-width': '2px',
            'border-color': '#1e40af',
            'border-opacity': 0.8
          } 
        },
        { 
          selector: 'edge', 
          style: { 
            'curve-style': 'straight', 
            'target-arrow-shape': 'triangle', 
            'arrow-scale': 1, 
            'width': '2px', 
            'line-color': '#94a3b8', 
            'target-arrow-color': '#94a3b8',
            'opacity': 0.7
          } 
        },
        { 
          selector: ':selected', 
          style: { 
            'background-color': '#ef4444', 
            'line-color': '#ef4444', 
            'target-arrow-color': '#ef4444',
            'border-color': '#dc2626'
          } 
        },
        {
          selector: 'node:hover',
          style: {
            'background-color': '#3b82f6',
            'border-color': '#2563eb'
          }
        }
      ],
      layout: getLayoutConfig(currentLayout)
    })
    
    cyRef.current = cy
    cy.minZoom(0.2); cy.maxZoom(2.5); cy.zoom(1); cy.center()
    const fit = () => cy.fit(undefined, 30)
    fit()
    return () => { cy.destroy() }
  }, [graphData, currentLayout])

  const changeLayout = (layoutName: string) => {
    setCurrentLayout(layoutName)
    if (cyRef.current) {
      cyRef.current.layout({ 
        name: layoutName === 'fcose' ? 'fcose' : 
               layoutName === 'cola' ? 'cola' :
               layoutName === 'circle' ? 'circle' :
               layoutName === 'cose' ? 'cose' : 'grid',
        animate: true,
        fit: true,
        padding: 30
      } as any).run()
    }
  }

  const fetchGraphData = async (id: string) => {
    if (!id) return
    
    onLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/graph/${id}`)
      const data = await response.json()
      setGraphData(data)
    } catch (err) {
      setError('Failed to fetch graph data')
    } finally {
      onLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    fetchGraphData(nodeId)
  }

  const sampleNodeIds = [
    'main.py',
    'calculate_sum',
    'calculate_product',
    'test_main.py'
  ]

  // Auto-load nodes when repoPath is provided
  useEffect(() => {
    const loadNodes = async () => {
      if (!repoPath) return
      onLoading(true)
      setError(null)
      try {
        const res = await fetch('/api/graph/list_nodes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ repo_path: repoPath })
        })
        const data = await res.json()
        const nodes: string[] = data?.nodes || []
        setAvailableNodes(nodes)
        if (nodes.length > 0) {
          setNodeId(nodes[0])
          fetchGraphData(nodes[0])
        }
      } catch (e) {
        setError('Failed to list nodes')
      } finally {
        onLoading(false)
      }
    }
    loadNodes()
  }, [repoPath])

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="nodeId" className="block text-sm font-medium text-gray-700">
            Node ID
          </label>
          <input
            type="text"
            id="nodeId"
            value={nodeId}
            onChange={(e) => setNodeId(e.target.value)}
            placeholder="Enter a node ID (file, function, or class name)"
            className="input"
            required
          />
          {availableNodes.length > 0 && (
            <p className="text-xs text-gray-500 mt-1">Loaded {availableNodes.length} nodes from repo</p>
          )}
        </div>
        
        <div className="flex space-x-4">
          <button type="submit" className="btn btn-primary">
            Load Graph
          </button>
          <div className="flex flex-wrap gap-2 max-h-40 overflow-auto">
            {(availableNodes.length > 0 ? availableNodes : sampleNodeIds).map((id, index) => (
              <button
                key={index}
                type="button"
                onClick={() => {
                  setNodeId(id)
                  fetchGraphData(id)
                }}
                className="btn btn-secondary text-xs"
              >
                {id}
              </button>
            ))}
          </div>
        </div>
      </form>
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}
      
      {graphData && (
        <div className="mt-4 space-y-4">
          <div className="p-4 bg-gray-100 rounded-lg">
            <h3 className="font-medium mb-2">Graph Data:</h3>
            <pre className="text-sm overflow-auto max-h-64">
              {JSON.stringify(graphData, null, 2)}
            </pre>
          </div>
          
          <div className="p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium">Graph Visualization</h3>
              <div className="space-x-2 flex flex-wrap">
                <div className="space-x-1">
                  <button 
                    type="button" 
                    className={`btn text-xs ${currentLayout === 'fcose' ? 'btn-primary' : 'btn-secondary'}`} 
                    onClick={() => changeLayout('fcose')}
                  >
                    Spider Web
                  </button>
                  <button 
                    type="button" 
                    className={`btn text-xs ${currentLayout === 'cola' ? 'btn-primary' : 'btn-secondary'}`} 
                    onClick={() => changeLayout('cola')}
                  >
                    Force
                  </button>
                  <button 
                    type="button" 
                    className={`btn text-xs ${currentLayout === 'circle' ? 'btn-primary' : 'btn-secondary'}`} 
                    onClick={() => changeLayout('circle')}
                  >
                    Circle
                  </button>
                  <button 
                    type="button" 
                    className={`btn text-xs ${currentLayout === 'cose' ? 'btn-primary' : 'btn-secondary'}`} 
                    onClick={() => changeLayout('cose')}
                  >
                    Organic
                  </button>
                </div>
                <button type="button" className="btn btn-secondary text-xs" onClick={() => { if (!containerRef.current || !graphData) return; /* re-layout by toggling state */ setGraphData({ ...graphData }) }}>Re-layout</button>
                <button type="button" className="btn btn-secondary text-xs" onClick={() => { if (cyRef.current) cyRef.current.fit(undefined, 30) }}>Fit</button>
              </div>
            </div>
            <div ref={containerRef} className="w-full h-96 border border-gray-300 rounded-lg bg-white" />
          </div>
        </div>
      )}
    </div>
  )
}

