# TTS Notification for Claude Code

A Text-to-Speech notification system that integrates with Claude Code hooks to provide audio feedback during development workflows.

## Purpose

This tool enhances the Claude Code development experience by providing audio notifications for key events:
- **Task completion alerts** - Know when long-running operations finish
- **Attention notifications** - Get notified when Claude is waiting for input
- **Custom workflow alerts** - Configure notifications for any hook event

Perfect for developers who want to multitask while Claude Code works in the background, or for accessibility enhancement.

## Features

- 🔊 **Text-to-Speech notifications** using OpenAI's TTS API
- 🎵 **Multiple voice options** (alloy, echo, fable, onyx, nova, shimmer)
- 💾 **Smart caching** to avoid repeated API calls for the same messages
- 🔗 **Claude Code hook integration** for automatic notifications
- 🎛️ **Cross-platform audio playback** support
- ⚡ **Fast execution** with efficient caching system

## Installation

### Prerequisites

1. **Python 3** and pip
2. **OpenAI API key** - Set as `OPENAI_API_KEY` environment variable
3. **Audio player** - One of: `mpg123`, `afplay`, `paplay`, `aplay`, or `ffplay`

### Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy the script to your Claude Code user bin directory:**
   ```bash
   mkdir -p ~/.claude/user/bin
   cp tts-notification.py ~/.claude/user/bin/
   chmod +x ~/.claude/user/bin/tts-notification.py
   ```

3. **Configure your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Set up Claude Code hooks** by adding to your settings file:
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

## Usage

### Direct Usage

```bash
# Basic text-to-speech
./tts-notification.py "Your message here"

# Choose a different voice
./tts-notification.py "Hello world" --voice nova

# Use high-quality model
./tts-notification.py "Important message" --model tts-1-hd

# Generate audio file without playing
./tts-notification.py "Background task" --no-play

# Check if message is cached
./tts-notification.py "Test message" --cache-only
```

### Hook Integration

The script automatically integrates with Claude Code hooks:
- Reads JSON data from stdin when used as a hook command
- Falls back to command-line arguments or default messages
- Caches generated audio to minimize API usage

## Configuration

### Voice Options
- `alloy` (default) - Balanced, neutral voice
- `echo` - Clear, professional tone
- `fable` - Warm, storytelling voice
- `onyx` - Deep, authoritative voice
- `nova` - Bright, energetic voice
- `shimmer` - Soft, gentle voice

### Models
- `tts-1` (default) - Fast, cost-effective
- `tts-1-hd` - Higher quality, slower generation

### Cache Location
Audio files are cached in: `~/.cache/claude-tts/`

## Technical Details

### Architecture
- **Input Processing**: Handles command-line args, stdin, and JSON hook data
- **Caching System**: MD5-based file naming for efficient cache lookups
- **API Integration**: Uses OpenAI's TTS API with error handling
- **Audio Playback**: Multi-platform player detection and execution

### Supported Audio Players
The script automatically detects and uses available players:
- `mpg123` (Linux/Unix)
- `afplay` (macOS)
- `paplay` (PulseAudio)
- `aplay` (ALSA)
- `ffplay` (FFmpeg)

### Error Handling
- Graceful fallback when API calls fail
- Silent operation when no audio player is available
- Timeout protection for audio playback

## Claude Code Hook Documentation

For comprehensive information about hooks in Claude Code:
- **[Hooks Overview](https://docs.anthropic.com/en/docs/claude-code/hooks)** - Complete guide to hook system
- **[Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings)** - How to configure Claude Code settings
- **[CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)** - Command-line usage and options

## Examples

### Basic Hook Setup
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command", 
            "command": "~/.claude/user/bin/tts-notification.py 'Done!'"
          }
        ]
      }
    ]
  }
}
```

### Advanced Configuration
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*.py",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/user/bin/tts-notification.py 'Python task completed' --voice onyx"
          }
        ]
      }
    ],
    "Error": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/user/bin/tts-notification.py 'Error occurred' --voice shimmer"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

**No audio playback:**
- Install an audio player: `sudo apt install mpg123` (Linux) or `brew install mpg123` (macOS)
- Check system audio settings

**API errors:**
- Verify `OPENAI_API_KEY` environment variable is set
- Check API key has sufficient credits
- Ensure network connectivity

**Hook not triggering:**
- Verify script path in hook configuration
- Check script permissions: `chmod +x ~/.claude/user/bin/tts-notification.py`
- Review Claude Code settings file syntax

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## License

MIT License - see LICENSE file for details.