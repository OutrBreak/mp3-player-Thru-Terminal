#!/bin/bash
# Setup script for Terminal MP3 Player

echo "╔════════════════════════════════════════╗"
echo "║  Terminal MP3 Player Setup             ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Install requirements
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║  Setup Complete!                       ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    echo "To use the MP3 player:"
    echo "1. Add your MP3 files to the 'songs/' folder"
    echo "2. Run: python3 player.py"
    echo ""
    echo "Enjoy your music! ♪"
else
    echo ""
    echo "❌ Failed to install dependencies"
    echo "Try running manually: pip3 install pygame numpy"
    exit 1
fi
