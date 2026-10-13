#!/usr/bin/env python3
"""
Minimal Firecrawl-compatible /v1/scrape proxy.
Returns page content as markdown. No API key needed.
"""
import asyncio, httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import html2text
from bs4 import BeautifulSoup

app = FastAPI(title="Firecrawl scraper proxy")

h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.body_width = 0


class ScrapeRequest(BaseModel):
    url: str
    formats: Optional[List[str]] = ["markdown"]
    onlyMainContent: Optional[bool] = True


@app.post("/v1/scrape")
async def scrape(req: ScrapeRequest):
    try:
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ManaGPT/1.0)"},
        ) as client:
            resp = await client.get(req.url)
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise
        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            tag.decompose()

        # Try main/article content first
        main = soup.find("main") or soup.find("article") or soup.find("body")
        html_content = str(main) if main else resp.text

        markdown = h2t.handle(html_content).strip()
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        return {
            "success": True,
            "data": {
                "markdown": markdown,
                "metadata": {"title": title, "sourceURL": req.url},
            },
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@app.get("/v1/scrape")
async def scrape_get(url: str = ""):
    if not url:
        return JSONResponse(status_code=400, content={"error": "url required"})
    return await scrape(ScrapeRequest(url=url))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)
