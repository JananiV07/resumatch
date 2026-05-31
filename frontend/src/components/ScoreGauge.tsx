import { tierClass } from '../types'

const SIZE = 92
const STROKE = 9
const R = (SIZE - STROKE) / 2
const C = 2 * Math.PI * R

export function ScoreGauge({ score, tier }: { score: number; tier: string }) {
  const pct = Math.max(0, Math.min(100, score))
  const offset = C - (pct / 100) * C
  const cls = tierClass(tier)
  return (
    <svg
      className={`gauge gauge-${cls}`}
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      role="img"
      aria-label={`Match score ${Math.round(score)} out of 100, ${tier}`}
    >
      <circle className="gauge-track" cx={SIZE / 2} cy={SIZE / 2} r={R} strokeWidth={STROKE} fill="none" />
      <circle
        className="gauge-value"
        cx={SIZE / 2}
        cy={SIZE / 2}
        r={R}
        strokeWidth={STROKE}
        fill="none"
        strokeLinecap="round"
        strokeDasharray={C}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${SIZE / 2} ${SIZE / 2})`}
      />
      <text className="gauge-num" x="50%" y="50%" dominantBaseline="central" textAnchor="middle">
        {Math.round(score)}
      </text>
    </svg>
  )
}
