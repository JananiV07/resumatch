import { chromium } from 'playwright'

const JD = `Senior Python Engineer

We are hiring a senior backend engineer with strong Python skills.
Must have experience building REST APIs, working with Docker and AWS,
and at least 5 years of professional experience. FastAPI a plus.`

const files = [
  'S:/Projects/HireSense/samples/alice_senior.txt',
  'S:/Projects/HireSense/samples/bob_mid.txt',
  'S:/Projects/HireSense/samples/carol_designer.txt',
]

const browser = await chromium.launch({ headless: true })
const page = await browser.newPage({ viewport: { width: 1120, height: 900 }, deviceScaleFactor: 2 })
page.on('console', (m) => console.log('PAGE:', m.type(), m.text()))
page.on('pageerror', (e) => console.log('PAGEERROR:', e.message))

await page.goto('http://localhost:5173/', { waitUntil: 'networkidle' })
await page.fill('textarea', JD)
await page.setInputFiles('input[type=file]', files)
await page.click('button.rank-btn')
await page.waitForSelector('.card', { timeout: 90000 })
await page.waitForTimeout(1200) // let gauges/bars animate
await page.screenshot({ path: 'S:/Projects/HireSense/resumatch.png', fullPage: true })
const count = await page.locator('.card').count()
console.log('CARDS:', count)
await browser.close()
console.log('SCREENSHOT_DONE')
