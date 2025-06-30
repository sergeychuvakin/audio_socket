"""Basic tests for WebSocket echo server."""

import asyncio
import json
import unittest

from fastapi.testclient import TestClient

from audio_socket_api.main import app, manager


class TestWebSocketBasic(unittest.TestCase):
    """Basic tests for WebSocket server."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("status", data)
        self.assertIn("connections", data)
        self.assertEqual(data["status"], "healthy")
        self.assertIsInstance(data["connections"], int)

    def test_root_endpoint(self):
        """Test root endpoint serves HTML."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("WebSocket Echo Client", response.text)

    def test_static_files(self):
        """Test static files are served correctly."""
        response = self.client.get("/static/websocket.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/javascript", response.headers["content-type"])
        self.assertIn("WebSocketClient", response.text)

    def test_app_configuration(self):
        """Test FastAPI app configuration."""
        self.assertEqual(app.title, "Simple WebSocket API")

    def test_connection_manager_initial_state(self):
        """Test connection manager initial state."""
        self.assertEqual(len(manager.active_connections), 0)


class TestWebSocketAsync(unittest.IsolatedAsyncioTestCase):
    """Async tests for WebSocket functionality."""

    async def test_websocket_connection(self):
        """Test basic WebSocket connection."""
        try:
            import websockets

            uri = "ws://localhost:8000/ws"

            async with websockets.connect(uri) as websocket:
                # Test that we can send and receive a message
                test_message = "Hello, WebSocket!"
                await websocket.send(test_message)

                response = await websocket.recv()
                self.assertEqual(response, f"Echo: {test_message}")

        except ImportError:
            self.skipTest("websockets library not available")

    async def test_multiple_messages(self):
        """Test sending multiple messages."""
        try:
            import websockets

            uri = "ws://localhost:8000/ws"

            async with websockets.connect(uri) as websocket:
                messages = ["First message", "Second message", "Third message"]

                for message in messages:
                    await websocket.send(message)
                    response = await websocket.recv()
                    self.assertEqual(response, f"Echo: {message}")

        except ImportError:
            self.skipTest("websockets library not available")


if __name__ == "__main__":
    unittest.main()
