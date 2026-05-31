import type { ScoreResponse } from './types'

const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export async function scoreResumes(jdText: string, files: File[]): Promise<ScoreResponse> {
  const form = new FormData()
  form.append('jd_text', jdText)
  for (const f of files) form.append('resumes', f)

  const resp = await fetch(`${BASE}/score`, { method: 'POST', body: form })
  if (!resp.ok) {
    const detail = await resp.json().catch(() => ({}))
    throw new Error(detail.detail ?? `Request failed: ${resp.status}`)
  }
  return resp.json()
}
