import { ScoreGauge } from './ScoreGauge'
import { tierClass, type Candidate } from '../types'

function SignalBar({ label, value, hint }: { label: string; value: number; hint: string }) {
  const pct = Math.max(0, Math.min(100, value * 100))
  return (
    <div className="signal">
      <div className="signal-head">
        <span className="signal-label">{label}</span>
        <span className="signal-val">{Math.round(pct)}%</span>
      </div>
      <div className="signal-track" role="meter" aria-valuenow={Math.round(pct)} aria-valuemin={0} aria-valuemax={100} aria-label={`${label}: ${hint}`}>
        <div className="signal-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function Chips({ items, kind }: { items: string[]; kind: 'matched' | 'missing' }) {
  if (items.length === 0) return null
  return (
    <div className={`chips chips-${kind}`}>
      <span className="chips-title">{kind === 'matched' ? 'Matched' : 'Missing'}</span>
      <div className="chips-row">
        {items.map((s) => (
          <span key={s} className={`chip chip-${kind}`}>{s}</span>
        ))}
      </div>
    </div>
  )
}

export function CandidateCard({ candidate, rank }: { candidate: Candidate; rank: number }) {
  const c = candidate
  const cls = tierClass(c.tier)
  const expPct = Math.min(c.experience_years / 20, 1)
  return (
    <article className={`card card-${cls}`} style={{ animationDelay: `${rank * 70}ms` }}>
      <div className="card-top">
        <span className="rank">#{rank}</span>
        <ScoreGauge score={c.score} tier={c.tier} />
        <div className="card-id">
          <h3 className="card-name" title={c.filename}>{c.filename}</h3>
          <span className={`badge badge-${cls}`}>{c.tier}</span>
        </div>
      </div>

      <p className="explanation">{c.explanation}</p>

      <div className="signals">
        <SignalBar label="Semantic relevance" value={c.semantic_similarity} hint="how closely the resume reads to the job description" />
        <SignalBar label="Skill match" value={c.skill_overlap} hint="share of required skills present" />
        <SignalBar label="Experience" value={expPct} hint={`${c.experience_years} years (capped at 20)`} />
      </div>

      <div className="card-skills">
        <Chips items={c.matched_skills} kind="matched" />
        <Chips items={c.missing_skills} kind="missing" />
      </div>
    </article>
  )
}
