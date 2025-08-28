import React from 'react'

export function VendorStatus({ vendors }: { vendors: any }) {
  return (
    <div>
      {Object.entries(vendors).map(([name, info]: any) => (
        <div key={name}>
          <strong>{name}</strong>: {info.connected ? 'connected' : 'down'}
        </div>
      ))}
    </div>
  )
}
