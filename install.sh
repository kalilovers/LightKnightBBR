#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-pip
pip install colorama
python3 <(curl -Ls https://raw.githubusercontent.com/kalilovers/LightKnightBBR/main/bbr.py --ipv4)
