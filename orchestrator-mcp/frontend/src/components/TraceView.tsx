import React from 'react'

export function TraceView({ trace }: { trace: any[] }) {
  return (
    <ul>
      {trace.map((t, i) => (
        <li key={i}>
          <pre>{JSON.stringify(t, null, 2)}</pre>
        </li>
      ))}
    </ul>
  )
}
