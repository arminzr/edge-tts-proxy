# edge-tts-proxy — Free, OpenAI-Compatible TTS & Scrape Proxy

Two lightweight Python (FastAPI) services that let you use **Microsoft Edge's free neural TTS voices** and a **Firecrawl-compatible scraper** through standard OpenAI-style APIs — no paid API keys required.

- ⚡ **TTS proxy** — an OpenAI `/v1/audio/speech`-compatible endpoint powered by [`edge-tts`](https://github.com/rany2/edge-tts) (free, no key).
- 🕷️ **Scrape proxy** — a minimal Firecrawl-compatible `/v1/scrape` endpoint that returns any page as clean Markdown.

## 🎙️ 1/ TTS Proxy (`server.py`)

Serves the OpenAI speech endpoint, so any tool that speaks to OpenAI TTS can use it with `base_url` pointed here. Default voice is Persian female (`fa-IR-DilaraNeural`).

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
  -d '{"model":"tts-1","input":"سلام، این یک تست است","voice":"dilara","response_format":"mp3","speed":1.0}' \
  --output speech.mp3
```

### Supported voices (short → full edge-tts)

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

You can also pass any full edge-tts voice name; it is validated against `edge_tts.list_voices()`.

## 🕷️ 2/ Scrape Proxy (`scraper.py`)

A minimal, no-key Firecrawl-compatible scraper. It fetches a URL, strips `<script>`, `<style>`, `<nav>`, `<footer>`, etc., extracts the main content, and returns it as **Markdown**.

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
# install deps (fastapi, uvicorn, edge-tts, httpx, html2text, beautifulsoup4)
pip install -r requirements.txt

# TTS proxy  → http://localhost:8090
python server.py

# Scrape proxy → http://localhost:8091
python scraper.py
```

Both services can be run together under any reverse proxy (e.g. nginx) to expose a single base URL.

## 🧠 How it works

- **TTS**: `edge-tts` talks to Microsoft's free neural TTS service, so you get high-quality voices without paying. The proxy translates OpenAI's speed (`1.0`, `1.25`, …) into edge-tts `+XX% / -XX%` rates.
- **Scraper**: `httpx` + `BeautifulSoup` + `html2text` turn any web page into clean, LLM-ready Markdown.

## ⚙️ Configuration

- **Ports**: default `8090` (TTS) and `8091` (scrape) — change at the bottom of each file.
- **No keys, no config files** — each tool works out of the box.

## 📄 License

MIT.

---

# نسخهٔ فارسی

# edge-tts-proxy — پروکسی TTS و اسکرپ رایگان سازگار با OpenAI

دو سرویس سبک پایتون (FastAPI) که بهت اجازه میدن از **صدای‌های عصبی رایگان Microsoft Edge** و یک **اسکرپر سازگار با Firecrawl** از طریق API های استاندارد شبیه OpenAI استفاده کنی — بدون نیاز به کلید پولی.

- ⚡ **پروکسی TTS** — یک اندپوینت سازگار با `/v1/audio/speech` مبتنی بر [`edge-tts`](https://github.com/rany2/edge-tts) (رایگان، بدون کلید).
- 🕷️ **پروکسی اسکرپ** — یک اندپوینت حداقلی سازگار با `/v1/scrape` که محتوای هر صفحه رو به صورت Markdown تمیز برمی‌گردونه.

## 🎙️ ۱/ پروکسی TTS (`server.py`)

اندپوینت سخن OpenAI رو ارائه میده، پس هر ابزاری که با OpenAI TTS کار میکنه، با تنظیم `base_url` به این سرویس میتونه استفادهش کنه. صدای پیش‌فرض، فارسی زنانه (`fa-IR-DilaraNeural`) است.

### اندپوینت‌ها

| متد | مسیر | کاربرد |
|---|---|---|
| `GET` | `/v1/models` | لیست مدل‌های موجود (`tts-1`, `tts-1-hd`) |
| `POST` | `/v1/audio/speech` | متن‌به‌صدا سازگار با OpenAI |
| `GET` | `/health` | بررسی سلامت |

### مثال

```bash
curl http://localhost:8090/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"tts-1","input":"سلام، این یک تست است","voice":"dilara","response_format":"mp3","speed":1.0}' \
  --output speech.mp3
```

### صداهای پشتیبانی‌شده (نام کوتاه → صدای کامل edge-tts)

| کوتاه | صدای edge-tts | توضیح |
|---|---|---|
| `alloy` | `en-US-GuyNeural` | انگلیسی |
| `echo` | `en-US-ChristopherNeural` | انگلیسی |
| `fable` | `en-GB-RyanNeural` | انگلیسی (بریتانیا) |
| `onyx` | `en-US-ChristopherNeural` | انگلیسی |
| `nova` | `en-US-JennyNeural` | انگلیسی |
| `shimmer` | `en-US-AriaNeural` | انگلیسی |
| `dilara` | `fa-IR-DilaraNeural` | **فارسی (پیش‌فرض)** |
| `davood` | `fa-IR-DavoodNeural` | فارسی |
| `farid` | `fa-IR-FaridNeural` | فارسی |
| `fatemeh` | `fa-IR-FatemehNeural` | فارسی |

همچنین می‌تونی هر نام صدای کامل edge-tts رو بدی؛ در برابر `edge_tts.list_voices()` اعتبارسنجی میشه.

## 🕷️ ۲/ پروکسی اسکرپ (`scraper.py`)

یک اسکرپر حداقلی و بدون کلید، سازگار با Firecrawl. URL رو واکشی می‌کنه، `<script>`، `<style>`، `<nav>`، `<footer>` و … رو حذف می‌کنه، محتوای اصلی رو استخراج می‌کنه و به صورت **Markdown** برمی‌گردونه.

### مثال

```bash
curl http://localhost:8091/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

پاسخ:

```json
{
  "success": true,
  "data": {
    "markdown": "# Example Domain ...",
    "metadata": {"title": "Example Domain", "sourceURL": "https://example.com"}
  }
}
```

## 🚀 اجرا

```bash
# نصب وابستگی‌ها (fastapi, uvicorn, edge-tts, httpx, html2text, beautifulsoup4)
pip install -r requirements.txt

# پروکسی TTS  → http://localhost:8090
python server.py

# پروکسی اسکرپ → http://localhost:8091
python scraper.py
```

هر دو سرویس می‌تونن پشت هر reverse proxy (مثلاً nginx) با هم اجرا بشن تا یک base URL واحد در اختیار باشه.

## 🧠 چطور کار می‌کنه

- **TTS**: `edge-tts` با سرویس رایگان عصبی مایکروسافت ارتباط برقرار می‌کنه، پس بدون پرداخت، صدای باکیفیت می‌گیری. پروکسی پارامتر سرعت OpenAI (`1.0`, `1.25`، …) رو به نرخ `+XX% / -XX%` ادج تی‌تی‌اس تبدیل می‌کنه.
- **اسکرپر**: `httpx` + `BeautifulSoup` + `html2text` هر صفحهٔ وب رو به Markdown تمیز آمادهٔ LLM تبدیل می‌کنن.

## ⚙️ پیکربندی

- **پورت‌ها**: پیش‌فرض `8090` (TTS) و `8091` (اسکرپ) — در انتهای هر فایل تغییرش بده.
- **بدون کلید، بدون فایل پیکربندی** — هر ابزار آمادهٔ استفاده است.

## 📄 مجوز

MIT.
