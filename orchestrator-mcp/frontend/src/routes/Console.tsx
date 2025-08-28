import React, { useEffect, useState } from 'react'
import { fetchTools, invokeTool } from '../lib/api'
import { ToolForm } from '../components/ToolForm'
import { TraceView } from '../components/TraceView'

export function Console() {
  const [tools, setTools] = useState<Record<string, any>>({})
  const [trace, setTrace] = useState<any[]>([])

  useEffect(() => {
    fetchTools().then(setTools)
  }, [])

  const handleInvoke = async (tool: string, args: any) => {
    const res = await invokeTool(tool, args)
    setTrace((t) => [...t, { tool, args, res }])
  }

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <ToolForm tools={tools} onInvoke={handleInvoke} />
      <TraceView trace={trace} />
    </div>
  )
}
