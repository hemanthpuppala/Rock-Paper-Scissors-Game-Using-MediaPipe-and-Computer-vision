import wave
import sys
import os

def playsound(file_path):
    """Play a WAV file using system commands (no external libraries required)."""
    
    # Check OS and use built-in player
    if sys.platform.startswith('darwin'):  # macOS
        os.system(f"afplay '{file_path}'")
    elif sys.platform.startswith('linux'):  # Linux
        os.system(f"aplay '{file_path}'")
    elif sys.platform.startswith('win'):  # Windows
        os.system(f"powershell -c (New-Object Media.SoundPlayer '{file_path}').PlaySync()")
    else:
        raise RuntimeError("Unsupported OS for sound playback.")

