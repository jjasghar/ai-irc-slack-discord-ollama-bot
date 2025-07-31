# Contributing to AI Multi-Platform Bot

Thank you for your interest in contributing to the AI Multi-Platform Bot! We welcome contributions from everyone.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/ai-irc-slack-discord-ollama-bot.git
   cd ai-irc-slack-discord-ollama-bot
   ```

3. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create configuration**
   ```bash
   cp config.toml.example config.toml
   # Edit config.toml with your settings
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing
- Test your changes on all supported platforms (IRC, Discord, Slack)
- Ensure the bot starts without errors
- Test both public mentions and private messages
- Verify the `continue` feature works correctly

### Platform-Specific Guidelines

**IRC Testing:**
- Use test channels like `#bots` or create your own
- Test on libera.chat or another network you have access to

**Discord Testing:**
- Create a test server for development
- Enable necessary privileged intents in Discord Developer Portal
- Test both server channels and DMs

**Slack Testing:**
- Use a development workspace
- Test both Socket Mode and legacy polling if applicable
- Verify slash commands work

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Test thoroughly on relevant platforms

3. **Update documentation**
   - Update README.md if you add new features
   - Update platform-specific docs in `/docs` if needed
   - Add comments to complex code

4. **Submit pull request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include testing notes

## 🐛 Bug Reports

When reporting bugs, please include:

- **Platform**: IRC, Discord, or Slack
- **Python version**: `python --version`
- **Operating system**: Windows, macOS, Linux
- **Error logs**: Include relevant log output
- **Steps to reproduce**: Clear reproduction steps
- **Expected vs actual behavior**

## 💡 Feature Requests

We welcome feature requests! Please:

- Check existing issues first
- Describe the use case clearly
- Explain how it would benefit users
- Consider implementation complexity

## 🏗️ Architecture

### Project Structure
```
ai-irc-slack-discord-ollama-bot/
├── main.py              # Entry point and orchestration
├── config.toml.example  # Configuration template
├── requirements.txt     # Python dependencies
├── docs/               # Platform-specific setup guides
├── irc_client.py       # IRC implementation
├── discord_client.py   # Discord implementation
├── slack_client.py     # Slack implementation (Socket Mode)
└── ollama_client.py    # AI model integration
```

### Key Components

**Client Architecture:**
- Each platform has its own client class
- Common interface for message handling
- Platform-specific formatting and features

**Message Processing:**
- AI responses are generated via Ollama
- Responses are chunked to respect platform limits
- Continuation feature for long responses

**Configuration:**
- TOML-based configuration
- Platform-specific settings
- Environment variable support possible

## 🧪 Testing Checklist

Before submitting a PR, ensure:

- [ ] Bot starts without errors
- [ ] Configuration validation works
- [ ] AI responses are generated correctly
- [ ] Message chunking works (test with long responses)
- [ ] Continue feature works (`continue`, `cont`, `more`)
- [ ] Platform-specific formatting is applied
- [ ] Error handling works gracefully
- [ ] No sensitive information in commits

## 🔐 Security

- **Never commit tokens or credentials**
- **Use config.toml.example for examples**
- **Sanitize logs of sensitive information**
- **Follow platform security best practices**

## 📚 Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Slack Bolt Documentation](https://slack.dev/bolt-python/)
- [IRC Protocol RFC](https://tools.ietf.org/html/rfc1459)

## 🤝 Community

- Be respectful and inclusive
- Help newcomers get started
- Share knowledge and best practices
- Have fun building cool AI chat bots!

Thank you for contributing! 🎉