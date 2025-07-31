# IRC Bot Setup Guide

This guide covers setting up the AI bot for IRC networks like libera.chat.

## Quick Start

IRC is the simplest platform to get started with - no tokens or special setup required!

## Configuration

Edit `config.toml`:

```toml
platform = "irc"
bot_name = "ticobotbot"

[ollama]
base_url = "http://localhost:11434"
model = "llama3:latest"

[irc]
server = "irc.libera.chat"
port = 6667
channels = ["#jj-testing"]
nickname = "ticobotbot"
realname = "AI Bot powered by Ollama"
```

## Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `server` | IRC server hostname | `"irc.libera.chat"` |
| `port` | IRC server port | `6667` (standard), `6697` (SSL) |
| `channels` | List of channels to join | `["#general", "#bots"]` |
| `nickname` | Bot's IRC nickname | `"myaibot"` |
| `realname` | Bot's real name field | `"AI Assistant"` |

## Popular IRC Networks

| Network | Server | Port | Notes |
|---------|--------|------|-------|
| Libera.Chat | `irc.libera.chat` | 6667/6697 | FOSS projects |
| OFTC | `irc.oftc.net` | 6667/6697 | Open source |
| EFNet | `irc.efnet.org` | 6667 | One of the oldest |
| Freenode | `chat.freenode.net` | 6667/6697 | Various topics |

## Usage

### Public Channel Interaction
- **Mention the bot**: `ticobotbot: what is Python?`
- **Ask questions**: `ticobotbot, explain machine learning`
- **Get help**: `ticobotbot: how do I code in JavaScript?`

### Private Messages
- Send a direct message to the bot: `/msg ticobotbot Hello!`
- The bot will respond privately

### Continue Feature
When responses are long, the bot will truncate them:
```
<ticobotbot> jjasghar: Machine learning is a subset of artificial intelligence... (say 'continue' for more)
<jjasghan> continue
<ticobotbot> jjasghar: ...that enables computers to learn and improve from experience...
```

## Troubleshooting

### Bot Won't Connect
- Check server hostname and port
- Verify your internet connection
- Some networks may require registration

### Nickname Already in Use
- Change the `nickname` in config.toml
- Use a unique name like `mybot123`

### Bot Not Responding
- Ensure you're mentioning the correct nickname
- Check that the bot has joined the channel
- Verify the bot is online (should appear in user list)

### Permission Issues
- Some channels may be invite-only
- Ask channel operators to invite your bot
- Check channel modes and requirements

## Advanced Configuration

### SSL Connection
```toml
[irc]
server = "irc.libera.chat"
port = 6697  # SSL port
# Note: SSL support may require additional configuration
```

### Multiple Channels
```toml
[irc]
channels = ["#general", "#bots", "#ai", "#coding"]
```

### Custom Bot Behavior
The bot responds to:
- Direct mentions: `botname: question`
- Name patterns: `botname, question` or `botname question`
- Private messages automatically

## Best Practices

1. **Choose appropriate channels** - Ask permission before adding to busy channels
2. **Use clear nicknames** - Make it obvious it's a bot
3. **Be respectful** - Follow channel rules and etiquette
4. **Monitor usage** - Keep an eye on bot activity and responses
5. **Test in quiet channels** - Use test channels like `#bots` for initial testing

## Example Session

```
12:34 <jjasghar> ticobotbot: what is the difference between Python and JavaScript?
12:34 <ticobotbot> jjasghar: Python and JavaScript are both popular programming languages, but they serve different purposes. Python is primarily used for... (say 'continue' for more)
12:35 <jjasghar> continue
12:35 <ticobotbot> jjasghar: ...server-side development, data science, and automation, while JavaScript is mainly used for web development...
```

## Security Notes

- IRC connections are typically unencrypted (except on SSL ports)
- Bot conversations are public in channels
- Private messages are more secure but still transmitted over IRC
- Consider the sensitivity of information being processed by the AI model