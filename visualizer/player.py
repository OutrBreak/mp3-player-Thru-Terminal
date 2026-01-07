#!/usr/bin/env python3
"""
Terminal MP3 Player with Visualizer
Black and Purple color scheme
"""

import curses
import pygame
import numpy as np
import os
import time
import threading
from pathlib import Path
from pygame import mixer


class MP3Player:
    def __init__(self, songs_dir="songs"):
        self.songs_dir = songs_dir
        self.songs = []
        self.current_song_index = 0
        self.paused = False
        self.volume = 0.7
        self.running = True
        self.audio_data = np.zeros(64)
        self.song_start_time = 0
        self.pause_time = 0
        self.seek_offset = 0  # Track manual seeking offset
        self.peak_data = np.zeros(64)  # Track peak values for bars
        self.beat_intensity = 0  # Simulated beat intensity
        self.current_song_length = 0  # Cached song length

        # Initialize pygame mixer
        pygame.init()
        mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Load songs
        self.load_songs()

    def load_songs(self):
        """Load all MP3 files from the songs directory"""
        songs_path = Path(self.songs_dir)
        if not songs_path.exists():
            songs_path.mkdir(parents=True)

        self.songs = sorted([f for f in os.listdir(self.songs_dir)
                            if f.lower().endswith('.mp3')])

    def play_song(self, start_pos=0):
        """Play the current song from a specific position"""
        if not self.songs:
            return

        song_path = os.path.join(self.songs_dir, self.songs[self.current_song_index])
        try:
            mixer.music.load(song_path)
            mixer.music.set_volume(self.volume)
            mixer.music.play(start=start_pos)
            self.paused = False
            self.song_start_time = time.time()
            self.seek_offset = start_pos

            # Cache the song length (only calculate once per song)
            try:
                sound = pygame.mixer.Sound(song_path)
                self.current_song_length = sound.get_length()
            except:
                self.current_song_length = 0
        except Exception as e:
            pass

    def toggle_pause(self):
        """Toggle pause/play"""
        if self.paused:
            mixer.music.unpause()
            # Adjust start time to account for pause duration
            self.song_start_time += (time.time() - self.pause_time)
            self.paused = False
        else:
            mixer.music.pause()
            self.pause_time = time.time()
            self.paused = True

    def next_song(self):
        """Play next song"""
        if self.songs:
            self.current_song_index = (self.current_song_index + 1) % len(self.songs)
            self.play_song()

    def prev_song(self):
        """Play previous song"""
        if self.songs:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
            self.play_song()

    def seek_forward(self):
        """Seek forward 10 seconds"""
        if not self.songs or not mixer.music.get_busy():
            return

        try:
            # Get current position
            current_pos = self.get_song_position()
            new_pos = current_pos + 10

            # Restart song from new position
            mixer.music.stop()
            self.play_song(start_pos=new_pos)
        except:
            pass

    def seek_backward(self):
        """Seek backward 10 seconds"""
        if not self.songs or not mixer.music.get_busy():
            return

        try:
            # Get current position
            current_pos = self.get_song_position()
            new_pos = max(0, current_pos - 10)

            # Restart song from new position
            mixer.music.stop()
            self.play_song(start_pos=new_pos)
        except:
            pass

    def volume_up(self):
        """Increase volume"""
        self.volume = min(1.0, self.volume + 0.1)
        mixer.music.set_volume(self.volume)

    def volume_down(self):
        """Decrease volume"""
        self.volume = max(0.0, self.volume - 0.1)
        mixer.music.set_volume(self.volume)

    def get_song_position(self):
        """Get current song position in seconds"""
        if not mixer.music.get_busy():
            return 0

        if self.paused:
            # Return position at pause time
            elapsed = self.pause_time - self.song_start_time
        else:
            # Calculate elapsed time since song started
            elapsed = time.time() - self.song_start_time

        return self.seek_offset + elapsed

    def get_song_length(self):
        """Get cached song length"""
        return self.current_song_length

    def generate_visualizer_data(self):
        """Generate classic car-style spectrum analyzer data - stationary bars"""
        if mixer.music.get_busy() and not self.paused:
            current_time = time.time()

            # Simulate beat pattern for overall intensity - MORE INTENSE
            beat_freq = 1.8  # Consistent beat frequency
            beat = (np.sin(current_time * beat_freq * 2 * np.pi) + 1) / 2

            # Create beat intensity variations with HIGHER peaks
            self.beat_intensity = self.beat_intensity * 0.75 + beat * 0.25
            if np.random.random() < 0.015:  # Occasional drops
                self.beat_intensity *= 0.3

            # Generate new frame of data with MUCH HIGHER amplitude
            new_data = np.zeros(64)

            # Bass frequencies (bars 0-15) - VERY HIGH and punchy
            bass_base = (self.beat_intensity ** 1.3) * 1.6  # Increased from 0.9 to 1.6
            for i in range(16):
                # Each bar has independent movement with MORE variation
                variation = np.random.random() * 0.6 + 0.7  # Higher range
                strength = bass_base * variation * (1.0 - i / 25)
                new_data[i] = strength

            # Low-mids (bars 16-27) - Higher and more rhythmic
            mid_low_base = self.beat_intensity * 1.35  # Increased from 0.75
            for i in range(16, 28):
                variation = np.random.random() * 0.7 + 0.6
                strength = mid_low_base * variation * (1.0 - (i - 16) / 20)
                new_data[i] = strength

            # Mid frequencies (bars 28-40) - HIGHER peaks
            mid_base = self.beat_intensity * 1.2  # Increased from 0.65
            for i in range(28, 41):
                variation = np.random.random() * 0.8 + 0.5
                strength = mid_base * variation
                new_data[i] = strength

            # High-mids (bars 41-52) - More active and TALLER
            high_mid_base = self.beat_intensity * 1.0  # Increased from 0.55
            for i in range(41, 53):
                variation = np.random.random() * 0.9 + 0.4
                strength = high_mid_base * variation
                new_data[i] = strength

            # Treble frequencies (bars 53-63) - Sparkly and HIGHER
            treble_base = self.beat_intensity * 0.85  # Increased from 0.45
            for i in range(53, 64):
                variation = np.random.random() * 1.0 + 0.3
                strength = treble_base * variation * (0.9 - (i - 53) / 18)
                new_data[i] = strength

            # Add MORE frequent energy spikes with HIGHER amplitude
            if np.random.random() < 0.12:  # More frequent
                spike_bar = int(np.random.random() * 64)
                new_data[spike_bar] = min(2.2, new_data[spike_bar] + 0.7)  # Much higher spikes

            # Allow MUCH HIGHER values for dramatic peaks
            new_data = np.clip(new_data, 0, 2.2)  # Increased from 1.3 to 2.2

            # VERY fast response for snappy, reactive movement
            self.audio_data = self.audio_data * 0.35 + new_data * 0.65  # More responsive

            # Update peaks - they fall more slowly
            for i in range(len(self.audio_data)):
                if self.audio_data[i] > self.peak_data[i]:
                    self.peak_data[i] = self.audio_data[i]
                else:
                    self.peak_data[i] *= 0.94  # Slightly slower fall for peak hold
        else:
            # Fade out when paused
            self.audio_data *= 0.82
            self.peak_data *= 0.88
            self.beat_intensity *= 0.85

        return self.audio_data


