export function JobDescriptionInput({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <label className="field">
      <span>Job Description</span>
      <textarea
        rows={8}
        value={value}
        placeholder="Paste the job description here…"
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  )
}
