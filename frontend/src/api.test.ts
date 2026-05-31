import { describe, it, expect, vi, afterEach } from 'vitest'
import { scoreResumes } from './api'

afterEach(() => vi.restoreAllMocks())

describe('scoreResumes', () => {
  it('posts FormData and returns parsed response', async () => {
    const mockResp = { candidates: [], warnings: [] }
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => mockResp })
    vi.stubGlobal('fetch', fetchMock)

    const files = [new File(['hi'], 'a.txt', { type: 'text/plain' })]
    const result = await scoreResumes('python role', files)

    expect(result).toEqual(mockResp)
    expect(fetchMock).toHaveBeenCalledOnce()
    const [url, opts] = fetchMock.mock.calls[0]
    expect(url).toContain('/score')
    expect(opts.method).toBe('POST')
    expect(opts.body).toBeInstanceOf(FormData)
  })

  it('throws on non-ok response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false, status: 400, json: async () => ({ detail: 'bad' }),
    }))
    await expect(scoreResumes('', [])).rejects.toThrow()
  })
})
