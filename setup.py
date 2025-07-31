"""
Setup script for AI Multi-Platform Bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-multi-platform-bot",
    version="1.0.0",
    author="AI Multi-Platform Bot Contributors",
    description="A Python bot that connects to IRC, Discord, and Slack to provide AI-powered responses using local Ollama models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ai-irc-slack-discord-ollama-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-multi-platform-bot=main:main",
        ],
    },
    keywords="ai, chatbot, irc, discord, slack, ollama, bot, artificial intelligence",
    project_urls={
        "Bug Reports": "https://github.com/your-username/ai-irc-slack-discord-ollama-bot/issues",
        "Source": "https://github.com/your-username/ai-irc-slack-discord-ollama-bot",
        "Documentation": "https://github.com/your-username/ai-irc-slack-discord-ollama-bot/tree/main/docs",
    },
)