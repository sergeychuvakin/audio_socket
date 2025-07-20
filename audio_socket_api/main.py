"""WebSocket audio recognition server using OpenAI Whisper."""

import io

import fleep
import openai
import pydub
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from audio_socket_api import AUDIO_SOCKET_ROOT_PATH

# Load env vars and configure logging
load_dotenv()
UNIFIED_AUDIO_FORMAT = "wav"

app = FastAPI(title="Audio WebSocket API", description="Realtime transcription with Whisper")
app.mount("/static", StaticFiles(directory=AUDIO_SOCKET_ROOT_PATH / "static"), name="static")


class ConnectionManager:  # pylint: disable=missing-class-docstring
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):  # pylint: disable=missing-function-docstring
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected. Total: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):  # pylint: disable=missing-function-docstring
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("Client disconnected. Total: %d", len(self.active_connections))

    async def send_text(self, websocket: WebSocket, text: str):  # pylint: disable=missing-function-docstring
        await websocket.send_text(text)


manager = ConnectionManager()


def detect_audio_format(audio_data: bytes) -> str:
    """Detect the audio format of the audio data."""
    audio_info = fleep.get(audio_data)
    return audio_info.extension.pop()


def convert_audio_to_wav(
    audio_data: bytes,
    input_format: str = "webm",
    output_format: str = "wav",
) -> bytes:
    """Convert the audio data to WAV format."""
    audio = pydub.AudioSegment.from_file(io.BytesIO(audio_data), format=input_format)
    audio_io_buffer = io.BytesIO()
    audio.export(audio_io_buffer, format=output_format)
    audio_io_buffer.seek(0)
    return audio_io_buffer.getvalue()


async def process_audio_with_whisper(audio_data: bytes) -> str:
    """Process audio with Whisper (supports multiple formats)."""
    try:
        # Log the first few bytes to help identify the format
        logger.info(f"Processing audio chunk of size: {len(audio_data)} bytes")
        logger.info(f"First 16 bytes: {audio_data[:16].hex()}")

        audio_format = detect_audio_format(audio_data)
        if audio_format != UNIFIED_AUDIO_FORMAT:
            audio_data = convert_audio_to_wav(audio_data, audio_format)

        # Create BytesIO object from audio data
        audio_file = io.BytesIO(audio_data)
        audio_file.name = f"audio.{UNIFIED_AUDIO_FORMAT}"  # Give it a filename for OpenAI

        result = openai.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio_file)
        logger.info(f"Transcription successful: {result.text[:50]}...")
        return result.text

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception("Whisper processing failed")
        return f"[ERROR] Transcription failed: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    html_path = AUDIO_SOCKET_ROOT_PATH / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle audio WebSocket stream and send back transcribed text."""
    await manager.connect(websocket)
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            logger.info(f"Received audio data: {len(audio_bytes)} bytes")
            transcription = await process_audio_with_whisper(audio_bytes)
            await manager.send_text(websocket, transcription)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        manager.disconnect(websocket)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception("WebSocket error: %s", e)
        manager.disconnect(websocket)


@app.get("/health")
async def health():
    """Health-check."""
    return {"status": "ok", "connections": len(manager.active_connections)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
