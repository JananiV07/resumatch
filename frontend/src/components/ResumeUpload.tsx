export function ResumeUpload({ files, onChange }: { files: File[]; onChange: (f: File[]) => void }) {
  return (
    <label className="field">
      <span>Resumes (PDF, DOCX, TXT)</span>
      <input
        type="file"
        multiple
        accept=".pdf,.docx,.txt"
        onChange={(e) => onChange(Array.from(e.target.files ?? []))}
      />
      {files.length > 0 && <small>{files.length} file(s) selected</small>}
    </label>
  )
}
