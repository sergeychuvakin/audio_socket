# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./
# Copy application code
COPY audio_socket_api/ ./audio_socket_api/

# Install dependencies
RUN uv sync --frozen

# Install the package
RUN uv pip install .

# Expose port
EXPOSE 8000
# Run the application
CMD ["uv", "run", "uvicorn", "audio_socket_api.main:app", "--host", "0.0.0.0", "--port", "8000"]