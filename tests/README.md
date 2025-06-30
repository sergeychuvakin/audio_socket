# WebSocket Echo Server Tests

This directory contains comprehensive tests for the WebSocket echo server.

## Test Files

### `test_basic.py`
Basic unit tests using Python's built-in `unittest` framework. Tests HTTP endpoints and basic functionality.

**Run with:**
```bash
python tests/test_basic.py
```

### `test_integration.py`
Integration tests that test the full WebSocket functionality. This is the main test script.

**Run with:**
```bash
python tests/test_integration.py
```

### `conftest.py`
Pytest configuration file (if you want to use pytest).

## Test Coverage

### HTTP Endpoints
- ✅ Health check endpoint (`/health`)
- ✅ Root endpoint (`/`) - serves HTML client
- ✅ Static files (`/static/websocket.js`)

### WebSocket Functionality
- ✅ Basic connection and message echo
- ✅ Multiple message handling
- ✅ Connection manager state tracking
- ✅ Proper connection cleanup

### App Configuration
- ✅ FastAPI app title and configuration
- ✅ Static file mounting
- ✅ Route registration

## Running Tests

### Prerequisites
Make sure you have the required dependencies:
```bash
pip install websockets httpx
```

### Quick Test
Run the integration test (recommended):
```bash
python tests/test_integration.py
```

### Unit Tests
Run basic unit tests:
```bash
python tests/test_basic.py
```

### With Server Running
For WebSocket tests, you can optionally start the server first:
```bash
# Terminal 1: Start server
python -m audio_socket_api.main

# Terminal 2: Run tests
python tests/test_integration.py
```

## Test Output

The integration test will show:
```
🧪 WebSocket Echo Server Integration Tests
==================================================

📋 Running HTTP endpoint tests...
✅ Health endpoint
✅ Root endpoint
✅ Static files

🔌 Running WebSocket tests...
✅ WebSocket connection
✅ Multiple messages
✅ Connection manager

==================================================
TEST SUMMARY
==================================================
✅ PASS: Health endpoint
✅ PASS: Root endpoint
✅ PASS: Static files
✅ PASS: WebSocket connection
✅ PASS: Multiple messages
✅ PASS: Connection manager

Results: 6/6 tests passed
🎉 All tests passed!
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the project root:
```bash
cd /path/to/audio_socket
python tests/test_integration.py
```

### WebSocket Connection Errors
If WebSocket tests fail, make sure:
1. The server is running on `localhost:8000`
2. No firewall is blocking the connection
3. The `websockets` library is installed

### Missing Dependencies
Install required dependencies:
```bash
pip install websockets httpx fastapi uvicorn
``` 