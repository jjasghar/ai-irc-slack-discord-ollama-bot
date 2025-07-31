#!/usr/bin/env python3
"""
Multi-platform AI bot that can connect to IRC, Discord, and Slack
and interact with local Ollama AI models.
"""
import json
import toml
import logging
import sys
import asyncio
import threading
from pathlib import Path

# Import platform-specific clients
from irc_client import run_irc_bot
from discord_client import run_discord_bot
from slack_client import run_slack_bot
from ollama_client import OllamaClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AIBot:
    def __init__(self, config_file='config.toml'):
        self.config_file = config_file
        self.config = self.load_config()
        self.validate_config()
        
        logger.info(f"AI Bot initialized for platform: {self.config['platform']}")
    
    def load_config(self):
        """Load configuration from TOML file"""
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
            
            # Support both TOML and JSON for backward compatibility
            if config_path.suffix.lower() == '.json':
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file} (JSON format)")
            else:
                with open(config_path, 'r') as f:
                    config = toml.load(f)
                logger.info(f"Configuration loaded from {self.config_file} (TOML format)")
            
            return config
        
        except (json.JSONDecodeError, toml.TomlDecodeError) as e:
            logger.error(f"Invalid format in configuration file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def validate_config(self):
        """Validate configuration settings"""
        required_keys = ['platform', 'bot_name', 'ollama']
        
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        platform = self.config['platform']
        if platform not in ['irc', 'discord', 'slack']:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Validate platform-specific config
        if platform not in self.config:
            raise ValueError(f"Missing configuration for platform: {platform}")
        
        logger.info("Configuration validation passed")
    
    def test_ollama_connection(self):
        """Test connection to Ollama service"""
        ollama_client = OllamaClient(
            base_url=self.config['ollama']['base_url'],
            model=self.config['ollama']['model']
        )
        
        if ollama_client.is_available():
            models = ollama_client.list_models()
            logger.info(f"Ollama service is available. Models: {models}")
            
            # Test if configured model is available
            configured_model = self.config['ollama']['model']
            if configured_model not in models:
                logger.warning(f"Configured model '{configured_model}' not found in available models")
                logger.info("Available models: " + ", ".join(models))
            
            return True
        else:
            logger.error("Ollama service is not available")
            return False
    
    def run_irc(self):
        """Run IRC bot"""
        logger.info("Starting IRC bot...")
        run_irc_bot(self.config)
    
    def run_discord(self):
        """Run Discord bot"""
        logger.info("Starting Discord bot...")
        asyncio.run(run_discord_bot(self.config))
    
    def run_slack(self):
        """Run Slack bot"""
        logger.info("Starting Slack bot...")
        run_slack_bot(self.config)
    
    def start(self):
        """Start the bot based on configured platform"""
        # Test Ollama connection
        if not self.test_ollama_connection():
            logger.error("Cannot start bot: Ollama service is not available")
            logger.info("Please ensure Ollama is running and accessible at: " + 
                       self.config['ollama']['base_url'])
            return False
        
        platform = self.config['platform']
        
        try:
            if platform == 'irc':
                self.run_irc()
            elif platform == 'discord':
                self.run_discord()
            elif platform == 'slack':
                self.run_slack()
            else:
                logger.error(f"Unknown platform: {platform}")
                return False
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error running {platform} bot: {e}")
            return False
        
        return True

def main():
    """Main entry point"""
    print("🤖 AI Multi-Platform Bot")
    print("=" * 50)
    
    # Check for custom config file argument
    config_file = 'config.toml'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    try:
        bot = AIBot(config_file)
        
        print(f"Platform: {bot.config['platform']}")
        print(f"Bot Name: {bot.config['bot_name']}")
        print(f"Ollama URL: {bot.config['ollama']['base_url']}")
        print(f"AI Model: {bot.config['ollama']['model']}")
        print("=" * 50)
        
        # Start the bot
        success = bot.start()
        
        if not success:
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()