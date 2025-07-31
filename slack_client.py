"""
Slack client implementation for the AI bot using Socket Mode
"""
import logging
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self, config):
        self.config = config
        slack_config = config['slack']
        
        self.bot_name = config['bot_name']
        self.token = slack_config['token']
        self.app_token = slack_config['app_token']
        self.channel = slack_config.get('channel', 'general')
        
        # Initialize Slack Bolt app
        self.app = App(token=self.token)
        
        self.ollama_client = OllamaClient(
            base_url=config['ollama']['base_url'],
            model=config['ollama']['model']
        )
        
        # Store full responses for continuation
        self.stored_responses = {}  # key: "user@channel", value: {"full_text": str, "position": int}
        
        # Event deduplication - store recent event IDs to prevent duplicates
        self.processed_events = set()  # Store recent event IDs
        
        # Get bot user ID
        self.bot_user_id = None
        self._get_bot_user_id()
        
        # Register event handlers
        self._register_handlers()
        
        logger.info("Slack Bot initialized with Socket Mode")
    
    def format_for_slack(self, text):
        """Format AI response with Slack markdown"""
        if not text:
            return text
            
        formatted_text = text
        
        # Convert common patterns to Slack markdown
        import re
        
        # Bold text (wrap *important* concepts in Slack format)
        formatted_text = re.sub(r'\b(AI|API|REST|GraphQL|Python|JavaScript|HTML|CSS|SQL|JSON|XML|HTTP|HTTPS|URL|URI|OAuth|JWT|SSL|TLS|TCP|UDP|IP|DNS|CPU|GPU|RAM|SSD|HDD|USB|CLI|GUI|IDE|SDK|CDN|VPN|SSH|FTP|SMTP|POP3|IMAP|CRUD|MVC|OOP|MVP|MVVM|DRY|SOLID|KISS|YAGNI)\b', r'*\1*', formatted_text)
        
        # Code blocks (wrap code examples in backticks)
        if '```' not in formatted_text:
            # Look for code-like patterns and wrap them
            formatted_text = re.sub(r'`([^`]+)`', r'`\1`', formatted_text)
            
            # Convert function calls and file paths to inline code
            formatted_text = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*\(\))\b', r'`\1`', formatted_text)
            formatted_text = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z]+)\b', r'`\1`', formatted_text)
        
        # Emphasis for key terms (use _italic_ in Slack)
        formatted_text = re.sub(r'\b(important|note|warning|remember|key|main|primary|essential|critical)\b', r'_\1_', formatted_text, flags=re.IGNORECASE)
        
        # Lists - Convert numbered lists to Slack format
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
    
    def _get_bot_user_id(self):
        """Get the bot's user ID from Slack"""
        try:
            response = self.app.client.auth_test()
            if response["ok"]:
                self.bot_user_id = response["user_id"]
                logger.info(f"Bot user ID: {self.bot_user_id}")
            else:
                logger.error("Failed to get bot user ID")
        except Exception as e:
            logger.error(f"Error getting bot user ID: {e}")
    
    def _register_handlers(self):
        """Register Slack event handlers"""
        
        # Handle app mentions (when bot is mentioned in channels)
        @self.app.event("app_mention")
        def handle_app_mention(event, say, logger):
            # Create unique event ID for deduplication
            event_id = f"{event.get('ts')}:{event.get('user')}:{event.get('channel')}"
            
            logger.info(f"App mention received - Event ID: {event_id}")
            logger.info(f"App mention details: {event}")
            
            # Check for duplicate events
            if event_id in self.processed_events:
                logger.warning(f"Duplicate app mention event detected and skipped: {event_id}")
                return
            
            # Add to processed events (keep last 100 to prevent memory growth)
            self.processed_events.add(event_id)
            if len(self.processed_events) > 100:
                # Remove oldest events (convert to list, remove first 50, convert back)
                event_list = list(self.processed_events)
                self.processed_events = set(event_list[50:])
            
            logger.info(f"Processing app mention: {event_id}")
            self.handle_mention(event, say)
        
        # Handle direct messages
        @self.app.event("message")
        def handle_message_events(event, say, logger):
            # Skip if this is a subtype (like bot_message, message_changed, etc.)
            if event.get("subtype"):
                logger.debug(f"Skipping message subtype: {event.get('subtype')}")
                return
            
            # Skip if this message contains bot mentions (handled by app_mention event)
            text = event.get("text", "")
            if self.bot_user_id and f"<@{self.bot_user_id}>" in text:
                logger.debug(f"Skipping message with bot mention - handled by app_mention: {text}")
                return
                
            # Only handle direct messages (channel type is 'im')
            if event.get("channel_type") == "im":
                # Create unique event ID for deduplication
                event_id = f"{event.get('ts')}:{event.get('user')}:{event.get('channel')}"
                
                logger.info(f"Direct message received - Event ID: {event_id}")
                
                # Check for duplicate events
                if event_id in self.processed_events:
                    logger.warning(f"Duplicate DM event detected and skipped: {event_id}")
                    return
                
                # Add to processed events
                self.processed_events.add(event_id)
                if len(self.processed_events) > 100:
                    event_list = list(self.processed_events)
                    self.processed_events = set(event_list[50:])
                
                logger.info(f"Processing direct message: {event_id}")
                logger.info(f"DM details: {event}")
                self.handle_dm(event, say)
            else:
                logger.debug(f"Skipping non-DM message in channel {event.get('channel')}")
        
        # Handle slash commands (optional)
        @self.app.command("/ping")
        def handle_ping_command(ack, respond):
            ack()
            respond("🤖 Pong! I'm online and ready to help!")
        
        @self.app.command("/models")
        def handle_models_command(ack, respond):
            ack()
            try:
                models = self.ollama_client.get_available_models()
                model_list = "\n".join([f"• {model}" for model in models])
                respond(f"Available AI models:\n{model_list}")
            except Exception as e:
                respond(f"Error getting models: {e}")
    
    def is_mentioned(self, text):
        """Check if bot is mentioned in the message"""
        if not text:
            return False
        
        text_lower = text.lower()
        bot_name_lower = self.bot_name.lower()
        
        # Check for user ID mention
        if self.bot_user_id and f"<@{self.bot_user_id}>" in text:
            return True
        
        # Check for name mentions
        mentions = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"{bot_name_lower} ",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        return any(mention in text_lower for mention in mentions)
    
    def clean_message(self, text):
        """Remove bot mentions and clean up the message"""
        if not text:
            return ""
        
        clean_text = text
        
        # Remove user ID mention
        if self.bot_user_id:
            clean_text = re.sub(f"<@{self.bot_user_id}>", "", clean_text)
        
        # Remove text mentions
        text_lower = text.lower()
        bot_name_lower = self.bot_name.lower()
        
        patterns_to_remove = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        for pattern in patterns_to_remove:
            clean_text = re.sub(pattern, "", clean_text, flags=re.IGNORECASE)
        
        return clean_text.strip()
    
    def handle_dm(self, event, say):
        """Handle direct messages"""
        user = event.get("user")
        text = event.get("text", "")
        
        # Skip bot messages
        if user == self.bot_user_id:
            return
        
        logger.info(f"DM from {user}: {text}")
        
        # Check for continue command
        if text.lower().strip() in ['continue', 'cont', 'more']:
            self.handle_continue(say, user, user)  # DM context
            return
        
        try:
            # Generate AI response
            full_response = self.ollama_client.generate_full_response(text)
            formatted_response = self.format_for_slack(full_response)
            chunked_response = self.get_first_chunk(formatted_response, user, user)
            
            # Send response
            say(chunked_response)
            
            logger.info(f"Sent DM response to {user}")
        
        except Exception as e:
            logger.error(f"Error handling DM: {e}")
            say("Sorry, I encountered an error processing your message.")
    
    def handle_mention(self, event, say):
        """Handle mentions in channels"""
        user = event.get("user")
        text = event.get("text", "")
        channel = event.get("channel")
        
        # Skip bot messages
        if user == self.bot_user_id:
            return
        
        clean_text = self.clean_message(text)
        
        # Check if the cleaned message is a continue command
        if clean_text.lower().strip() in ['continue', 'cont', 'more']:
            logger.info(f"Continue command from {user} in {channel}")
            self.handle_continue(say, user, channel)
            return
        
        logger.info(f"Mentioned in {channel} by {user}: {clean_text}")
        
        try:
            # Generate AI response
            full_response = self.ollama_client.generate_full_response(clean_text)
            formatted_response = self.format_for_slack(full_response)
            chunked_response = self.get_first_chunk(formatted_response, user, channel)
            
            # Send response with user mention
            say(f"<@{user}>: {chunked_response}")
            
            logger.info(f"Sent mention response in {channel}")
        
        except Exception as e:
            logger.error(f"Error handling mention: {e}")
            say(f"<@{user}>: Sorry, I encountered an error processing your message.")
    
    def get_first_chunk(self, full_text, user, context):
        """Get the first chunk of text and store the rest for continuation"""
        key = f"{user}@{context}"
        
        # Preserve markdown formatting - don't collapse newlines completely
        clean_text = full_text.replace('\r\n', '\n').replace('\r', '\n')
        # Only normalize excessive whitespace within lines
        lines = clean_text.split('\n')
        clean_lines = [' '.join(line.split()) for line in lines]
        clean_text = '\n'.join(clean_lines)
        
        # Reserve space for the continuation message
        continuation_msg = " (say 'continue' for more)"
        max_content_length = 3800 - len(continuation_msg)  # Slack has 4000 char limit
        
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
    
    def handle_continue(self, say, user, context):
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
                max_content_length = 3800 - len(continuation_msg)
                
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
            say(response)
        else:  # Channel
            say(f"<@{user}>: {response}")
        
        logger.info(f"Sent continuation to {user} in {context}")
    
    def start_bot(self):
        """Start the Slack bot with Socket Mode"""
        try:
            logger.info("Starting Slack bot with Socket Mode...")
            
            # Test connection
            response = self.app.client.auth_test()
            if not response["ok"]:
                raise Exception("Failed to authenticate with Slack")
            
            logger.info("Successfully connected to Slack")
            
            # Start Socket Mode handler
            handler = SocketModeHandler(self.app, self.app_token)
            logger.info("Socket Mode handler started - bot is now running in real-time!")
            handler.start()
            
        except Exception as e:
            logger.error(f"Error starting Slack bot: {e}")
            raise

def run_slack_bot(config):
    """Function to run the Slack bot"""
    bot = SlackBot(config)
    bot.start_bot()