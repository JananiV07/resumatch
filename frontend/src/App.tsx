import { useState } from 'react'
import { ResultsTable } from './components/ResultsTable'
import { scoreResumes } from './api'
import type { ScoreResponse } from './types'
import './App.css'

export default function App() {
  const [jd, setJd] = useState('')
  const [files, setFiles] = useState<File[]>([])
  const [result, setResult] = useState<ScoreResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleRank() {
    setError(null); setLoading(true); setResult(null)
    try {
      setResult(await scoreResumes(jd, files))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const canRank = jd.trim().length > 0 && files.length > 0 && !loading

  return (
    <div className="page">
      <div className="aurora" aria-hidden="true" />
      <main className="app">
        <header className="hero">
          <span className="kicker">AI RESUME SCREENING</span>
          <h1>Resu<span className="grad">Match</span></h1>
          <p className="tagline">
            Rank candidates against any job description with BERT semantic matching,
            skill analysis, and an explainable scoring model.
          </p>
        </header>

        <section className="panel glass">
          <label className="field">
            <span className="field-label">Job description</span>
            <textarea
              rows={7}
              value={jd}
              placeholder="Paste the role's responsibilities, required skills, and experience…"
              onChange={(e) => setJd(e.target.value)}
            />
          </label>

          <label className={`dropzone ${files.length ? 'has-files' : ''}`}>
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.txt"
              onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
            />
            <svg className="up-icon" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M12 16V4M12 4l-4 4M12 4l4 4" />
              <path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
            </svg>
            <span className="dz-text">
              {files.length ? `${files.length} resume${files.length > 1 ? 's' : ''} ready` : 'Drop resumes or click to upload'}
            </span>
            <span className="dz-sub">PDF, DOCX, or TXT · multiple files</span>
          </label>

          <button className="rank-btn" onClick={handleRank} disabled={!canRank}>
            {loading ? (
              <><span className="spinner" aria-hidden="true" /> Ranking…</>
            ) : (
              'Rank candidates'
            )}
          </button>
          {error && <p className="error" role="alert">{error}</p>}
        </section>

        {result?.warnings?.length ? (
          <ul className="warnings" role="status">
            {result.warnings.map((w) => <li key={w}>{w}</li>)}
          </ul>
        ) : null}

        {result && (
          <div className="results-wrap">
            <h2 className="results-h">
              {result.candidates.length
                ? `${result.candidates.length} candidate${result.candidates.length > 1 ? 's' : ''} ranked`
                : 'No candidates ranked'}
            </h2>
            <ResultsTable candidates={result.candidates} />
          </div>
        )}
      </main>
    </div>
  )
}
