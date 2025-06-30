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
- OpenAI API key
- Modern web browser with microphone access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd audio_socket
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
```

4. Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

## Usage

1. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Allow microphone access when prompted

4. Click "Start Recording" to begin audio capture

5. Speak clearly into your microphone

6. Click "Stop Recording" when finished

7. View the transcribed text in real-time

## API Endpoints

### WebSocket Endpoint
- **URL**: `ws://localhost:8000/ws`
- **Purpose**: Real-time audio processing and transcription

### Health Check
- **URL**: `GET /health`
- **Purpose**: Check server status and active connections

### Web Interface
- **URL**: `GET /`
- **Purpose**: Serve the HTML client interface

## WebSocket Message Format

### Client to Server (Audio)
```json
{
  "type": "audio",
  "audio": "base64_encoded_audio_data"
}
```

### Server to Client (Responses)
```json
// Status update
{
  "type": "status",
  "message": "Processing audio..."
}

// Transcription result
{
  "type": "transcription",
  "text": "Your transcribed text here",
  "status": "success"
}

// Error message
{
  "type": "error",
  "message": "Error description"
}
```

## Project Structure

```
audio_socket/
├── main.py              # FastAPI application with WebSocket support
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
├── static/
│   └── index.html      # Web client interface
├── README.md           # Project documentation
└── LICENSE             # Project license
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### OpenAI API Setup

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add the key to your `.env` file

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Ensure your browser has permission to access the microphone
   - Check browser settings for microphone permissions

2. **OpenAI API Errors**
   - Verify your API key is correct and has sufficient credits
   - Check OpenAI service status

3. **WebSocket Connection Issues**
   - Ensure the server is running on the correct port
   - Check firewall settings

4. **Audio Quality Issues**
   - Use a good quality microphone
   - Speak clearly and avoid background noise
   - Ensure stable internet connection

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