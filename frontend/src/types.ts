export interface Candidate {
  filename: string
  score: number
  tier: string
  explanation: string
  matched_skills: string[]
  missing_skills: string[]
  experience_years: number
  semantic_similarity: number
  skill_overlap: number
}

export interface ScoreResponse {
  candidates: Candidate[]
  warnings: string[]
}

export function tierClass(tier: string): string {
  const t = tier.toLowerCase()
  if (t.startsWith('strong')) return 'strong'
  if (t.startsWith('moderate')) return 'moderate'
  if (t.startsWith('weak')) return 'weak'
  return 'poor'
}
