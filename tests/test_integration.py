#!/usr/bin/env python3
"""
Integration tests for WebSocket echo server.
Run this script to test the server functionality.
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import websockets
    from fastapi.testclient import TestClient

    from audio_socket_api.main import app, manager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies: pip install websockets httpx")
    sys.exit(1)


class WebSocketTester:
    """Integration tester for WebSocket server."""

    def __init__(self):
        self.client = TestClient(app)
        self.test_results = []

    def run_test(self, test_name, test_func):
        """Run a test and record the result."""
        try:
            test_func()
            print(f"✅ {test_name}")
            self.test_results.append((test_name, True, None))
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            self.test_results.append((test_name, False, str(e)))

    async def run_async_test(self, test_name, test_func):
        """Run an async test and record the result."""
        try:
            await test_func()
            print(f"✅ {test_name}")
            self.test_results.append((test_name, True, None))
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            self.test_results.append((test_name, False, str(e)))

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "connections" in data

    def test_root_endpoint(self):
        """Test root endpoint serves HTML."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "WebSocket Echo Client" in response.text

    def test_static_files(self):
        """Test static files are served correctly."""
        response = self.client.get("/static/websocket.js")
        assert response.status_code == 200
        assert "WebSocketClient" in response.text

    async def test_websocket_connection(self):
        """Test basic WebSocket connection."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            test_message = "Hello, WebSocket!"
            await websocket.send(test_message)

            response = await websocket.recv()
            assert response == f"Echo: {test_message}"

    async def test_multiple_messages(self):
        """Test sending multiple messages."""
        uri = "ws://localhost:8000/ws"

        async with websockets.connect(uri) as websocket:
            messages = ["First", "Second", "Third"]

            for message in messages:
                await websocket.send(message)
                response = await websocket.recv()
                assert response == f"Echo: {message}"

    async def test_connection_manager(self):
        """Test connection manager functionality."""
        initial_connections = len(manager.active_connections)

        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri) as websocket:
            # Check that connection is tracked
            assert len(manager.active_connections) == initial_connections + 1

            # Send a message
            await websocket.send("Test message")
            response = await websocket.recv()
            assert response == "Echo: Test message"

        # Check that connection is removed after disconnect
        await asyncio.sleep(0.1)  # Give time for cleanup
        assert len(manager.active_connections) == initial_connections

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)

        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)

        for test_name, success, error in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {test_name}")
            if error:
                print(f"   Error: {error}")

        print(f"\nResults: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("💥 Some tests failed!")
            return False


async def main():
    """Run all integration tests."""
    print("🧪 WebSocket Echo Server Integration Tests")
    print("=" * 50)

    tester = WebSocketTester()

    # Run synchronous tests
    print("\n📋 Running HTTP endpoint tests...")
    tester.run_test("Health endpoint", tester.test_health_endpoint)
    tester.run_test("Root endpoint", tester.test_root_endpoint)
    tester.run_test("Static files", tester.test_static_files)

    # Run asynchronous tests
    print("\n🔌 Running WebSocket tests...")
    await tester.run_async_test("WebSocket connection", tester.test_websocket_connection)
    await tester.run_async_test("Multiple messages", tester.test_multiple_messages)
    await tester.run_async_test("Connection manager", tester.test_connection_manager)

    # Print summary
    success = tester.print_summary()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
