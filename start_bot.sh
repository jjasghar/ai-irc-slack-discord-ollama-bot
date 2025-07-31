#!/bin/bash
# Startup script for the AI bot

echo "🤖 Starting AI Multi-Platform Bot"
echo "=================================="

# Activate virtual environment
source venv/bin/activate

# Start the bot
python main.py

# Deactivate when done
deactivate