export async function fetchTools() {
  const res = await fetch('/tools')
  return res.json()
}

export async function invokeTool(tool: string, args: any) {
  const res = await fetch('/invoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tool, args }),
  })
  return res.json()
}

export async function getVendors() {
  const res = await fetch('/vendors')
  return res.json()
}
