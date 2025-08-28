import React, { useEffect, useState } from 'react'
import { getVendors } from '../lib/api'
import { VendorStatus } from '../components/VendorStatus'

export function Connections() {
  const [vendors, setVendors] = useState<any>({})
  useEffect(() => {
    getVendors().then(setVendors)
  }, [])
  return (
    <div>
      <VendorStatus vendors={vendors} />
    </div>
  )
}
