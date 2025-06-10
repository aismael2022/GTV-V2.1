#!/bin/bash

echo "⏳ Installing requirements..."

# Check for pip3 and install if missing
if ! command -v pip3 >/dev/null 2>&1; then
  echo -e "\n⚙️ pip3 not found. Installing..."
  curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Clone repo if not exists
if [ ! -d "GTV-V2.1" ]; then
  git clone https://github.com/aismael2022/GTV-V2.1.git
fi

cd GTV-V2.1 || exit 1

# Install dependencies
pip3 install -r requirements.txt > /dev/null 2>&1

clear
echo -e "\n🚀 Starting NOVA ClIP Workflow..."
python3 Orchestrator.py
