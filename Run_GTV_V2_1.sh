#!/bin/bash

echo "📦 Requirements:"
curl -s https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/requirements.txt

# Check if pip3 is installed
if ! command -v pip3 >/dev/null 2>&1; then
  echo -e "\n⚙️ pip3 not found. Attempting to install pip..."
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Create temporary folder
TMP_DIR="/tmp/gtv_run"
mkdir -p "$TMP_DIR"
cd "$TMP_DIR" || exit 1

echo -e "\n📥 Downloading required files...\n"
curl -sO https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/Orchestrator.py
curl -sO https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/Scraper.py
curl -sO https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/video_factory_V2.py
curl -sO https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/images_factory.py
curl -sO https://raw.githubusercontent.com/aismael2022/GTV-V2.1/main/requirements.txt

echo -e "\n📦 Installing Python packages...\n"
pip3 install -q -r requirements.txt

clear
echo -e "\n🚀 Starting NOVA ClIP Workflow...\n"
python3 Orchestrator.py

# Optional: clean up
# echo -e "\n🧹 Cleaning up temporary files..."
# rm -rf "$TMP_DIR"
