"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from audio_socket_api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)
