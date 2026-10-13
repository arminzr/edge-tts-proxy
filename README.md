# edge-tts-proxy — Free OpenAI-Compatible TTS & Scrape Proxy

Two lightweight Python (FastAPI) services that let you use **Microsoft Edge's free neural TTS voices** and a **Firecrawl-compatible scraper** through standard OpenAI-style APIs — no paid API keys required.

- ⚡ **TTS proxy** — an OpenAI `/v1/audio/speech`-compatible endpoint powered by [`edge-tts`](https://github.com/rany2/edge-tts) (free, no key).
- 🕷️ **Scrape proxy** — a minimal Firecrawl-compatible `/v1/scrape` endpoint that returns any page as clean Markdown.

## 🎙️ 1/ TTS Proxy (`server.py`)

Serves the OpenAI speech endpoint, so any tool that speaks to OpenAI TTS works
here with `base_url` pointed at this service. Default voice is Persian female
(`fa-IR-DilaraNeural`).

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/v1/models` | Lists available models (`tts-1`, `tts-1-hd`) |
| `POST` | `/v1/audio/speech` | OpenAI-compatible text-to-speech |
| `GET` | `/health` | Liveness check |

### Example

```bash
curl http://localhost:8090/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "سلام، این یک تست است",
    "voice": "dilara",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

### Supported voices (short names → full edge-tts voices)

| Short | edge-tts voice | Notes |
|---|---|---|
| `alloy` | `en-US-GuyNeural` | English |
| `echo` | `en-US-ChristopherNeural` | English |
| `fable` | `en-GB-RyanNeural` | English (UK) |
| `onyx` | `en-US-ChristopherNeural` | English |
| `nova` | `en-US-JennyNeural` | English |
| `shimmer` | `en-US-AriaNeural` | English |
| `dilara` | `fa-IR-DilaraNeural` | **Persian (default)** |
| `davood` | `fa-IR-DavoodNeural` | Persian |
| `farid` | `fa-IR-FaridNeural` | Persian |
| `fatemeh` | `fa-IR-FatemehNeural` | Persian |

You can also pass any full edge-tts voice name; it is validated against
`edge_tts.list_voices()`.

## 🕷️ 2/ Scrape Proxy (`scraper.py`)

A minimal, no-key Firecrawl-compatible scraper. It fetches a URL, strips
`<script>`, `<style>`, `<nav>`, `<footer>`, etc., extracts the main content, and
returns it as **Markdown**.

### Example

```bash
curl http://localhost:8091/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

Response:

```json
{
  "success": true,
  "data": {
    "markdown": "# Example Domain ...",
    "metadata": {"title": "Example Domain", "sourceURL": "https://example.com"}
  }
}
```

## 🚀 Run

```bash
# install deps
pip install -r requirements.txt   # (fastapi, uvicorn, edge-tts, httpx, html2text, beautifulsoup4)

# TTS proxy  → http://localhost:8090
python server.py

# Scrape proxy → http://localhost:8091
python scraper.py
```

> `requirements.txt` — add the deps shown in the comment above (they are the
> imports used by `server.py` and `scraper.py`). A ready-made `requirements.txt`
> is included in releases.

Both services can be run together under any reverse proxy (e.g. nginx) to
expose a single base URL.

## 🧠 How it works

- **TTS**: `edge-tts` talks to Microsoft's free neural TTS service, so you get
  high-quality voices without paying. The proxy translates OpenAI's speed
  parameter (`1.0`, `1.25`, …) into edge-tts `+XX% / -XX%` rates.
- **Scraper**: `httpx` + `BeautifulSoup` + `html2text` turn any web page into
  clean, LLM-ready Markdown.

## ⚙️ Configuration

- **Ports**: default `8090` (TTS) and `8091` (scrape) — change at the bottom of
  each file.
- **No keys, no config files** — each tool works out of the box.

## 📄 License

MIT.
