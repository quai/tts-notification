#!/usr/bin/env python3
"""
TTS Notification Script for Claude Code Hooks
Generates speech from text using OpenAI TTS API with caching and playback.
"""

import os
import sys
import json
import hashlib
import argparse
import subprocess
from pathlib import Path
from openai import OpenAI

# Configuration
CACHE_DIR = Path.home() / ".cache" / "claude-tts"
DEFAULT_VOICE = "alloy"
DEFAULT_MODEL = "tts-1"

def setup_cache_dir():
    """Ensure cache directory exists."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR

def get_cache_filename(text, voice, model):
    """Generate cache filename based on text content and settings."""
    content = f"{text}:{voice}:{model}"
    hash_obj = hashlib.md5(content.encode())
    return CACHE_DIR / f"{hash_obj.hexdigest()}.mp3"

def generate_tts(text, voice=DEFAULT_VOICE, model=DEFAULT_MODEL):
    """Generate TTS audio using OpenAI API."""
    client = OpenAI()
    
    cache_file = get_cache_filename(text, voice, model)
    
    # Return cached file if exists
    if cache_file.exists():
        return cache_file
    
    # Generate new TTS
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Save to cache
        with open(cache_file, 'wb') as f:
            f.write(response.content)
        
        return cache_file
    
    except Exception as e:
        print(f"Error generating TTS: {e}", file=sys.stderr)
        return None

def play_audio(file_path):
    """Play audio file using system audio player."""
    if not file_path or not file_path.exists():
        return False
    
    # Try different audio players
    players = ['mpg123', 'afplay', 'paplay', 'aplay', 'ffplay']
    
    for player in players:
        try:
            result = subprocess.run([player, str(file_path)], 
                                  capture_output=True, 
                                  timeout=10)
            if result.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print(f"Could not play audio file: {file_path}", file=sys.stderr)
    return False

def main():
    parser = argparse.ArgumentParser(description="TTS notification for Claude Code")
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("--voice", default=DEFAULT_VOICE, 
                       choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                       help="Voice to use")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                       choices=["tts-1", "tts-1-hd"],
                       help="TTS model to use")
    parser.add_argument("--no-play", action="store_true", 
                       help="Generate file but don't play it")
    parser.add_argument("--cache-only", action="store_true",
                       help="Only check cache, don't generate new file")
    
    args = parser.parse_args()
    
    # Get text from argument or stdin
    if args.text:
        text = args.text
    else:
        try:
            # Try to read from stdin (for hook usage)
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                # Try to parse as JSON first (hook data)
                try:
                    hook_data = json.loads(stdin_data)
                    # Extract text from hook data or use default
                    text = hook_data.get("message", "Claude Code needs attention")
                except json.JSONDecodeError:
                    # Use stdin data directly
                    text = stdin_data
            else:
                text = "Claude Code needs attention"
        except:
            text = "Claude Code needs attention"
    
    if not text.strip():
        print("No text provided", file=sys.stderr)
        return 1
    
    # Setup cache directory
    setup_cache_dir()
    
    # Check if we should only look in cache
    if args.cache_only:
        cache_file = get_cache_filename(text, args.voice, args.model)
        if cache_file.exists():
            if not args.no_play:
                play_audio(cache_file)
            print(f"Cache hit: {cache_file}")
            return 0
        else:
            print("Not found in cache", file=sys.stderr)
            return 1
    
    # Generate TTS
    audio_file = generate_tts(text, args.voice, args.model)
    
    if not audio_file:
        return 1
    
    print(f"Generated: {audio_file}")
    
    # Play audio unless disabled
    if not args.no_play:
        if play_audio(audio_file):
            print("Playback completed")
        else:
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())