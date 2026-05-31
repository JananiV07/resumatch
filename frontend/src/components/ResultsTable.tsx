import { CandidateCard } from './CandidateCard'
import type { Candidate } from '../types'

export function ResultsTable({ candidates }: { candidates: Candidate[] }) {
  if (candidates.length === 0) {
    return <p className="empty">No candidates to display.</p>
  }
  return (
    <section className="results" aria-label="Ranked candidates">
      {candidates.map((c, i) => (
        <CandidateCard key={c.filename} candidate={c} rank={i + 1} />
      ))}
    </section>
  )
}
