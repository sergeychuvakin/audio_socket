"""Simple WebSocket server with echo functionality."""

import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from audio_socket_api import AUDIO_SOCKET_ROOT_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Simple WebSocket API")

# Mount static files
app.mount("/static", StaticFiles(directory=AUDIO_SOCKET_ROOT_PATH / "static"), name="static")


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections and message sending."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected. Total connections: %s", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from active connections."""
        self.active_connections.remove(websocket)
        logger.info("Client disconnected. Total connections: %s", len(self.active_connections))

    async def send_message(self, message: str, websocket: WebSocket):
        """Send a text message to a specific WebSocket connection."""
        await websocket.send_text(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get():
    """Serve a simple HTML client"""
    with open(AUDIO_SOCKET_ROOT_PATH / "static" / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Simple WebSocket endpoint that echoes messages"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info("Received: %s", data)

            # Echo the message back
            await manager.send_message(f"Echo: {data}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except (ValueError, RuntimeError) as e:
        logger.error("WebSocket error: %s", e)
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "connections": len(manager.active_connections)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
