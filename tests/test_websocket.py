"""Tests for WebSocket echo server functionality."""

import asyncio
import json

import pytest
import websockets
from fastapi.testclient import TestClient

from audio_socket_api.main import app


class TestWebSocketServer:
    """Test WebSocket server functionality."""

    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
        self.base_url = "ws://localhost:8000/ws"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "connections" in data
        assert data["status"] == "healthy"
        assert isinstance(data["connections"], int)

    def test_root_endpoint(self):
        """Test root endpoint serves HTML."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "WebSocket Echo Client" in response.text

    def test_static_files(self):
        """Test static files are served correctly."""
        response = self.client.get("/static/websocket.js")
        assert response.status_code == 200
        assert "text/javascript" in response.headers["content-type"]
        assert "WebSocketClient" in response.text

    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test basic WebSocket connection."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            # Test that we can send and receive a message
            test_message = "Hello, WebSocket!"
            await websocket.send(test_message)

            response = await websocket.recv()
            assert response == f"Echo: {test_message}"

    @pytest.mark.asyncio
    async def test_multiple_messages(self):
        """Test sending multiple messages."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            messages = ["First message", "Second message", "Third message"]

            for message in messages:
                await websocket.send(message)
                response = await websocket.recv()
                assert response == f"Echo: {message}"

    @pytest.mark.asyncio
    async def test_empty_message(self):
        """Test handling of empty messages."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            await websocket.send("")
            response = await websocket.recv()
            assert response == "Echo: "

    @pytest.mark.asyncio
    async def test_special_characters(self):
        """Test messages with special characters."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            special_message = "Hello! @#$%^&*()_+-=[]{}|;':\",./<>?"
            await websocket.send(special_message)

            response = await websocket.recv()
            assert response == f"Echo: {special_message}"

    @pytest.mark.asyncio
    async def test_unicode_messages(self):
        """Test messages with unicode characters."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            unicode_message = "Hello 世界! 🌍 Привет! 🚀"
            await websocket.send(unicode_message)

            response = await websocket.recv()
            assert response == f"Echo: {unicode_message}"

    @pytest.mark.asyncio
    async def test_long_message(self):
        """Test handling of long messages."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            long_message = "A" * 1000  # 1000 character message
            await websocket.send(long_message)

            response = await websocket.recv()
            assert response == f"Echo: {long_message}"

    @pytest.mark.asyncio
    async def test_connection_manager(self):
        """Test connection manager functionality."""
        from audio_socket_api.main import manager

        # Check initial state
        assert len(manager.active_connections) == 0

        # Connect a client
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as websocket:
            # Check that connection is tracked
            assert len(manager.active_connections) == 1

            # Send a message
            await websocket.send("Test message")
            response = await websocket.recv()
            assert response == "Echo: Test message"

        # Check that connection is removed after disconnect
        assert len(manager.active_connections) == 0

    @pytest.mark.asyncio
    async def test_multiple_connections(self):
        """Test multiple simultaneous connections."""
        uri = "ws://localhost:8000/ws"

        async def test_single_connection(connection_id):
            async with websockets.connect(uri) as websocket:
                message = f"Message from connection {connection_id}"
                await websocket.send(message)
                response = await websocket.recv()
                assert response == f"Echo: {message}"

        # Test multiple connections simultaneously
        tasks = [test_single_connection(i) for i in range(3)]
        await asyncio.gather(*tasks)

    @pytest.mark.asyncio
    async def test_connection_disconnect(self):
        """Test proper handling of connection disconnection."""
        from audio_socket_api.main import manager

        uri = "ws://localhost:8000/ws"

        # Create connection
        websocket = await websockets.connect(uri)
        assert len(manager.active_connections) == 1

        # Close connection
        await websocket.close()
        await asyncio.sleep(0.1)  # Give time for cleanup

        # Check that connection is removed
        assert len(manager.active_connections) == 0

    def test_app_configuration(self):
        """Test FastAPI app configuration."""
        assert app.title == "Simple WebSocket API"

        # Check that required routes exist
        routes = [route.path for route in app.routes if hasattr(route, "path")]
        assert "/" in routes
        assert "/health" in routes

        # Check that static files are mounted
        static_mounts = [route.path for route in app.routes if hasattr(route, "name") and route.name == "static"]
        assert len(static_mounts) > 0
