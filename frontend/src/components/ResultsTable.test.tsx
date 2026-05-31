import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { ResultsTable } from './ResultsTable'
import type { Candidate } from '../types'

const candidates: Candidate[] = [
  { filename: 'alice.pdf', score: 88.0, tier: 'Strong match',
    explanation: 'Strong match (88/100). Resume content is highly relevant to the role.',
    matched_skills: ['python', 'docker'], missing_skills: ['aws'],
    experience_years: 6, semantic_similarity: 0.7, skill_overlap: 0.66 },
  { filename: 'bob.pdf', score: 41.0, tier: 'Weak match',
    explanation: 'Weak match (41/100). Resume content is somewhat relevant to the role.',
    matched_skills: ['python'], missing_skills: ['docker', 'aws'],
    experience_years: 2, semantic_similarity: 0.4, skill_overlap: 0.33 },
]

describe('ResultsTable', () => {
  it('renders a card per candidate with score, tier and explanation', () => {
    render(<ResultsTable candidates={candidates} />)
    expect(screen.getByText('alice.pdf')).toBeInTheDocument()
    expect(screen.getByText('bob.pdf')).toBeInTheDocument()
    // gauge score numbers
    expect(screen.getByText('88')).toBeInTheDocument()
    expect(screen.getByText('41')).toBeInTheDocument()
    // tier badges
    expect(screen.getByText('Strong match')).toBeInTheDocument()
    expect(screen.getByText('Weak match')).toBeInTheDocument()
    // explanation text rendered
    expect(screen.getByText(/highly relevant to the role/i)).toBeInTheDocument()
    // signal bar labels present
    expect(screen.getAllByText('Semantic relevance').length).toBe(2)
    expect(screen.getAllByText('Skill match').length).toBe(2)
    // matched + missing skills both render 'docker' somewhere
    expect(screen.getAllByText('docker').length).toBe(2)
  })

  it('shows empty state when no candidates', () => {
    render(<ResultsTable candidates={[]} />)
    expect(screen.getByText(/no candidates/i)).toBeInTheDocument()
  })
})
