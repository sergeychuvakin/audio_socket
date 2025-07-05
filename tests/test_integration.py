"""Integration tests for the Audio WebSocket API."""

from fastapi.testclient import TestClient


def test_websocket_connection_and_disconnection(client: TestClient):
    """Test WebSocket connection and disconnection."""
    with client.websocket_connect("/ws") as websocket:
        assert websocket is not None
        test_audio_data = b"fake_audio_data"
        websocket.send_bytes(test_audio_data)


def test_multiple_websocket_connections(client: TestClient):
    """Test that multiple WebSocket connections can be established."""
    with client.websocket_connect("/ws") as websocket1:
        assert websocket1 is not None
        with client.websocket_connect("/ws") as websocket2:
            assert websocket2 is not None
            assert websocket1 is not None
            assert websocket2 is not None


def test_websocket_sends_audio_data(client: TestClient):
    """Test that WebSocket can receive audio data."""
    with client.websocket_connect("/ws") as websocket:
        fake_audio = b"fake_webm_audio_data"
        websocket.send_bytes(fake_audio)


def test_health_endpoint_reflects_connections(client: TestClient):
    """Test that health endpoint shows correct connection count."""
    response = client.get("/health")
    initial_connections = response.json()["connections"]

    with client.websocket_connect("/ws") as _:
        response = client.get("/health")
        current_connections = response.json()["connections"]
        assert current_connections > initial_connections

    response = client.get("/health")
    final_connections = response.json()["connections"]
    assert final_connections == initial_connections


def test_app_endpoints_exist(client: TestClient):
    """Test that all expected endpoints exist."""
    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/health")
    assert response.status_code == 200
