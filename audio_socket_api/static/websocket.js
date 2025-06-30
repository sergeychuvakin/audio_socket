// WebSocket Echo Client
class WebSocketClient {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000; // 3 seconds
        
        this.statusElement = document.getElementById('status');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.messagesContainer = document.getElementById('messages');
        
        this.initialize();
    }
    
    initialize() {
        this.setupEventListeners();
        this.connect();
    }
    
    connect() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            console.log('Connecting to:', wsUrl);
            this.ws = new WebSocket(wsUrl);
            this.setupWebSocketHandlers();
            
        } catch (error) {
            console.error('Connection error:', error);
            this.addSystemMessage(`Connection error: ${error.message}`);
            this.updateStatus('Connection failed', 'disconnected');
        }
    }
    
    setupWebSocketHandlers() {
        this.ws.onopen = () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.updateStatus('Connected', 'connected');
            this.enableInput();
            this.addSystemMessage('Connected to server');
            this.messageInput.focus(); // Focus input when connected
        };
        
        this.ws.onmessage = (event) => {
            this.addMessage(event.data, 'received');
        };
        
        this.ws.onclose = (event) => {
            this.isConnected = false;
            this.updateStatus('Disconnected', 'disconnected');
            this.disableInput();
            this.addSystemMessage('Disconnected from server');
            
            // Attempt to reconnect if not a clean close
            if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
                this.attemptReconnect();
            }
        };
        
        this.ws.onerror = (error) => {
            this.addSystemMessage('WebSocket error occurred');
            console.error('WebSocket error:', error);
        };
    }
    
    setupEventListeners() {
        // Send message on Enter key
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.isConnected) {
                this.sendMessage();
            }
        });
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        
        console.log('sendMessage called:', { message, isConnected: this.isConnected });
        
        if (!message || !this.isConnected) {
            console.log('Message not sent:', { hasMessage: !!message, isConnected: this.isConnected });
            return;
        }
        
        try {
            this.ws.send(message);
            this.addMessage(message, 'sent');
            this.messageInput.value = '';
            
        } catch (error) {
            console.error('Send error:', error);
            this.addSystemMessage(`Failed to send message: ${error.message}`);
        }
    }
    
    addMessage(text, type) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = type === 'sent' ? `You: ${text}` : `Server: ${text}`;
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    addSystemMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message system';
        messageElement.textContent = text;
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    updateStatus(text, className) {
        this.statusElement.textContent = text;
        this.statusElement.className = `status ${className}`;
    }
    
    enableInput() {
        this.messageInput.disabled = false;
        this.sendButton.disabled = false;
    }
    
    disableInput() {
        this.messageInput.disabled = true;
        this.sendButton.disabled = true;
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    attemptReconnect() {
        this.reconnectAttempts++;
        this.addSystemMessage(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        
        setTimeout(() => {
            if (!this.isConnected) {
                this.connect();
            }
        }, this.reconnectDelay);
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Global function for the onclick handler
function sendMessage() {
    if (window.wsClient) {
        window.wsClient.sendMessage();
    }
}

// Initialize the WebSocket client when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.wsClient = new WebSocketClient();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.wsClient) {
        window.wsClient.disconnect();
    }
}); 