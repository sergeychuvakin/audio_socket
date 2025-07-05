# Tests

This directory contains basic tests for the Audio WebSocket API.

## Test Files

- `test_basic.py` - Basic functionality tests (endpoints, imports, configuration)
- `test_integration.py` - Integration tests (WebSocket connections, health checks)
- `test_websocket.py` - WebSocket-specific tests (audio data handling, connections)
- `conftest.py` - Pytest configuration and fixtures

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_basic.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=audio_socket_api
```

## Test Coverage

The tests cover:

- ✅ Health endpoint functionality
- ✅ Root endpoint (HTML serving)
- ✅ WebSocket connection establishment
- ✅ Audio data handling
- ✅ Connection manager functionality
- ✅ Error handling
- ✅ Basic imports and configuration

## Notes

- Tests use fake audio data since we can't easily mock OpenAI API
- WebSocket tests focus on connection handling rather than transcription results
- Integration tests verify the application works end-to-end
- Basic tests ensure all components are properly configured

## Adding New Tests

When adding new tests:

1. Use descriptive test function names
2. Add docstrings explaining what each test does
3. Keep tests simple and focused
4. Use the `client` fixture for HTTP/WebSocket tests
5. Test both success and error cases 