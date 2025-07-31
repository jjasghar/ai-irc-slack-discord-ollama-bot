# Slack Bot Setup Guide

This guide covers setting up the AI bot for Slack workspaces using Socket Mode for real-time responses.

## Prerequisites

- Slack workspace admin permissions
- Slack account with app creation rights

## Step 1: Create Slack App

1. **Go to Slack API Portal**: https://api.slack.com/apps
2. **Click "Create New App"**
3. **Choose "From scratch"**
4. **App Info**:
   - **App Name**: e.g., "AI Ollama Bot"
   - **Workspace**: Select your workspace
5. **Click "Create App"**

## Step 2: Enable Socket Mode

1. **In left sidebar: "Socket Mode"**
2. **Toggle "Enable Socket Mode" to ON**
3. **Click "Generate" to create an App-Level Token**
4. **Name**: "Socket Mode Token"
5. **Scopes**: Should automatically include `connections:write`
6. **Click "Generate"**
7. **Copy the App-Level Token** (starts with `xapp-`) - you'll need this later

## Step 3: Configure Bot Token Scopes

1. **In left sidebar: "OAuth & Permissions"**
2. **Scroll to "Scopes" → "Bot Token Scopes"**
3. **Add these scopes**:

### Required Scopes
- ✅ `app_mentions:read` - Listen for mentions of your app
- ✅ `chat:write` - Send messages as the bot
- ✅ `im:history` - Read direct messages
- ✅ `im:read` - View basic info about direct messages

### Optional Scopes for Enhanced Features
- `channels:history` - Read public channel messages
- `groups:history` - Read private channel messages
- `mpim:history` - Read group direct messages
- `channels:read` - View basic info about public channels
- `groups:read` - View basic info about private channels
- `users:read` - View people in workspace
- `commands` - Add slash commands

## Step 4: Configure Event Subscriptions

1. **In left sidebar: "Event Subscriptions"**
2. **Toggle "Enable Events" to ON**
3. **Under "Subscribe to bot events", add**:
   - ✅ `app_mention` - Listen for mentions
   - ✅ `message.im` - Listen for direct messages

## Step 5: Install Bot to Workspace

1. **Go back to "OAuth & Permissions" page**
2. **Click "Install to Workspace"**
3. **Review permissions and click "Allow"**
4. **Copy the "Bot User OAuth Token"** (starts with `xoxb-`)

## Step 4: Add Bot to Channels

### Method 1: Slash Command
In any channel:
```
/invite @your-bot-name
```

### Method 2: Channel Settings
1. **Go to channel settings**
2. **Integrations tab**
3. **Add apps**
4. **Select your bot**

## Step 6: Configure Bot

Edit `config.toml`:

```toml
platform = "slack"
bot_name = "ticobotbot"

[ollama]
base_url = "http://localhost:11434"
model = "granite3.2:latest"

[slack]
token = "xoxb-your-slack-bot-token-here"
app_token = "xapp-your-app-level-token-here"
channel = "general"
```

## Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `token` | Your Slack bot token | `"xoxb-1234567890..."` |
| `app_token` | Your app-level token for Socket Mode | `"xapp-1234567890..."` |
| `channel` | Primary channel preference | `"general"` |

**Important**: You need both tokens for Socket Mode to work:
- **Bot Token** (`xoxb-`): For sending messages and API calls
- **App-Level Token** (`xapp-`): For Socket Mode real-time connection

## Usage

### Channel Interaction
- **Mention the bot**: `@YourBot what is artificial intelligence?`
- **Ask questions**: `@YourBot explain machine learning`
- **Get help**: `@YourBot how do I code in Python?`

### Direct Messages
- **Send a DM** to the bot directly
- No need to mention the bot in DMs

### Slash Commands (Optional)
- `/ping` - Check if bot is online
- `/models` - List available AI models

### Continue Feature
For long responses:
```
@YourBot what is deep learning?
Bot: Deep learning is a subset of machine learning that uses neural networks with multiple layers... (say 'continue' for more)
You: continue
Bot: ...to automatically learn complex patterns in data. These networks are inspired by the human brain...
```

## Troubleshooting

### Bot Not Responding

**Check bot is in channel**:
```
/invite @your-bot-name
```

**Verify token**:
- Token should start with `xoxb-`
- Copy the complete token
- Don't include quotes around the actual token

**Check permissions**:
- Ensure bot has required scopes
- Verify workspace installation

### Bot Not Receiving Mentions

**Check Event Subscriptions**:
1. Go to Slack API portal
2. Select your app → "Event Subscriptions"
3. Ensure `app_mention` and `message.im` are subscribed

**Verify Socket Mode**:
1. Check that Socket Mode is enabled
2. Ensure app-level token is correct
3. Restart the bot

### Missing App-Level Token

```
Error: App-level token required for Socket Mode
```

**Solution**:
1. Go to Slack API portal → "Socket Mode"
2. Generate new App-Level Token
3. Copy token (starts with `xapp-`)
4. Update `config.toml` with the token

### Permission Errors

**Missing scopes**:
1. Go to Slack API portal
2. Select your app
3. "OAuth & Permissions" → "Scopes"
4. Add missing scopes
5. Reinstall to workspace

## Advanced Configuration

### Slash Commands (Optional)

1. **In left sidebar: "Slash Commands"**
2. **Click "Create New Command"**
3. **Add commands**:
   - Command: `/ping`, Description: "Check bot status"
   - Command: `/models`, Description: "List AI models"

### Multiple Workspaces

To use across multiple workspaces:
1. Create separate app for each workspace
2. Or distribute app through Slack App Directory

### Custom Bot Appearance

1. **Go to "Basic Information"**
2. **Display Information**:
   - Upload bot avatar
   - Set display name
   - Add description
   - Choose background color

## Best Practices

1. **Clear bot identity** - Make it obvious it's an AI assistant
2. **Appropriate channels** - Use dedicated AI/bot channels when possible
3. **Respect workspace culture** - Follow team communication norms
4. **Monitor usage** - Keep track of bot interactions
5. **Data privacy** - Be mindful of sensitive information in conversations
6. **Real-time responses** - Socket Mode provides instant responses

## Example Session

```
User: @AIBot explain the difference between REST and GraphQL APIs

AIBot: <@User>: REST and GraphQL are both API architectural styles, but they handle data fetching differently. REST uses multiple endpoints with fixed data structures, while GraphQL uses a single endpoint... (say 'continue' for more)

User: continue

AIBot: <@User>: ...where clients can request exactly the data they need. GraphQL provides more flexibility and efficiency by allowing clients to specify precisely which fields they want...
```

## Security Considerations

- **Token security**: Keep bot token private and secure
- **Workspace access**: Bot can read messages in channels it's added to
- **Data handling**: Consider privacy of conversations processed by AI
- **Audit logs**: Slack provides audit logs for bot activity
- **Permissions**: Only grant minimum necessary scopes

## Socket Mode Benefits

### Real-time Features
- **Instant responses**: No polling delays
- **Event-driven**: Responds immediately to mentions and DMs
- **No rate limits**: Socket Mode has higher rate limits than polling
- **Reliable**: Persistent WebSocket connection

### Performance Improvements
- **Lower latency**: Real-time event processing
- **Better user experience**: Immediate feedback
- **Reduced API calls**: No continuous polling
- **Scalable**: Can handle high message volumes

## Token Security

**Bot Token (`xoxb-`)**:
- Keep private and secure
- Used for API calls and sending messages
- Has workspace-level permissions

**App-Level Token (`xapp-`)**:
- Required for Socket Mode connection
- Keep separate from bot token
- Has app-level permissions for real-time events