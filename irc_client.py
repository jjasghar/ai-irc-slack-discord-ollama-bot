"""
IRC client implementation for the AI bot
"""
import irc.bot
import irc.strings
import threading
import logging
from ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        self.config = config
        irc_config = config['irc']
        
        # Initialize IRC connection
        server = irc_config['server']
        port = irc_config['port']
        nickname = irc_config['nickname']
        
        super().__init__([(server, port)], nickname, nickname)
        
        self.channel_list = irc_config['channels']
        self.bot_name = config['bot_name']
        self.ollama_client = OllamaClient(
            base_url=config['ollama']['base_url'],
            model=config['ollama']['model']
        )
        
        # Store full responses for continuation
        self.stored_responses = {}  # key: "user@channel", value: {"full_text": str, "position": int}
        
        logger.info(f"IRC Bot initialized for {server}:{port} as {nickname}")
    
    def on_welcome(self, connection, event):
        """Called when bot successfully connects to IRC server"""
        logger.info("Connected to IRC server")
        for channel in self.channel_list:
            connection.join(channel)
            logger.info(f"Joined channel: {channel}")
    
    def on_privmsg(self, connection, event):
        """Handle private messages"""
        sender = event.source.nick
        message = event.arguments[0].strip() if event.arguments else ""
        
        logger.info(f"Private message from {sender}: {message}")
        
        # Check for continue command
        if message.lower() in ['continue', 'cont', 'more']:
            self.handle_continue(connection, sender, sender)  # DM context
            return
        
        # Generate AI response
        full_response = self.ollama_client.generate_full_response(message)
        chunked_response = self.get_first_chunk(full_response, sender, sender)
        
        # Send response back as private message
        connection.privmsg(sender, chunked_response)
        logger.info(f"Sent private response to {sender}")
    
    def on_pubmsg(self, connection, event):
        """Handle public channel messages"""
        sender = event.source.nick
        channel = event.target
        message = event.arguments[0].strip() if event.arguments else ""
        
        # Check for simple continue command (no mention)
        if message.lower() in ['continue', 'cont', 'more']:
            self.handle_continue(connection, sender, channel)
            return
        
        # Check if bot is mentioned
        if self.is_mentioned(message):
            # Remove bot name from message
            clean_message = self.clean_message(message)
            
            # Check if the cleaned message is a continue command
            if clean_message.lower().strip() in ['continue', 'cont', 'more']:
                logger.info(f"Continue command from {sender} in {channel}")
                self.handle_continue(connection, sender, channel)
                return
            
            logger.info(f"Mentioned in {channel} by {sender}: {clean_message}")
            
            # Generate AI response
            full_response = self.ollama_client.generate_full_response(clean_message)
            chunked_response = self.get_first_chunk(full_response, sender, channel)
            
            # Send response to channel
            connection.privmsg(channel, f"{sender}: {chunked_response}")
            logger.info(f"Sent public response in {channel}")
    
    def is_mentioned(self, message):
        """Check if the bot is mentioned in the message"""
        message_lower = message.lower()
        bot_name_lower = self.bot_name.lower()
        
        # Check for various mention patterns
        mentions = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"{bot_name_lower} ",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        return any(mention in message_lower for mention in mentions)
    
    def clean_message(self, message):
        """Remove bot name and clean up the message"""
        message_lower = message.lower()
        bot_name_lower = self.bot_name.lower()
        
        # Remove common mention patterns
        patterns_to_remove = [
            f"{bot_name_lower}:",
            f"{bot_name_lower},",
            f"@{bot_name_lower}",
            bot_name_lower
        ]
        
        clean_msg = message
        for pattern in patterns_to_remove:
            clean_msg = clean_msg.replace(pattern, "", 1)
            clean_msg = clean_msg.replace(pattern.title(), "", 1)
            clean_msg = clean_msg.replace(pattern.upper(), "", 1)
        
        return clean_msg.strip()
    
    def get_first_chunk(self, full_text, user, context):
        """Get the first chunk of text and store the rest for continuation"""
        key = f"{user}@{context}"
        
        # Clean the text for IRC
        clean_text = full_text.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
        clean_text = ' '.join(clean_text.split())
        
        # Reserve space for the continuation message
        continuation_msg = " (say 'continue' for more)"
        max_content_length = 400 - len(continuation_msg)
        
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
    
    def handle_continue(self, connection, user, context):
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
                max_content_length = 400 - len(continuation_msg)
                
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
            connection.privmsg(user, response)
        else:  # Channel
            connection.privmsg(context, f"{user}: {response}")
        
        logger.info(f"Sent continuation to {user} in {context}")
    
    def on_error(self, connection, event):
        """Handle IRC errors"""
        logger.error(f"IRC Error: {event}")
    
    def on_disconnect(self, connection, event):
        """Handle disconnection"""
        logger.info("Disconnected from IRC server")
    
    def start_bot(self):
        """Start the IRC bot"""
        try:
            logger.info("Starting IRC bot...")
            self.start()
        except Exception as e:
            logger.error(f"Error starting IRC bot: {e}")
            raise

def run_irc_bot(config):
    """Function to run the IRC bot in a separate thread"""
    bot = IRCBot(config)
    bot.start_bot()