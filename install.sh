#!/bin/bash
CYAN="\e[96m"
GREEN="\e[92m"
YELLOW="\e[93m"
RED="\e[91m"
BLUE="\e[94m"
MAGENTA="\e[95m"
WHITE="\e[97m"
NC="\e[0m"

# Function to check if a package is installed
check_pkg() {
    dpkg -l | grep -qw "$1"
}

echo && echo -e "$YELLOW Updating package list... $NC"
sudo apt update

# Check and install python3 if not installed
if check_pkg "python3"; then
    echo && echo -e "$GREEN Python3 is already installed. $NC"
else
    echo && echo -e "$YELLOW Installing Python3... $NC"
    sudo apt install -y python3
fi

# Check and install python3-pip if not installed
if check_pkg "python3-pip"; then
    echo && echo -e "$GREEN pip3 is already installed. $NC"
else
    echo && echo -e "$YELLOW Installing pip3... $NC"
    sudo apt install -y python3-pip
fi

# Check if colorama is installed in Python, and install if necessary
if python3 -c "import colorama" &> /dev/null; then
    echo && echo -e "$GREEN colorama is already installed. $NC"
else
    echo && echo -e "$YELLOW Installing colorama... $NC"
    pip3 install colorama
fi

# Run the Python script
python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
