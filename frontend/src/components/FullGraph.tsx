import React, { useEffect, useRef, useState } from 'react'
import cytoscape from 'cytoscape'
// @ts-ignore
import fcose from 'cytoscape-fcose'
// @ts-ignore  
import cola from 'cytoscape-cola'

// Register layout extensions
cytoscape.use(fcose)
cytoscape.use(cola)

interface FullGraphProps {
  repoPath?: string
  onLoading: (loading: boolean) => void
}

export const FullGraph: React.FC<FullGraphProps> = ({ repoPath, onLoading }) => {
  const [data, setData] = useState<{ nodes: any[]; edges: any[]; root?: string } | null>(null)
  const [error, setError] = useState<string | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [currentLayout, setCurrentLayout] = useState('fcose')
  const cyRef = useRef<any>(null)

  useEffect(() => {
    const load = async () => {
      if (!repoPath) return
      onLoading(true)
      setError(null)
      try {
        const res = await fetch('/api/graph/repo_tree', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ repo_path: repoPath })
        })
        const json = await res.json()
        setData(json)
      } catch (e) {
        setError('Failed to load full graph')
      } finally {
        onLoading(false)
      }
    }
    load()
  }, [repoPath])

  useEffect(() => {
    if (!containerRef.current || !data) return
    const elements: any[] = []
    ;(data.nodes || []).forEach((n: any) => {
      if (typeof n === 'string') {
        elements.push({ data: { id: n, label: n } })
      } else {
        elements.push({ data: { id: n.id, label: n.label || n.id } })
      }
    })
    ;(data.edges || []).forEach((e: any, idx: number) => {
      elements.push({ data: { id: e.id || `e${idx}`, source: e.source, target: e.target, label: e.label } })
    })
    
    const getLayoutConfig = (layoutName: string) => {
      switch (layoutName) {
        case 'fcose':
          return {
            name: 'fcose',
            randomize: false,
            animate: true,
            animationDuration: 1500,
            fit: true,
            padding: 40,
            nodeDimensionsIncludeLabels: true,
            uniformNodeDimensions: false,
            packComponents: true,
            stepSize: 25,
            nodeRepulsion: () => 8000,
            idealEdgeLength: () => 120,
            edgeElasticity: () => 0.3,
            nestingFactor: 0.2,
            gravity: 0.15,
            numIter: 3000,
            tile: true
          } as any
        case 'cola':
          return {
            name: 'cola',
            animate: true,
            refresh: 1,
            maxSimulationTime: 6000,
            fit: true,
            padding: 40,
            randomize: false,
            avoidOverlap: true,
            handleDisconnected: true,
            nodeSpacing: () => 100
          } as any
        case 'breadthfirst':
          return {
            name: 'breadthfirst',
            directed: true,
            padding: 40,
            spacingFactor: 1.5,
            animate: true,
            roots: data.root ? [data.root] : undefined
          } as any
        default:
          return { name: 'cose', fit: true, padding: 40, animate: true } as any
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
            'font-size': '7px', 
            'background-color': '#059669', 
            'color': '#000000', 
            'text-wrap': 'wrap', 
            'text-max-width': '120px', 
            'width': '16px', 
            'height': '16px',
            'text-valign': 'center',
            'text-halign': 'center',
            'border-width': '1px',
            'border-color': '#047857'
          } 
        },
        { 
          selector: 'edge', 
          style: { 
            'curve-style': 'straight', 
            'width': '1px', 
            'line-color': '#cbd5e1', 
            'target-arrow-shape': 'triangle', 
            'target-arrow-color': '#cbd5e1',
            'opacity': 0.6
          } 
        },
        { 
          selector: ':selected', 
          style: { 
            'background-color': '#f59e0b', 
            'line-color': '#f59e0b', 
            'target-arrow-color': '#f59e0b',
            'border-color': '#d97706'
          } 
        },
        {
          selector: 'node:hover',
          style: {
            'background-color': '#10b981',
            'border-color': '#059669'
          }
        }
      ],
      layout: getLayoutConfig(currentLayout)
    })
    
    cyRef.current = cy
    cy.minZoom(0.1); cy.maxZoom(2.5); cy.center(); cy.zoom(1)
    return () => { cy.destroy() }
  }, [data, currentLayout])

  const changeLayout = (layoutName: string) => {
    setCurrentLayout(layoutName)
    if (cyRef.current) {
      const config = layoutName === 'fcose' ? { name: 'fcose', animate: true, fit: true, padding: 40 } :
                     layoutName === 'cola' ? { name: 'cola', animate: true, fit: true, padding: 40 } :
                     layoutName === 'breadthfirst' ? { name: 'breadthfirst', animate: true, fit: true, padding: 40 } :
                     { name: 'cose', animate: true, fit: true, padding: 40 }
      cyRef.current.layout(config as any).run()
    }
  }

  if (!repoPath) {
    return <div className="text-sm text-gray-500">Ingest a repository first.</div>
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">{error}</div>
      )}
      <div className="p-4 bg-green-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-medium">Full Repository Graph</h3>
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
                className={`btn text-xs ${currentLayout === 'breadthfirst' ? 'btn-primary' : 'btn-secondary'}`} 
                onClick={() => changeLayout('breadthfirst')}
              >
                Tree
              </button>
            </div>
            <button type="button" className="btn btn-secondary text-xs" onClick={() => { if (cyRef.current) cyRef.current.fit(undefined, 40) }}>Fit</button>
          </div>
        </div>
        <div ref={containerRef} className="w-full h-[600px] border border-gray-300 rounded-lg bg-white" />
      </div>
    </div>
  )
}

export default FullGraph


