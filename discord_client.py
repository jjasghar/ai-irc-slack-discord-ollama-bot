"""
Discord client implementation for the AI bot
"""
import discord
from discord.ext import commands
import asyncio
import logging
from ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        discord_config = config['discord']
        
        # Set up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.bot_name = config['bot_name']
        self.token = discord_config['token']
        self.guild_id = discord_config.get('guild_id', None)
        self.allowed_channels = discord_config.get('channels', [])
        
        self.ollama_client = OllamaClient(
            base_url=config['ollama']['base_url'],
            model=config['ollama']['model']
        )
        
        # Store full responses for continuation
        self.stored_responses = {}  # key: "user@channel", value: {"full_text": str, "position": int}
        
        logger.info("Discord Bot initialized")
    
    def format_for_discord(self, text):
        """Format AI response with Discord markdown"""
        if not text:
            return text
            
        formatted_text = text
        
        # Convert common patterns to Discord markdown
        import re
        
        # Bold text (wrap **important** concepts)
        formatted_text = re.sub(r'\b(AI|API|REST|GraphQL|Python|JavaScript|HTML|CSS|SQL|JSON|XML|HTTP|HTTPS|URL|URI|OAuth|JWT|SSL|TLS|TCP|UDP|IP|DNS|CPU|GPU|RAM|SSD|HDD|USB|CLI|GUI|IDE|SDK|CDN|VPN|SSH|FTP|SMTP|POP3|IMAP|CRUD|MVC|OOP|MVP|MVVM|DRY|SOLID|KISS|YAGNI)\b', r'**\1**', formatted_text)
        
        # Code blocks (wrap code examples in triple backticks)
        if '```' not in formatted_text:
            # Look for code-like patterns and wrap them
            formatted_text = re.sub(r'`([^`]+)`', r'`\1`', formatted_text)
            
            # Convert function calls and file paths to inline code
            formatted_text = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*\(\))\b', r'`\1`', formatted_text)
            formatted_text = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z]+)\b', r'`\1`', formatted_text)
        
        # Emphasis for key terms
        formatted_text = re.sub(r'\b(important|note|warning|remember|key|main|primary|essential|critical)\b', r'*\1*', formatted_text, flags=re.IGNORECASE)
        
        # Lists - Convert numbered lists to Discord format
        lines = formatted_text.split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line):
                formatted_lines.append(f"• {line[line.find('.')+1:].strip()}")
            elif line.startswith('*') or line.startswith('-'):
                formatted_lines.append(f"• {line[1:].strip()}")
            else:
                formatted_lines.append(line)
        
        formatted_text = '\n'.join(formatted_lines)
        
        return formatted_text
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        
        if self.guild_id:
            guild = discord.utils.get(self.guilds, id=self.guild_id)
            if guild:
                logger.info(f'Connected to guild: {guild.name}')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="AI questions"
            )
        )
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Handle DMs
        if isinstance(message.channel, discord.DMChannel):
            await self.handle_dm(message)
            return
        
        # Handle mentions in guild channels
        if self.user.mentioned_in(message) or self.is_mentioned(message.content):
            # Check if channel is allowed (if restriction is set)
            if self.allowed_channels and message.channel.name not in self.allowed_channels:
                return
            
            await self.handle_mention(message)
        
        # Process commands
        await self.process_commands(message)
    
    def is_mentioned(self, content):
        """Check if bot is mentioned in message content"""
        content_lower = content.lower()
        bot_name_lower = self.bot_name.lower()
        
        mentions = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"{bot_name_lower} ",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        return any(mention in content_lower for mention in mentions)
    
    def clean_message(self, content):
        """Remove bot mentions and clean up the message"""
        # Remove Discord mentions
        clean_content = content
        # Check if user ID is in the content (mentions)
        if f'<@{self.user.id}>' in content or f'<@!{self.user.id}>' in content:
            clean_content = clean_content.replace(f'<@{self.user.id}>', '')
            clean_content = clean_content.replace(f'<@!{self.user.id}>', '')
        
        # Remove text mentions
        content_lower = content.lower()
        bot_name_lower = self.bot_name.lower()
        
        patterns_to_remove = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        for pattern in patterns_to_remove:
            clean_content = clean_content.replace(pattern, "", 1)
            clean_content = clean_content.replace(pattern.title(), "", 1)
            clean_content = clean_content.replace(pattern.upper(), "", 1)
        
        return clean_content.strip()
    
    async def handle_dm(self, message):
        """Handle direct messages"""
        user = message.author
        content = message.content.strip()
        
        logger.info(f"DM from {user}: {content}")
        
        # Check for continue command
        if content.lower() in ['continue', 'cont', 'more']:
            await self.handle_continue(message, user.name, user.name)  # DM context
            return
        
        # Generate AI response
        try:
            full_response = self.ollama_client.generate_full_response(content)
            formatted_response = self.format_for_discord(full_response)
            chunked_response = self.get_first_chunk(formatted_response, user.name, user.name)
            await message.channel.send(chunked_response)
            logger.info(f"Sent DM response to {user}")
        except Exception as e:
            logger.error(f"Error handling DM: {e}")
            await message.channel.send("Sorry, I encountered an error processing your message.")
    
    async def handle_mention(self, message):
        """Handle mentions in channels"""
        user = message.author
        content = self.clean_message(message.content)
        channel = message.channel
        
        # Check if the cleaned message is a continue command
        if content.lower().strip() in ['continue', 'cont', 'more']:
            logger.info(f"Continue command from {user} in {channel}")
            await self.handle_continue(message, user.name, channel.name)
            return
        
        logger.info(f"Mentioned in {channel} by {user}: {content}")
        
        # Generate AI response
        try:
            full_response = self.ollama_client.generate_full_response(content)
            formatted_response = self.format_for_discord(full_response)
            chunked_response = self.get_first_chunk(formatted_response, user.name, channel.name)
            await message.channel.send(f"{user.mention}: {chunked_response}")
            logger.info(f"Sent mention response in {channel}")
        except Exception as e:
            logger.error(f"Error handling mention: {e}")
            await message.channel.send(f"{user.mention}: Sorry, I encountered an error processing your message.")
    
    def get_first_chunk(self, full_text, user, context):
        """Get the first chunk of text and store the rest for continuation"""
        key = f"{user}@{context}"
        
        # Preserve markdown formatting - don't collapse newlines
        clean_text = full_text.replace('\r\n', '\n').replace('\r', '\n')
        # Only normalize excessive whitespace within lines
        lines = clean_text.split('\n')
        clean_lines = [' '.join(line.split()) for line in lines]
        clean_text = '\n'.join(clean_lines)
        
        # Reserve space for the continuation message
        continuation_msg = " (say 'continue' for more)"
        max_content_length = 1800 - len(continuation_msg)  # Discord has 2000 char limit
        
        if len(clean_text) <= max_content_length:
            # Text fits in one message, no need to store
            if key in self.stored_responses:
                del self.stored_responses[key]
            return clean_text
        
        # Find a good break point (prefer ending at word boundary)
        chunk_end = max_content_length - 3  # Reserve space for "..."
        
        # Try to break at a word boundary
        space_pos = clean_text.rfind(' ', 0, chunk_end)
        if space_pos > chunk_end - 50:  # Only use word boundary if it's not too far back
            chunk_end = space_pos
        
        # Store full text for continuation
        self.stored_responses[key] = {
            "full_text": clean_text,
            "position": chunk_end
        }
        
        # Return first chunk with continuation indicator
        first_chunk = clean_text[:chunk_end] + "..."
        return f"{first_chunk}{continuation_msg}"
    
    async def handle_continue(self, message, user, context):
        """Handle continue requests"""
        key = f"{user}@{context}"
        
        if key not in self.stored_responses:
            response = "No previous message to continue."
        else:
            stored = self.stored_responses[key]
            full_text = stored["full_text"]
            start_pos = stored["position"]
            
            if start_pos >= len(full_text):
                response = "End of message reached."
                del self.stored_responses[key]
            else:
                # Get next chunk
                remaining_text = full_text[start_pos:]
                continuation_msg = " (say 'continue' for more)"
                max_content_length = 1800 - len(continuation_msg)
                
                if len(remaining_text) <= max_content_length:
                    # This is the last chunk
                    response = remaining_text
                    del self.stored_responses[key]
                else:
                    # More chunks remain - find good break point
                    chunk_end = max_content_length - 3  # Reserve space for "..."
                    
                    # Try to break at word boundary
                    space_pos = remaining_text.rfind(' ', 0, chunk_end)
                    if space_pos > chunk_end - 50:  # Only use word boundary if it's not too far back
                        chunk_end = space_pos
                    
                    chunk = remaining_text[:chunk_end] + "..."
                    self.stored_responses[key]["position"] = start_pos + chunk_end
                    response = f"{chunk}{continuation_msg}"
        
        # Send continuation response
        if context == user:  # DM
            await message.channel.send(response)
        else:  # Channel
            await message.channel.send(f"{message.author.mention}: {response}")
        
        logger.info(f"Sent continuation to {user} in {context}")
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Simple ping command"""
        await ctx.send('Pong! AI bot is online.')
    
    @commands.command(name='models')
    async def list_models(self, ctx):
        """List available AI models"""
        models = self.ollama_client.list_models()
        if models:
            model_list = "\\n".join(models)
            await ctx.send(f"Available models:\\n```\\n{model_list}\\n```")
        else:
            await ctx.send("No models available or AI service is down.")
    
    async def start_bot(self):
        """Start the Discord bot"""
        try:
            logger.info("Starting Discord bot...")
            await self.start(self.token)
        except Exception as e:
            logger.error(f"Error starting Discord bot: {e}")
            raise

async def run_discord_bot(config):
    """Function to run the Discord bot"""
    bot = DiscordBot(config)
    await bot.start_bot()