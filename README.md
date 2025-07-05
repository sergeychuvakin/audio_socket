# Audio WebSocket API

A real-time audio-to-text conversion service built with FastAPI and WebSockets, powered by OpenAI's Whisper API.

## Features

- 🎤 Real-time audio recording through web browser
- 🔄 WebSocket communication for instant feedback
- 🤖 OpenAI Whisper integration for accurate speech-to-text
- 🎨 Modern, responsive web interface
- ⚡ Fast and efficient audio processing
- 🔒 Secure API key management

## Prerequisites

- Python 3.11 or higher
- UV package manager
- OpenAI API key
- Modern web browser with microphone access

## Installation

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**:
```bash
git clone <repository-url>
cd audio_socket
```

3. **Sync dependencies**:
```bash
uv sync
```

4. **Install the package in development mode**:
```bash
uv pip install -e .
```

5. **Set up environment variables**:
```bash
cp env.example .env
```

6. **Edit `.env` file and add your OpenAI API key**:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

## Usage

1. **Start the server**:
```bash
uv run audio_socket_api/main.py
```

2. **Open your browser and navigate to**:
```
http://localhost:8000
```

3. **Allow microphone access** when prompted

4. **Click "Start Recording"** to begin audio capture

5. **Speak clearly** into your microphone

6. **View the transcribed text** in real-time as it appears

7. **Click "Stop Recording"** when finished

## How It Works

1. **Audio Capture**: The web interface captures audio from your microphone in real-time
2. **WebSocket Streaming**: Audio chunks are streamed to the server via WebSocket
3. **Whisper Processing**: The server processes each audio chunk with OpenAI Whisper
4. **Real-time Display**: Transcribed text is sent back to the browser and displayed immediately

## API Endpoints

### WebSocket Endpoint
- **URL**: `ws://localhost:8000/ws`
- **Purpose**: Real-time audio processing and transcription
- **Input**: Audio data chunks (WebM format)
- **Output**: Transcribed text strings

### Health Check
- **URL**: `GET /health`
- **Purpose**: Check server status and active connections

### Web Interface
- **URL**: `GET /`
- **Purpose**: Serve the HTML client interface

## Project Structure

```
audio_socket/
├── audio_socket_api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with WebSocket support
│   └── static/
│       └── index.html       # Web client interface
├── tests/                   # Test files
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # UV lock file
├── env.example             # Environment variables template
├── README.md               # Project documentation
└── LICENSE                 # Project license
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### OpenAI API Setup

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add the key to your `.env` file

## Development

### Running in Development Mode
```bash
uv run audio_socket_api/main.py
```

### Running Tests
```bash
uv run pytest tests/
```

### API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## UV Workflow

This project uses UV as the package manager. Here's the typical workflow:

1. **Install dependencies**: `uv sync`
2. **Install package**: `uv pip install -e .`
3. **Run application**: `uv run audio_socket_api/main.py`
4. **Run tests**: `uv run pytest`
5. **Add new dependency**: `uv add package-name`

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Ensure your browser has permission to access the microphone
   - Check browser settings for microphone permissions

2. **OpenAI API Errors**
   - Verify your API key is correct and has sufficient credits
   - Check OpenAI service status
   - Ensure your `.env` file contains the correct API key

3. **WebSocket Connection Issues**
   - Ensure the server is running on the correct port
   - Check firewall settings

4. **Audio Quality Issues**
   - Use a good quality microphone
   - Speak clearly and avoid background noise
   - Ensure stable internet connection

5. **No Transcription Appearing**
   - Check browser console for WebSocket errors
   - Verify OpenAI API key is set correctly
   - Ensure you're speaking clearly into the microphone

6. **UV-related Issues**
   - Ensure UV is properly installed
   - Try running `uv sync` to refresh dependencies
   - Check that you're in the correct directory

## Security Considerations

- Never commit your `.env` file to version control
- Use HTTPS in production environments
- Implement rate limiting for production use
- Consider adding authentication for public deployments

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
