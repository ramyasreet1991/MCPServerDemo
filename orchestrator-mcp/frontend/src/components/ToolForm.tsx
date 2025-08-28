import React, { useState } from 'react'

interface Props {
  tools: Record<string, any>
  onInvoke: (tool: string, args: any) => void
}

export function ToolForm({ tools, onInvoke }: Props) {
  const [tool, setTool] = useState('')
  const [arg, setArg] = useState('')
  return (
    <div>
      <select value={tool} onChange={(e) => setTool(e.target.value)}>
        <option value="">Select tool</option>
        {Object.keys(tools).map((t) => (
          <option key={t} value={t}>{t}</option>
        ))}
      </select>
      <input
        value={arg}
        onChange={(e) => setArg(e.target.value)}
        placeholder="args as JSON"
      />
      <button onClick={() => onInvoke(tool, JSON.parse(arg || '{}'))}>Invoke</button>
    </div>
  )
}