def draw_visualizer(stdscr, player, start_row, height, width):
    """Draw the enhanced audio visualizer with peaks"""
    data = player.generate_visualizer_data()
    peaks = player.peak_data

    # Calculate bar width to fill the screen
    bar_count = len(data)  # Use all 64 data points
    available_width = width - 4  # Leave small margins
    bar_width = max(1, available_width // bar_count)
    remainder = available_width % bar_count  # Extra pixels to distribute

    # Draw visualizer bars
    col_position = 2  # Start position
    for i in range(bar_count):
        # Distribute remainder across first bars to fill screen completely
        current_bar_width = bar_width + (1 if i < remainder else 0)
        col_start = col_position
        col_position += current_bar_width  # Update for next bar
        bar_height = int(data[i] * (height - 2))
        bar_height = min(bar_height, height - 2)

        peak_height = int(peaks[i] * (height - 2))
        peak_height = min(peak_height, height - 2)

        # Draw bar from bottom up with gradient
        for j in range(bar_height):
            row = start_row + height - 2 - j

            # Create gradient effect based on height percentage
            height_percent = j / max(1, bar_height)

            # Use different characters and colors for Lain theme
            if height_percent > 0.85:
                # Top of bar - bright cyan
                char = "█"
                color = curses.color_pair(3) | curses.A_BOLD
            elif height_percent > 0.6:
                # Upper middle - bright green/cyan
                char = "█"
                color = curses.color_pair(3)
            elif height_percent > 0.3:
                # Middle - medium green
                char = "▓"
                color = curses.color_pair(2)
            else:
                # Bottom - dark green
                char = "▒"
                color = curses.color_pair(1)

            # Fill the full bar width
            for w in range(current_bar_width):
                col = col_start + w
                if 0 <= row < curses.LINES and 0 <= col < curses.COLS:
                    try:
                        stdscr.addstr(row, col, char, color)
                    except:
                        pass

        # Draw peak indicator (falling dot)
        if peak_height > bar_height + 2:
            peak_row = start_row + height - 2 - peak_height

            # Fill the full bar width with peak indicator
            for w in range(current_bar_width):
                peak_col = col_start + w
                if 0 <= peak_row < curses.LINES and 0 <= peak_col < curses.COLS:
                    try:
                        stdscr.addstr(peak_row, peak_col, "▬",
                                    curses.color_pair(3) | curses.A_BOLD)
                    except:
                        pass


def draw_progress_bar(stdscr, player, row, width):
    """Draw the progress bar with Lain theme"""
    position = player.get_song_position()
    length = player.get_song_length()

    if length > 0:
        progress = min(1.0, position / length)
    else:
        progress = 0

    bar_width = width - 24
    filled = int(progress * bar_width)

    # Time display
    time_str = f"{int(position//60):02d}:{int(position%60):02d} / {int(length//60):02d}:{int(length%60):02d}"

    try:
        stdscr.addstr(row, 2, "STREAM: ", curses.color_pair(2))
        stdscr.addstr(row, 11, "█" * filled, curses.color_pair(3))
        stdscr.addstr(row, 11 + filled, "░" * (bar_width - filled), curses.color_pair(5))
        stdscr.addstr(row, width - len(time_str) - 2, time_str, curses.color_pair(2))
    except:
        pass


def draw_lain_art(stdscr, height, width):
    """Draw Serial Experiments Lain ASCII art and quotes"""
    # Lain face ASCII art (from reference image - right side)
    lain_face = [
        "     ░░░▒▒▒▓▓▓██",
        "   ░░▒▒▓▓████████",
        "  ░▒▓███░░░██░░██",
        "  ▒▓██░░░░░░░░░██",
        "  ▓██░░░██░░██░██",
        "  ███░░░██░░██░██",
        "  ▓██░░░░░░░░░░██",
        "  ▒▓██░░░███░░██",
        "   ░▒▓███░░░░██",
        "     ░▒▒▓▓████",
    ]

    # Wired connection visual
    wired_art = [
        "╔═══════════════╗",
        "║ THE WIRED    ║",
        "║  ○ ○ ○ ○ ○   ║",
        "║  CONNECTED   ║",
        "╚═══════════════╝",
    ]

    # Lain quotes cycling
    quotes = [
        "CLOSE THE WORLD,",
        "OPEN THE nExt",
    ]

    try:
        # Draw Lain face ASCII art (bottom right)
        if height > 20 and width > 75:
            start_row = height - 15
            start_col = width - 22
            for i, line in enumerate(lain_face):
                if start_row + i < height - 5:
                    stdscr.addstr(start_row + i, start_col, line, curses.color_pair(3))

        # Draw Wired connection box (right side, middle)
        if height > 20 and width > 70:
            start_row = height // 2
            start_col = width - 25
            for i, line in enumerate(wired_art):
                if start_row + i < height - 5:
                    stdscr.addstr(start_row + i, start_col, line, curses.color_pair(3))

        # Draw quotes (bottom left)
        if height > 10 and width > 40:
            quote_row = height - 3
            for i, quote in enumerate(quotes):
                if quote_row - i >= height - 4:
                    stdscr.addstr(height - 3 + i, 2, f"// {quote}", curses.color_pair(5))

        # Add some digital noise/glitch effect
        import random
        if random.random() < 0.1 and height > 15 and width > 80:
            glitch_chars = ["█", "▓", "▒", "░", "▪", "▫"]
            for _ in range(3):
                x = random.randint(width - 26, width - 3)
                y = random.randint(6, min(height - 6, height // 2 - 2))
                char = random.choice(glitch_chars)
                stdscr.addstr(y, x, char, curses.color_pair(4))

    except:
        pass


def draw_controls(stdscr, start_row, start_col):
    """Draw control instructions with Lain theme"""
    controls = [
        ("PROTOCOL", ""),
        ("─" * 22, ""),
        ("SPACE", "PLAY/PAUSE"),
        ("n", "NEXT LAYER"),
        ("p", "PREV LAYER"),
        ("→", "SEEK +10s"),
        ("←", "SEEK -10s"),
        ("+", "AMP UP"),
        ("-", "AMP DOWN"),
        ("r", "REFRESH"),
        ("q", "DISCONNECT"),
    ]

    try:
        for i, (key, desc) in enumerate(controls):
            row = start_row + i
            if i == 0:
                stdscr.addstr(row, start_col, f"[ {key} ]", curses.color_pair(3) | curses.A_BOLD)
            elif i == 1:
                stdscr.addstr(row, start_col, key, curses.color_pair(3))
            else:
                stdscr.addstr(row, start_col, f"[{key:^6}]", curses.color_pair(2))
                stdscr.addstr(row, start_col + 9, desc, curses.color_pair(1))
    except:
        pass


def draw_ui(stdscr, player):
    """Main UI drawing function"""
    stdscr.erase()  # Use erase instead of clear to reduce flickering
    height, width = stdscr.getmaxyx()

    # Lain-themed title
    title = "[ PRESENT DAY - PRESENT TIME ]"
    subtitle = ">> THE WIRED AUDIO INTERFACE <<"
    try:
        stdscr.addstr(0, (width - len(title)) // 2, title,
                     curses.color_pair(3) | curses.A_BOLD)
        if width > len(subtitle) + 4:
            stdscr.addstr(1, (width - len(subtitle)) // 2, subtitle,
                         curses.color_pair(2))
    except:
        pass

    # Current song info with Lain styling
    if player.songs:
        song_name = player.songs[player.current_song_index]
        status = "[PAUSED]" if player.paused else "[PROTOCOL 7]"
        song_info = f">> {status} [{player.current_song_index + 1}/{len(player.songs)}] {song_name}"

        # Truncate if too long
        if len(song_info) > width - 4:
            song_info = song_info[:width-7] + "..."

        try:
            stdscr.addstr(3, 2, song_info, curses.color_pair(2))
        except:
            pass
    else:
        try:
            stdscr.addstr(3, 2, ">> NO DATA STREAM DETECTED - ADD FILES TO 'songs/' <<",
                         curses.color_pair(4))
        except:
            pass

    # Volume indicator
    volume_str = f"SIGNAL: {'█' * int(player.volume * 10)}{'░' * (10 - int(player.volume * 10))} {int(player.volume * 100)}%"
    try:
        stdscr.addstr(4, 2, volume_str, curses.color_pair(1))
    except:
        pass

    # Visualizer (reserve space for controls on the right)
    visualizer_height = height - 12
    visualizer_width = width - 28  # Leave room for controls and ASCII art
    if visualizer_height > 5:
        draw_visualizer(stdscr, player, 6, visualizer_height, visualizer_width)

    # Progress bar
    draw_progress_bar(stdscr, player, height - 4, width)

    # Controls (right side)
    draw_controls(stdscr, 6, width - 26)

    # Lain ASCII art and decorations
    draw_lain_art(stdscr, height, width)

    # Border decorations with Lain theme
    try:
        border_char = "─"
        for i in range(1, width - 1):
            stdscr.addstr(5, i, border_char, curses.color_pair(3))
            stdscr.addstr(height - 5, i, border_char, curses.color_pair(3))

        # Corner accents
        stdscr.addstr(5, 0, "┌", curses.color_pair(3))
        stdscr.addstr(5, width - 1, "┐", curses.color_pair(3))
        stdscr.addstr(height - 5, 0, "└", curses.color_pair(3))
        stdscr.addstr(height - 5, width - 1, "┘", curses.color_pair(3))
    except:
        pass

    stdscr.refresh()


def show_intro(stdscr):
    """Display intro screen with Lain quote"""
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()

    # Initialize colors first
    curses.start_color()
    curses.use_default_colors()
    curses.init_color(8, 250, 0, 250)
    curses.init_color(9, 400, 0, 450)
    curses.init_color(10, 600, 0, 650)
    curses.init_color(11, 750, 0, 850)
    curses.init_color(12, 900, 0, 400)
    curses.init_pair(1, 9, -1)
    curses.init_pair(2, 10, -1)
    curses.init_pair(3, 11, -1)
    curses.init_pair(4, 12, -1)

    # Intro sequence
    for frame in range(60):  # About 3 seconds
        stdscr.clear()

        # Main quote
        quote1 = "CLOSE THE WORLD,"
        quote2 = "OPEN THE nExt"

        # Calculate center position
        center_row = height // 2

        try:
            # Fade in effect
            if frame < 15:
                if frame % 3 == 0:
                    stdscr.addstr(center_row - 1, (width - len(quote1)) // 2,
                                quote1, curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(center_row - 1, (width - len(quote1)) // 2,
                            quote1, curses.color_pair(3) | curses.A_BOLD)

            if frame >= 10:
                stdscr.addstr(center_row + 1, (width - len(quote2)) // 2,
                            quote2, curses.color_pair(2) | curses.A_BOLD)

            # Additional text after main quote appears
            if frame >= 30:
                subtitle = "[ SERIAL EXPERIMENTS LAIN ]"
                stdscr.addstr(center_row + 4, (width - len(subtitle)) // 2,
                            subtitle, curses.color_pair(1))

            if frame >= 40:
                prompt = "PRESS ANY KEY TO CONNECT TO THE WIRED"
                stdscr.addstr(height - 3, (width - len(prompt)) // 2,
                            prompt, curses.color_pair(2))

            # Glitch effect
            if frame > 20 and np.random.random() < 0.15:
                import random
                glitch_chars = ["█", "▓", "▒", "░", "▪", "▫", "#", "@"]
                for _ in range(5):
                    x = random.randint(2, width - 3)
                    y = random.randint(2, height - 3)
                    char = random.choice(glitch_chars)
                    stdscr.addstr(y, x, char, curses.color_pair(4))

        except:
            pass

        stdscr.refresh()
        time.sleep(0.05)

        # Check for key press to skip
        stdscr.nodelay(1)
        if stdscr.getch() != -1 and frame > 20:
            break

    # Wait for key press if auto-sequence completed
    stdscr.nodelay(0)
    stdscr.getch()
    stdscr.clear()


def main(stdscr):
    """Main application loop"""
    # Show intro screen first
    show_intro(stdscr)

    # Setup curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(50)  # 50ms timeout for input

    # Initialize color pairs (Serial Experiments Lain theme - Dark Magenta)
    curses.start_color()
    curses.use_default_colors()

    # Define Lain-themed colors (darker magenta palette)
    curses.init_color(8, 250, 0, 250)     # Deep dark magenta
    curses.init_color(9, 400, 0, 450)     # Dark magenta
    curses.init_color(10, 600, 0, 650)    # Medium magenta
    curses.init_color(11, 750, 0, 850)    # Bright magenta
    curses.init_color(12, 900, 0, 400)    # Red-magenta accent

    curses.init_pair(1, 9, -1)    # Dark magenta
    curses.init_pair(2, 10, -1)   # Medium magenta
    curses.init_pair(3, 11, -1)   # Bright magenta
    curses.init_pair(4, 12, -1)   # Red-magenta accent
    curses.init_pair(5, 8, -1)    # Deep dark magenta

    # Create player
    player = MP3Player()

    # Auto-play first song if available
    if player.songs:
        player.play_song()

    # Main loop
    while player.running:
        # Draw UI
        draw_ui(stdscr, player)

        # Handle input
        try:
            key = stdscr.getch()

            if key == ord('q'):
                player.running = False
            elif key == ord(' '):
                player.toggle_pause()
            elif key == ord('n'):
                player.next_song()
            elif key == ord('p'):
                player.prev_song()
            elif key == curses.KEY_RIGHT:
                player.seek_forward()
            elif key == curses.KEY_LEFT:
                player.seek_backward()
            elif key == ord('+') or key == ord('='):
                player.volume_up()
            elif key == ord('-') or key == ord('_'):
                player.volume_down()
            elif key == ord('r'):
                player.load_songs()
            elif key == curses.KEY_RESIZE:
                # Handle terminal resize
                stdscr.clear()
                stdscr.refresh()
        except:
            pass

        # Check if song ended
        if not mixer.music.get_busy() and not player.paused and player.songs:
            player.next_song()

        time.sleep(0.05)  # Increased sleep time to reduce flickering

    # Cleanup
    mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
