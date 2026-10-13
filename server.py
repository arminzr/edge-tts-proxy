#!/usr/bin/env python3
"""
edge-tts proxy — OpenAI-compatible /v1/audio/speech endpoint.
Accepts OpenAI TTS requests and replies with edge-tts audio.
"""
import io, asyncio, json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import edge_tts

app = FastAPI(title="edge-tts proxy")

# Default Persian female voice
DEFAULT_VOICE = "fa-IR-DilaraNeural"

# Map short voice names to full edge-tts voices if needed
VOICE_MAP = {
    "alloy": "en-US-GuyNeural",
    "echo": "en-US-ChristopherNeural",
    "fable": "en-GB-RyanNeural",
    "onyx": "en-US-ChristopherNeural",
    "nova": "en-US-JennyNeural",
    "shimmer": "en-US-AriaNeural",
    # Persian voices
    "dilara": "fa-IR-DilaraNeural",
    "davood": "fa-IR-DavoodNeural",
    "farid": "fa-IR-FaridNeural",
    "fatemeh": "fa-IR-FatemehNeural",
}


class TTSRequest(BaseModel):
    model: str = "tts-1"
    input: str
    voice: str = "dilara"
    response_format: str = "mp3"  # mp3, opus, aac, flac, wav, pcm
    speed: float = 1.0


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "tts-1", "object": "model", "owned_by": "edge-tts"},
            {"id": "tts-1-hd", "object": "model", "owned_by": "edge-tts"},
        ],
    }


@app.post("/v1/audio/speech")
async def create_speech(req: TTSRequest):
    voice = VOICE_MAP.get(req.voice.lower(), req.voice)

    # Validate voice exists
    available = await edge_tts.list_voices()
    voice_ids = {v["ShortName"] for v in available}
    if voice not in voice_ids:
        return JSONResponse(
            status_code=400,
            content={"error": f"Voice '{voice}' not found. Use a valid edge-tts voice name."},
        )

    # Rate adjustment: edge-tts uses +XX% or -XX% format
    if req.speed == 1.0:
        rate = "+0%"
    elif req.speed > 1.0:
        rate = f"+{int((req.speed - 1) * 100)}%"
    else:
        rate = f"-{int((1 - req.speed) * 100)}%"

    communicate = edge_tts.Communicate(req.input, voice, rate=rate)

    # Choose output format
    fmt_map = {"mp3": "mp3", "opus": "mp3", "aac": "mp3", "flac": "mp3", "wav": "mp3", "pcm": "mp3"}
    media_type_map = {"mp3": "audio/mpeg", "opus": "audio/ogg", "aac": "audio/aac", "flac": "audio/flac", "wav": "audio/wav", "pcm": "audio/pcm"}

    fmt = fmt_map.get(req.response_format, "mp3")
    media_type = media_type_map.get(req.response_format, "audio/mpeg")

    async def audio_stream():
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(audio_stream(), media_type=media_type)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "edge-tts-proxy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
