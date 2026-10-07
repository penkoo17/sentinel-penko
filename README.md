# Sentinel

Security scanner & AI analyst untuk website publik.

## Disclaimer

Gunakan hanya pada website yang kamu miliki atau punya izin tertulis.

## Fitur

- Security header analysis
- Cookie flag check
- TLS certificate inspection
- CORS configuration check
- DNS records (SPF, DMARC)
- Crawler + endpoint discovery
- JavaScript endpoint extraction
- Exposed secret detection
- AI security report (Google Gemini)
- Security score 0-100

## Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Isi `GEMINI_API_KEY` di `.env`.

## Run

```
./run.sh
```

API: http://localhost:8000
UI: http://localhost:8501

## Stack

Python 3.11+ · FastAPI · httpx · BeautifulSoup · Google Gemini · Streamlit
