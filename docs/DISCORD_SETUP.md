# Discord Bot Setup Guide

This guide covers setting up the AI bot for Discord servers.

## Prerequisites

- Discord account
- Server admin permissions (to invite bots)
- Discord Developer Portal access

## Step 1: Create Discord Application

1. **Go to Discord Developer Portal**: https://discord.com/developers/applications
2. **Click "New Application"**
3. **Name your application**: e.g., "AI Ollama Bot"
4. **Click "Create"**

## Step 2: Create Bot User

1. **In the left sidebar, click "Bot"**
2. **Click "Add Bot"**
3. **Confirm**: "Yes, do it!"
4. **Customize your bot**:
   - Upload an avatar (optional)
   - Set username
   - Add description

## Step 3: Configure Bot Permissions

1. **In left sidebar: "OAuth2" → "URL Generator"**
2. **Under "Scopes", check**: `bot`
3. **Under "Bot Permissions", select**:
   - ✅ `Send Messages`
   - ✅ `Read Message History`
   - ✅ `Use Slash Commands` (optional)
   - ✅ `Add Reactions` (optional)
   - ✅ `Embed Links` (optional)

## Step 4: Enable Privileged Intents

**⚠️ IMPORTANT**: Your bot needs privileged intents to read message content.

1. **Go back to "Bot" section**
2. **Scroll down to "Privileged Gateway Intents"**
3. **Enable these toggles**:
   - ✅ **Message Content Intent** (required)
   - ✅ **Server Members Intent** (optional)
   - ✅ **Presence Intent** (optional)
4. **Click "Save Changes"**

## Step 5: Get Bot Token

1. **In "Bot" section, under "Token"**
2. **Click "Copy"** to copy your bot token
3. **⚠️ Keep this token secret!** Don't share it publicly

## Step 6: Invite Bot to Server

1. **Copy the generated URL** from OAuth2 URL Generator
2. **Open URL in new tab**
3. **Select your Discord server**
4. **Click "Authorize"**
5. **Complete captcha if prompted**

## Step 7: Configure Bot

Edit `config.toml`:

```toml
platform = "discord"
bot_name = "ticobotbot"

[ollama]
base_url = "http://localhost:11434"
model = "llama3:latest"

[discord]
token = "YOUR_DISCORD_BOT_TOKEN_HERE"
# guild_id = 123456789  # Optional: restrict to specific server
channels = []  # Optional: restrict to specific channels
```

## Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `token` | Your Discord bot token | `"MTQwMDU1Njk..."` |
| `guild_id` | Restrict to specific server (optional) | `123456789` |
| `channels` | Restrict to specific channels (optional) | `["general", "ai-chat"]` |

## Usage

### Server Interaction
- **Mention the bot**: `@YourBot what is artificial intelligence?`
- **Ask questions**: `@YourBot explain Python programming`
- **Get help**: `@YourBot how do I learn to code?`

### Direct Messages
- **Send a DM** to the bot directly
- No need to mention the bot in DMs

### Continue Feature
For long responses:
```
@YourBot what is machine learning?
Bot: Machine learning is a subset of artificial intelligence that enables computers to learn... (say 'continue' for more)
You: continue
Bot: ...from data without being explicitly programmed. It involves algorithms that can identify patterns...
```

### Slash Commands
- `/ping` - Check if bot is online
- `/models` - List available AI models

## Troubleshooting

### Bot Not Responding to Mentions

**Check Privileged Intents**:
1. Go to Discord Developer Portal
2. Select your app → "Bot"
3. Enable "Message Content Intent"
4. Restart your bot

### Permission Errors

**Ensure bot has permissions**:
- Send Messages
- Read Message History
- Use Slash Commands

**Check channel permissions**:
- Bot must be able to see and send in the channel
- Some channels may restrict bots

### Bot Appears Offline

**Check token**:
- Verify token is correct and complete
- Token should start with `MTQ...` or similar
- Don't include quotes in the actual token

**Check internet connection**:
- Ensure bot can reach Discord servers
- Check firewall settings

### Rate Limiting

Discord has rate limits:
- **Message sending**: 5 messages per 5 seconds per channel
- **Bot mentions**: Higher limits for bot accounts
- **API calls**: Various limits depending on endpoint

## Advanced Configuration

### Restrict to Specific Server
```toml
[discord]
token = "your-token"
guild_id = 123456789  # Your server's ID
```

### Restrict to Specific Channels
```toml
[discord]
token = "your-token"
channels = ["ai-chat", "general", "bots"]
```

### Server ID and Channel Names
To find server/channel IDs:
1. Enable Developer Mode in Discord settings
2. Right-click server/channel → "Copy ID"

## Best Practices

1. **Clear bot purpose** - Make it obvious it's an AI bot
2. **Appropriate channels** - Use dedicated bot/AI channels when possible
3. **Respect rate limits** - Don't spam requests
4. **Monitor usage** - Keep track of bot activity
5. **Follow Discord ToS** - Ensure compliance with Discord's terms
6. **Secure your token** - Never commit tokens to public repositories

## Example Session

```
User: @AIBot what's the difference between machine learning and deep learning?

AIBot: @User Machine learning is a broad field of artificial intelligence that enables computers to learn from data without explicit programming. Deep learning is a specialized subset of machine learning that uses neural networks with multiple layers... (say 'continue' for more)

User: continue

AIBot: @User ...to automatically learn complex patterns in data. While traditional machine learning often requires manual feature engineering, deep learning can automatically discover features from raw data...
```

## Security Considerations

- **Token security**: Keep your bot token private and secure
- **Message content**: Bot can read all messages in servers it's in
- **Data privacy**: Consider what data the AI model processes
- **Permissions**: Only grant necessary permissions
- **Monitoring**: Keep logs of bot activity for security auditing