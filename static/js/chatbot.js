// Chat Widget Functionality
class SoraChatBot {
    constructor() {
        this.isOpen = false;
        this.isListening = false;
        this.recognition = null;
        this.synthesis = null;
        this.threadId = localStorage.getItem('chatThreadId') || this.generateUUID();
        this.isVoiceInput = false; // Track if current input is from voice
        
        this.initElements();
        this.initSpeechAPI();
        this.bindEvents();
        
        localStorage.setItem('chatThreadId', this.threadId);
    }
    
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    
    initElements() {
        this.chatToggle = document.getElementById('chatToggle');
        this.chatContainer = document.getElementById('chatContainer');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.voiceButton = document.getElementById('voiceButton');
        this.sendButton = document.getElementById('sendButton');
        this.inputWrapper = document.getElementById('inputWrapper');
        this.typingIndicator = document.getElementById('typingIndicator');
    }
    
    initSpeechAPI() {
        // Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.voiceButton.classList.add('listening');
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.voiceButton.classList.remove('listening');
            };
            
            this.recognition.onresult = (event) => {
                const query = event.results[0][0].transcript;
                this.chatInput.value = query;
                this.isVoiceInput = true; // Mark this as voice input
                this.sendMessage();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.addMessage('bot', "Sorry, I couldn't understand. Please try speaking again or type your message.", true);
                this.isVoiceInput = false; // Reset voice input flag on error
            };
        } else {
            this.voiceButton.style.display = 'none';
        }
        
        // Speech Synthesis
        if ('speechSynthesis' in window) {
            this.synthesis = window.speechSynthesis;
            
            // Initialize voice loading
            this.initVoices();
        }
    }
    
    initVoices() {
        // Load and log available voices for better voice selection
        const loadVoices = () => {
            const voices = this.synthesis.getVoices();
            console.log('🎤 Available voices:', voices.length);
            
            // Log high-quality voices for debugging
            const qualityVoices = voices.filter(voice => 
                voice.lang.startsWith('en') && 
                (voice.name.toLowerCase().includes('samantha') ||
                 voice.name.toLowerCase().includes('susan') ||
                 voice.name.toLowerCase().includes('zira') ||
                 voice.name.toLowerCase().includes('neural') ||
                 voice.name.toLowerCase().includes('premium'))
            );
            
            if (qualityVoices.length > 0) {
                console.log('🎯 High-quality female voices found:', 
                    qualityVoices.map(v => v.name).join(', '));
            }
        };
        
        // Load voices immediately if available
        if (this.synthesis.getVoices().length > 0) {
            loadVoices();
        } else {
            // Wait for voices to load
            this.synthesis.addEventListener('voiceschanged', loadVoices);
            
            // Fallback: try loading after a delay
            setTimeout(loadVoices, 1000);
        }
    }
    
    bindEvents() {
        this.chatToggle.addEventListener('click', () => this.toggleChat());
        this.sendButton.addEventListener('click', () => {
            this.isVoiceInput = false; // Mark as text input
            this.sendMessage();
        });
        this.voiceButton.addEventListener('click', () => this.toggleVoice());
        
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.isVoiceInput = false; // Mark as text input
                this.sendMessage();
            }
        });
        
        this.chatInput.addEventListener('focus', () => {
            this.inputWrapper.classList.add('focused');
        });
        
        this.chatInput.addEventListener('blur', () => {
            this.inputWrapper.classList.remove('focused');
        });
        
        // Auto-resize input
        this.chatInput.addEventListener('input', (e) => {
            this.sendButton.disabled = !e.target.value.trim();
        });
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatContainer.classList.toggle('active', this.isOpen);
        this.chatToggle.classList.toggle('active', this.isOpen);
        
        if (this.isOpen) {
            this.chatInput.focus();
            this.scrollToBottom();
            // Speak welcome message only on first open
            if (this.chatMessages.children.length === 1) {
                setTimeout(() => {
                    this.speak("Hi! I'm Sora, Deriv's AI assistant. How can I help you today?");
                }, 500);
            }
        }
    }
    
    toggleVoice() {
        if (!this.recognition) return;
        
        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;
        
        this.addMessage('user', message);
        this.chatInput.value = '';
        this.sendButton.disabled = true;
        
        this.showTyping(true);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: message,
                    thread_id: this.threadId
                })
            });
            
            const data = await response.json();
            
            this.showTyping(false);
            // Only speak if the input was from voice
            this.addMessage('bot', data.response, this.isVoiceInput);
            this.threadId = data.thread_id;
            
            // Reset voice input flag
            this.isVoiceInput = false;
            
        } catch (error) {
            console.error('Chat error:', error);
            this.showTyping(false);
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again.', false);
            this.isVoiceInput = false; // Reset voice input flag on error
        }
    }
    
    addMessage(sender, text, speak = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.textContent = text;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());
        
        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        if (speak && sender === 'bot') {
            this.speak(text);
        }
    }
    
    showTyping(show) {
        this.typingIndicator.style.display = show ? 'flex' : 'none';
        if (show) {
            // Faster scrolling for better perceived performance
            this.scrollToBottom();
            // Keep input ready for faster interactions
            this.chatInput.focus();
        }
    }
    
    speak(text) {
        if (!this.synthesis) return;
        
        // Stop any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // More natural speech parameters - 10% faster
        utterance.rate = 0.935 + Math.random() * 0.11; // 0.935-1.045 for variation (10% faster)
        utterance.pitch = 1.05 + Math.random() * 0.1; // 1.05-1.15 for natural feminine pitch
        utterance.volume = 0.85 + Math.random() * 0.1; // 0.85-0.95 for slight volume variation
        utterance.lang = 'en-US';
        
        // Priority order for high-quality, natural-sounding female voices
        const voices = this.synthesis.getVoices();
        
        // First, try premium/neural voices (usually have "Neural" or "Premium" in name)
        const premiumFemaleVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('neural') ||
             voice.name.toLowerCase().includes('premium') ||
             voice.name.toLowerCase().includes('enhanced')) &&
            (voice.name.toLowerCase().includes('female') ||
             voice.name.toLowerCase().includes('woman') ||
             voice.name.toLowerCase().includes('samantha') ||
             voice.name.toLowerCase().includes('susan') ||
             voice.name.toLowerCase().includes('karen') ||
             voice.name.toLowerCase().includes('moira') ||
             voice.name.toLowerCase().includes('tessa') ||
             voice.name.toLowerCase().includes('fiona') ||
             voice.name.toLowerCase().includes('serena') ||
             voice.name.toLowerCase().includes('ava') ||
             voice.name.toLowerCase().includes('allison') ||
             voice.name.toLowerCase().includes('zira') ||
             voice.name.toLowerCase().includes('hazel') ||
             voice.name.toLowerCase().includes('aria') ||
             voice.name.toLowerCase().includes('jenny') ||
             voice.name.toLowerCase().includes('nova'))
        );
        
        // Then try high-quality system voices known for natural sound
        const qualityFemaleVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('samantha') ||   // Mac - very natural
             voice.name.toLowerCase().includes('susan') ||      // Mac - clear
             voice.name.toLowerCase().includes('moira') ||      // Mac - Irish accent
             voice.name.toLowerCase().includes('tessa') ||      // Mac - South African
             voice.name.toLowerCase().includes('fiona') ||      // Mac - Scottish
             voice.name.toLowerCase().includes('karen') ||      // Mac - Australian
             voice.name.toLowerCase().includes('zira') ||       // Windows - natural
             voice.name.toLowerCase().includes('hazel') ||      // Windows - British
             voice.name.toLowerCase().includes('aria') ||       // Windows - modern
             voice.name.toLowerCase().includes('jenny'))        // Windows - conversational
        );
        
        // Fallback to any reasonable female voice
        const anyFemaleVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            (voice.name.toLowerCase().includes('female') ||
             voice.name.toLowerCase().includes('woman')) &&
            !voice.name.toLowerCase().includes('male')
        );
        
        // Last resort - avoid obviously male voices
        const neutralVoice = voices.find(voice => 
            voice.lang.startsWith('en') && 
            !voice.name.toLowerCase().includes('male') &&
            !voice.name.toLowerCase().includes('man') &&
            !voice.name.toLowerCase().includes('guy')
        );
        
        // Select the best available voice in priority order
        const selectedVoice = premiumFemaleVoice || qualityFemaleVoice || anyFemaleVoice || neutralVoice;
        
        if (selectedVoice) {
            utterance.voice = selectedVoice;
            console.log(`🎤 Sora speaking with: ${selectedVoice.name} (${selectedVoice.lang})`);
            
            // Adjust parameters based on voice type for more natural sound - 10% faster
            if (selectedVoice.name.toLowerCase().includes('samantha')) {
                utterance.rate = 0.99; // Samantha sounds best at this rate (10% faster)
                utterance.pitch = 1.0; // Natural pitch for Samantha
            } else if (selectedVoice.name.toLowerCase().includes('moira')) {
                utterance.rate = 0.88; // Irish accent needs slower pace (10% faster)
                utterance.pitch = 1.1;
            } else if (selectedVoice.name.toLowerCase().includes('zira')) {
                utterance.rate = 0.935; // Windows Zira optimization (10% faster)
                utterance.pitch = 1.05;
            }
        } else {
            console.log('🎤 Sora using default voice');
        }
        
        // Add natural pauses for longer texts
        if (text.length > 100) {
            // Insert natural pauses at sentence boundaries
            const processedText = text.replace(/([.!?])\s+/g, '$1 ... ');
            utterance.text = processedText;
        } else {
            utterance.text = text;
        }
        
        // Add emotion and emphasis for certain words
        const emotionalText = text
            .replace(/\b(amazing|fantastic|great|excellent|wonderful)\b/gi, '$& ')
            .replace(/\b(sorry|unfortunately|error)\b/gi, ' $& ')
            .replace(/!/g, '. ');
        
        utterance.text = emotionalText;
        
        // Optimize speech synthesis for faster start
        utterance.onstart = () => {
            console.log('🎤 Sora started speaking');
        };
        
        utterance.onend = () => {
            console.log('🎤 Sora finished speaking');
        };
        
        utterance.onerror = (event) => {
            console.error('🎤 Speech error:', event.error);
        };
        
        this.synthesis.speak(utterance);
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    formatTime(date) {
        return date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
}

// Initialize chat bot when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.soraChatBot = new SoraChatBot();
});

// Add some animation on page load
window.addEventListener('load', () => {
    setTimeout(() => {
        document.querySelector('.chat-button').style.animation = 'pulse-orange 2s infinite';
    }, 2000);
});

