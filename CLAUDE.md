# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a TTS (Text-to-Speech) notification system for Claude Code hooks. It uses OpenAI's TTS API to generate speech notifications with caching and automatic playback.

## Core Components

- `tts-notification.py`: Main Python script that handles TTS generation, caching, and audio playback
- `example-claude-code-settings.json`: Example configuration showing how to integrate TTS notifications with Claude Code hooks

## Common Commands

### Running the TTS Script
```bash
# Basic usage with text
python3 tts-notification.py "Your message here"

# Test different voices
python3 tts-notification.py "Test message" --voice nova
python3 tts-notification.py "Test message" --voice alloy

# Generate without playing (useful for pre-caching)
python3 tts-notification.py "Message" --no-play

# Check if text is already cached
python3 tts-notification.py "Message" --cache-only
```

### Testing the Script
```bash
# Test help output
python3 tts-notification.py --help

# Test basic functionality
echo "Test notification" | python3 tts-notification.py
```

## Architecture

### TTS Pipeline
1. **Input Processing**: Accepts text from command line args, stdin, or JSON hook data
2. **Cache Management**: MD5-based caching in `~/.cache/claude-tts/` to avoid repeated API calls
3. **TTS Generation**: Uses OpenAI API with configurable voice and model options
4. **Audio Playback**: Multi-platform audio player detection (mpg123, afplay, paplay, etc.)

### Hook Integration
The script is designed to work with Claude Code hooks:
- **Stop hooks**: Notify when tasks complete
- **Notification hooks**: Alert when Claude needs attention
- Supports JSON input from hook systems

### Configuration
- Cache directory: `~/.cache/claude-tts/`
- Default voice: "alloy"
- Default model: "tts-1"
- Supported voices: alloy, echo, fable, onyx, nova, shimmer
- Supported models: tts-1, tts-1-hd

## Dependencies

### Required
- Python 3
- OpenAI Python library (`pip install openai`)
- OpenAI API key (set as OPENAI_API_KEY environment variable)

### Audio Playback (at least one required)
- `mpg123` (Linux/Unix)
- `afplay` (macOS)
- `paplay` (PulseAudio systems)
- `aplay` (ALSA systems)
- `ffplay` (FFmpeg)

## Installation and Setup

### Prerequisites Setup
```bash
# Install Python dependencies
pip install openai

# Set OpenAI API key (add to ~/.bashrc or ~/.zshrc for persistence)
export OPENAI_API_KEY="your-api-key-here"

# Install audio player (choose one based on your system)
sudo apt install mpg123      # Linux/Ubuntu
brew install mpg123          # macOS
sudo dnf install mpg123      # Fedora
```

### Script Installation
```bash
# Copy script to Claude Code user bin directory
mkdir -p ~/.claude/user/bin
cp tts-notification.py ~/.claude/user/bin/
chmod +x ~/.claude/user/bin/tts-notification.py
```

### Hook Configuration
Add to your Claude Code settings file (usually `~/.claude/settings.json`):
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/user/bin/tts-notification.py 'Task completed'"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "*", 
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/user/bin/tts-notification.py 'Claude is waiting'"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

**Script not found:**
- Verify script is in `~/.claude/user/bin/` and executable
- Check path in hook configuration matches actual location

**No audio playback:**
- Install audio player: `mpg123`, `afplay`, `paplay`, `aplay`, or `ffplay`
- Test audio system: `speaker-test -t sine -f 1000 -l 1` (Linux)

**API errors:**
- Verify `OPENAI_API_KEY` environment variable: `echo $OPENAI_API_KEY`
- Check API key has sufficient credits at platform.openai.com
- Test network connectivity to OpenAI API

**Hook not triggering:**
- Validate JSON syntax in settings file
- Check Claude Code settings file location
- Review hook matcher patterns (use `*` for all files)
- Restart Claude Code after settings changes