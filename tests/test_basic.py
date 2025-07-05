"""Basic tests for the Audio WebSocket API."""

import fastapi
import openai
from fastapi.testclient import TestClient

from audio_socket_api.main import ConnectionManager, app, process_audio_with_whisper


def test_health_endpoint(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200


def test_root_endpoint_returns_html(client: TestClient):
    """Test that the root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html_content = response.text
    assert "<html" in html_content.lower()
    assert "<head" in html_content.lower()
    assert "<body" in html_content.lower()


def test_websocket_endpoint_exists(client: TestClient):
    """Test that the WebSocket endpoint is properly configured."""
    with client.websocket_connect("/ws") as websocket:
        assert websocket is not None


def test_connection_manager():
    """Test the ConnectionManager class."""

    manager = ConnectionManager()
    assert len(manager.active_connections) == 0


def test_process_audio_function_exists():
    """Test that the audio processing function exists and is callable."""

    assert callable(process_audio_with_whisper)


def test_app_configuration():
    """Test that the FastAPI app is properly configured."""

    assert app.title == "Audio WebSocket API"
    assert "Realtime transcription with Whisper" in app.description


def test_imports_work():
    """Test that all required imports work correctly."""

    assert openai is not None
    assert fastapi is not None
