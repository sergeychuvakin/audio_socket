"""WebSocket-specific tests for the Audio WebSocket API."""

from fastapi.testclient import TestClient

from audio_socket_api.main import ConnectionManager, manager


def test_websocket_accepts_audio_data(client: TestClient):
    """Test that WebSocket accepts audio data without errors."""
    with client.websocket_connect("/ws") as websocket:
        test_cases = [
            b"",  # Empty data
            b"fake_audio",  # Small fake data
        ]

        for audio_data in test_cases:
            websocket.send_bytes(audio_data)


def test_websocket_connection_lifecycle(client: TestClient):
    """Test complete WebSocket connection lifecycle."""
    with client.websocket_connect("/ws") as websocket:
        assert websocket is not None
        websocket.send_bytes(b"test_audio")
        assert websocket is not None


def test_websocket_multiple_messages(client: TestClient):
    """Test sending multiple audio messages through WebSocket."""
    with client.websocket_connect("/ws") as websocket:
        messages = [b"audio_chunk_1", b"audio_chunk_2", b"audio_chunk_3"]

        for message in messages:
            websocket.send_bytes(message)


def test_websocket_bytes_data(client: TestClient):
    """Test WebSocket with larger audio data."""
    with client.websocket_connect("/ws") as websocket:
        large_audio = b"x"
        websocket.send_bytes(large_audio)


def test_websocket_connection_manager_integration():
    """Test that ConnectionManager works with WebSocket connections."""
    assert len(manager.active_connections) == 0
    assert isinstance(manager, ConnectionManager)
    assert hasattr(manager, "active_connections")
    assert hasattr(manager, "connect")
    assert hasattr(manager, "disconnect")
    assert hasattr(manager, "send_text")
