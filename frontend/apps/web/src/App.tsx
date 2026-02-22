import { useEffect, useState } from 'react'
import './App.css'
import { renderToPipeableStream } from 'react-dom/server'

type Json = Record<string, unknown>

async function fetchJson(path: string) {
  const res = await fetch(path)
  const data = (await res.json()) as {status?: string}
  return { ok: res.ok, status: res.status, data }
}

export default function App() {
  const [gateway, setGateway] = useState<Json | null>(null)
  const [identity, setIdentity] = useState<Json | null>(null)
  const [finance, setFinance] = useState<Json | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ;(async () => {
      try {
        const g = await fetchJson('/health')
        setGateway(g.data as Json)

        const i = await fetchJson('/api/identity/health')
        setIdentity(i.data)

        const f = await fetchJson('/api/finance/health')
        setFinance(f.data)
      } catch (e) {
        setError(String(e))
      }
    })()
  }, [])

  return (
    <div style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <h1>ERPLife — Dev Status</h1>

      {error && (
        <div style={{ marginTop: 16 }}>
          <h2>Error</h2>
          <pre>{error}</pre>
        </div>
      )}

      <div style={{ marginTop: 16 }}>
        <h2>Gateway</h2>
        <pre>{JSON.stringify(gateway, null, 2)}</pre>
      </div>

      <div style={{ marginTop: 16 }}>
        <h2>Identity</h2>
        <pre>{JSON.stringify(identity, null, 2)}</pre>
      </div>

      <div style={{ marginTop: 16 }}>
        <h2>Finance</h2>
        <pre>{JSON.stringify(finance, null, 2)}</pre>
      </div>
    </div>
  )
}