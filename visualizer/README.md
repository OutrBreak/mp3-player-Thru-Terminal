# SERIAL EXPERIMENTS LAIN - THE WIRED AUDIO INTERFACE MADE BY OUTRBREAK

A terminal-based MP3 player themed after Serial Experiments Lain, featuring real-time audio visualization in the aesthetic of THE WIRED.

```
[ PRESENT DAY - PRESENT TIME ]
>> THE WIRED AUDIO INTERFACE <<
```

## Features

- **Classic Spectrum Analyzer**: Stationary frequency bars like vintage car stereos
-  **Protocol 7 Playback**: Full control over your audio stream
- **Peak Indicators**: Falling peak markers for each frequency band
-  **Signal Control**: Precise volume adjustment
- **Auto-Advance**: Seamlessly transitions between audio layers
- **Auto-Discovery**: Automatically indexes all MP3 files in the songs folder
- **Lain Theme**: Green/cyan terminal aesthetic with ASCII art from the show
-  **Glitch Effects**: Occasional digital artifacts for authenticity

## Installation

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or install dependencies manually:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Add your MP3 files:**
   ```bash
   cp /path/to/your/music/*.mp3 songs/
   ```

3. **Run the player:**
   ```bash
   python3 player.py
   ```

## Protocol Controls

| Key | Action |
|-----|--------|
| `SPACE` | PLAY/PAUSE stream |
| `n` | NEXT LAYER (next song) |
| `p` | PREV LAYER (previous song) |
| `→` | SEEK forward +10 seconds |
| `←` | SEEK backward -10 seconds |
| `+` | AMP UP (increase volume) |
| `-` | AMP DOWN (decrease volume) |
| `r` | REFRESH data stream |
| `q` | DISCONNECT from THE WIRED |

## Adding Songs

drop MP3 files into the `songs/` folder. The player will automatically detect and format them in alphabetical order.

You can add songs while the player is running and press `r` to reload the song list!

## Requirements

- Python 3.7+
- pygame (for audio playback)
- numpy (for visualization)
- A terminal with color support

## Troubleshooting

**No sound**
- Make sure your system audio is working
- Check that pygame is properly installed
- Verify your MP3 files are not corrupted

**Visualizer not showing**
- Make sure your terminal window is large enough
- Try maximizing the terminal window

**Colors look wrong**
- Ensure your terminal supports 256 colors
- Try a different terminal emulator (recommended: gnome-terminal, iTerm2, or Windows Terminal)

- Maximize your terminal window for full immersion
- The spectrum analyzer displays 64 independent frequency bands
- Bass frequencies on the left, treble on the right 
- Watch for occasional glitch effects
- Audio layers are played in alphabetical order
- The interface automatically advances to the next layer

```
CLOSE THE WORLD,
OPEN THE nExt
```

