# Upwork Job Hunting Agent — Instructions

Run this from any machine in under a minute. It hunts Upwork jobs, scores them,
and generates AI-written proposals and wireframes. Opens a clean HTML report in your browser.

---

## Quick start

```bash
# 1. Clone / copy the folder anywhere on your machine

# 2. Install dependencies (one time only)
pip install -r requirements.txt

# 3. Set your Gemini API key
cp .env.example .env
# then open .env and paste your key from https://aistudio.google.com/app/apikey

# 4. Activate feeds (open feeds.py, uncomment the URLs you want)

# 5. Run it
python3 upwork.py instant    # jobs under 2 hrs  — posted in last 12 hrs
python3 upwork.py short      # jobs under 24 hrs  — posted in last 24 hrs
python3 upwork.py sprint     # jobs 1–7 days      — no recency filter
python3 upwork.py project    # long-term jobs     — no recency filter
```

The report opens automatically in your browser. Files are saved as `report_[mode]_[timestamp].html`.

---

## Modes explained

| Mode | Job length | Recency filter | AI artifacts |
|------|-----------|----------------|--------------|
| `instant` | Under 2 hrs | Posted ≤ 12 hrs | Score matrix + UI wireframe |
| `short` | Under 24 hrs | Posted ≤ 24 hrs | Score matrix + UI wireframe |
| `sprint` | 1–7 days | None | Score matrix + proposal draft |
| `project` | 7+ days | None | Score matrix + proposal + wireframe |

---

## How scoring works

Each job gets a score out of 100:

- **85%** — implied hourly rate (budget ÷ estimated hours). Capped at $150/hr = full marks.
- **15%** — client score (rating + payment history). Normalised to /5.

Jobs are sorted highest score first in the report.

---

## Setting up your RSS feeds

Upwork RSS feeds are the data source for V1. Here's how to get your own:

### Option A — Use the pre-built URLs in feeds.py
Open `feeds.py` and uncomment any feeds that match what you're hunting. You can have multiple active at once — results are merged and deduplicated automatically.

### Option B — Generate custom URLs with ChatGPT
Paste this prompt into ChatGPT to generate 20 fresh RSS URLs tailored to your skills:

```
I need 20 Upwork RSS feed URLs for saved searches across these skill areas:
Python development, AI/ML engineering, chatbot development, LangChain / LLM integration,
data analytics, automation scripting, web scraping, API integration,
dashboard building (Streamlit / Gradio), and general AI consulting.

For each one, give me the Upwork saved search URL in RSS format
(https://www.upwork.com/ab/feed/jobs/rss?...) with realistic query parameters.
Group them by skill area and label each one clearly.
I want to paste these directly into a Python config file as commented-out strings.
```

Then paste the URLs into `feeds.py` in the same commented format as the existing ones.

### Option C — Save a search directly from Upwork
1. Go to Upwork and search for jobs (e.g. "Python AI chatbot")
2. Click **Save Search** (top right of results)
3. In your saved searches, find the RSS icon and copy the URL
4. Paste it into `feeds.py`

---

## Project structure

```
upwork-agent/
├── upwork.py          # main script — run this
├── feeds.py           # your RSS URLs — edit this
├── .env               # your Gemini API key — never commit this
├── .env.example       # template for the above
├── requirements.txt   # pip dependencies
├── instructions.md    # this file
└── report_*.html      # generated reports (gitignored)
```

---

## Roadmap

- **V1 (now)** — RSS feeds + Gemini AI artifacts
- **V2** — Browser automation layer for richer job data (budget confidence, payment verified flag, client spend history). Drop-in replacement for the fetch layer — everything else stays the same.

---

## Troubleshooting

**No jobs found** — check that at least one feed is uncommented in `feeds.py`. RSS feeds go stale; if a URL 404s, get a fresh one using Option B or C above.

**Gemini errors** — make sure your `.env` file exists with a valid `GEMINI_API_KEY`. Get a free key at https://aistudio.google.com/app/apikey

**Report doesn't open automatically** — just open the `report_*.html` file manually in any browser.

**Weird job scores** — budget and hour estimates are parsed from the job description text. Upwork doesn't always include them in RSS, so estimates may be rough. V2 browser automation will fix this.
