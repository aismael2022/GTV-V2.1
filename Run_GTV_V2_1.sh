#!/bin/bash

echo "Requirements:"
curl -s https://raw.githubusercontent.com/aismael2022/GVT-V2.1/main/requirements.txt

# Check if pip3 is installed
if ! command -v pip3 >/dev/null 2>&1; then
  echo -e "\n⚙️ pip3 not found. Attempting to install pip..."
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

echo -e "\n⏳ Downloading necessary files... This may take a few minutes depending on your internet connection.\n"

# Install Python dependencies quietly
pip3 install -q -r <(curl -s https://raw.githubusercontent.com/aismael2022/GVT-V2.1/main/requirements.txt) > /dev/null 2>&1

# Clear terminal and run the script
clear
echo -e "\n🚀 Starting ..."
curl -s https://raw.githubusercontent.com/aismael2022/GVT-V2.1/main/Orchestrator.py | python3 -
