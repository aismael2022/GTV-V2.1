#!/bin/bash

echo "📦 Requirements:"
curl -s https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/requirements.txt

# Ensure pip3 exists
if ! command -v pip3 >/dev/null 2>&1; then
  echo "⚙️ Installing pip..."
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Make temp dir
WORKDIR=$(mktemp -d)
cd "$WORKDIR" || exit 1

# Download everything needed
echo "📥 Getting files ready..."
for file in Orchestrator.py Scraper.py video_factory_V2.py images_factory.py requirements.txt; do
  curl -sO "https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/$file"
done

# Install dependencies
echo "📦 Installing Python packages..."
pip3 install -q -r requirements.txt

# Run
echo "🚀 Running..."
python3 Orchestrator.py

# Cleanup
echo "🧹 Cleaning up temp files..."
cd ~
rm -rf "$WORKDIR"
