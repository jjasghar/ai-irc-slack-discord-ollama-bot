# AI Multi-Platform Bot 🤖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/AI-Ollama-green.svg)](https://ollama.ai/)
[![IRC](https://img.shields.io/badge/Chat-IRC-orange.svg)](https://en.wikipedia.org/wiki/Internet_Relay_Chat)
[![Discord](https://img.shields.io/badge/Chat-Discord-7289da.svg)](https://discord.com/)
[![Slack](https://img.shields.io/badge/Chat-Slack-4A154B.svg)](https://slack.com/)

A powerful Python bot that connects to **IRC**, **Discord**, and **Slack** to provide AI-powered responses using local **Ollama** models. Get instant AI assistance in your favorite chat platforms!

> 🎯 **Perfect for**: Development teams, communities, and anyone who wants AI assistance directly in their chat platforms while keeping data private with local AI models.

## ✨ Features

### 🌐 Multi-Platform Support
- **IRC**: Real-time chat on networks like Libera.Chat, OFTC, EFNet
- **Discord**: Server integration with real-time responses  
- **Slack**: Socket Mode for instant responses (no polling delays!)

### 🧠 AI Integration
- **Local AI Models**: Powered by Ollama (privacy-first, runs offline)
- **Multiple Models**: Support for LLaMA, Granite, and other Ollama models
- **Intelligent Chunking**: Long responses split into readable chunks
- **Continue Feature**: Get full responses with `continue` command
- **Markdown Formatting**: Rich text formatting with bold, code blocks, and lists

### 💬 Smart Messaging
- **Direct Messages**: Private conversations with the AI
- **Public Mentions**: Responds when mentioned in channels
- **Context Awareness**: Remembers conversation context for continuations
- **Error Handling**: Graceful error recovery and user feedback

### ⚙️ Advanced Features
- **Real-time Responses**: Socket Mode for Slack, event-driven for Discord
- **Message Chunking**: Respects platform character limits (IRC: 400, Discord: 2000, Slack: 4000)
- **Continuation Support**: Smart text breaking at word boundaries
- **Rich Text Formatting**: Platform-specific markdown with bold, code, and emphasis
- **Comprehensive Logging**: Monitor all bot activity and errors
- **Easy Configuration**: Simple TOML configuration switching

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** running locally
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull an AI model
   ollama pull llama3:latest
   
   # Start Ollama service
   ollama serve
   ```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-irc-slack-discord-ollama-bot
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**
   ```bash
   cp config.toml.example config.toml
   # Edit config.toml with your platform settings
   ```
   
   > ⚠️ **Important**: Never commit `config.toml` with real tokens to version control!

5. **Run the bot**
   ```bash
   python main.py
   ```

## 📋 Platform Setup Guides

Choose your platform and follow the detailed setup guide:

| Platform | Setup Guide | Difficulty | Features |
|----------|-------------|------------|----------|
| 🔧 **IRC** | [IRC Setup Guide](docs/IRC_SETUP.md) | Easy | No tokens needed |
| 🎮 **Discord** | [Discord Setup Guide](docs/DISCORD_SETUP.md) | Medium | Rich features |
| 💼 **Slack** | [Slack Setup Guide](docs/SLACK_SETUP.md) | Medium | Socket Mode |

## ⚙️ Configuration

The bot uses a `config.toml` file for all settings:

```toml
# Choose your platform: "irc", "discord", or "slack"
platform = "irc"
bot_name = "ticobotbot"

[ollama]
base_url = "http://localhost:11434"
model = "llama3:latest"

# Platform-specific configurations
[irc]
server = "irc.libera.chat"
port = 6667
channels = ["#general"]
nickname = "ticobotbot"
realname = "AI Bot powered by Ollama"

[discord]
token = "YOUR_DISCORD_BOT_TOKEN"
# guild_id = 123456789  # Optional: restrict to specific server
channels = []  # Optional: restrict to specific channels

[slack]
token = "xoxb-your-bot-token"
app_token = "xapp-your-app-level-token"  # Required for Socket Mode
channel = "general"
```

## 💬 How to Use

### Direct Messages
Send a private message to the bot:
```
You: What is machine learning?
Bot: Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed...
```

### Channel Mentions
Mention the bot in public channels:
```
You: @ticobotbot explain quantum computing
Bot: @You: Quantum computing is a revolutionary computing paradigm that leverages quantum mechanical phenomena...
```

### Continue Feature
For long responses that get truncated:
```
Bot: Machine learning involves algorithms that can identify patterns... (say 'continue' for more)
You: continue
Bot: ...in large datasets. These algorithms improve their performance as they process more data...
```

### Rich Text Formatting
The bot automatically formats responses with platform-appropriate markdown:

**Discord Example:**
```
You: @bot explain APIs
Bot: @You: **APIs** (Application Programming Interfaces) are sets of protocols and tools for building software applications. They enable different software components to communicate with each other.

Key concepts:
• **REST**: Representational State Transfer architecture
• **GraphQL**: Query language for `APIs`
• **Authentication**: Using `JWT` tokens or `OAuth`
• **Rate limiting**: Controlling `API` usage

*Remember*: Always validate input data when building APIs!
```

**Slack Example:**
```
You: @bot explain APIs  
Bot: <@user>: *APIs* (Application Programming Interfaces) are sets of protocols and tools for building software applications. They enable different software components to communicate with each other.

Key concepts:
• *REST*: Representational State Transfer architecture
• *GraphQL*: Query language for `APIs`
• *Authentication*: Using `JWT` tokens or `OAuth`
• *Rate limiting*: Controlling `API` usage

_Remember_: Always validate input data when building APIs!
```

### Platform-Specific Commands

**Discord Only:**
- `/ping` - Check bot status
- `/models` - List available AI models

**Slack Only:**
- `/ping` - Check bot status  
- `/models` - List available AI models

## 🛠️ Development

### Project Structure
```
ai-irc-slack-discord-ollama-bot/
├── main.py              # Main orchestrator
├── config.toml          # Configuration file
├── requirements.txt     # Python dependencies
├── start_bot.sh        # Convenience startup script
├── docs/               # Platform setup guides
│   ├── IRC_SETUP.md
│   ├── DISCORD_SETUP.md
│   └── SLACK_SETUP.md
└── src/
    ├── irc_client.py       # IRC implementation
    ├── discord_client.py   # Discord implementation  
    ├── slack_client.py     # Slack implementation (Socket Mode)
    └── ollama_client.py    # AI model integration
```

### Key Features Implementation

**Message Chunking:**
- Respects platform character limits
- Breaks at word boundaries for readability
- Provides continuation commands

**Socket Mode (Slack):**
- Real-time WebSocket connection
- No polling delays or rate limits
- Event-driven message handling

**Error Handling:**
- Network disconnections and reconnections
- API rate limiting management
- Graceful error messages to users

## 🔧 Troubleshooting

### Common Issues

**Bot not responding:**
1. Check if Ollama is running: `ollama serve`
2. Verify bot tokens and permissions
3. Check bot is in the correct channels
4. Review logs for error messages

**Ollama connection failed:**
```bash
# Check Ollama status
ollama list

# Restart Ollama service
ollama serve

# Verify model is available
ollama pull llama3:latest
```

**Platform-specific issues:**
- **IRC**: Nickname conflicts, channel permissions
- **Discord**: Privileged intents, bot permissions
- **Slack**: Missing app-level token, event subscriptions

### Logging

The bot provides comprehensive logging:
- Console output for real-time monitoring
- Detailed error messages and stack traces
- Connection status and message handling logs

### Getting Help

1. Check the platform-specific setup guides in `/docs`
2. Review the troubleshooting sections
3. Check Ollama documentation for model issues
4. Verify your platform tokens and permissions

## 🌟 Advanced Usage

### Multiple Models
Switch between different AI models:
```toml
[ollama]
model = "granite3.2:latest"  # Or llama3:latest, hermes3:latest, etc.
```

### Custom Behavior
Modify the AI responses by:
- Changing the Ollama model
- Adjusting message chunking limits
- Customizing bot personality in prompts

### Production Deployment
- Use process managers like `systemd` or `pm2`
- Set up proper logging and monitoring
- Configure firewall rules for Ollama
- Use Docker for containerized deployment

## 📊 Repository Stats

- **Languages**: Python
- **Platforms**: IRC, Discord, Slack  
- **AI Backend**: Ollama (Local)
- **License**: MIT
- **Status**: Production Ready

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

Quick start for contributors:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## 🔗 Related Projects

- [Ollama](https://ollama.ai/) - Local AI model runtime
- [Slack Bolt](https://slack.dev/bolt-python/) - Slack app framework  
- [Discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [IRC Library](https://pypi.org/project/irc/) - Python IRC client

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/ai-irc-slack-discord-ollama-bot&type=Date)](https://star-history.com/#your-username/ai-irc-slack-discord-ollama-bot&Date)

---

<div align="center">

**Happy chatting with AI! 🎉**

Made with ❤️ by the open source community

[⬆ Back to Top](#ai-multi-platform-bot-)

</div>