#!/bin/bash

LABDIR="/home/kali/llab9"
DOCKERDIR="$LABDIR/Dockerized"

echo "[+] Updating packages..."
sudo apt update

echo "[+] Installing Wireshark..."
sudo apt install -y wireshark

echo "[+] Configuring Wireshark permissions..."
sudo usermod -aG wireshark $USER
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap
newgrp wireshark <<EOF
echo "Wireshark permissions applied"
EOF

echo "[+] Installing Docker and legacy docker-compose..."
sudo apt install -y docker.io docker-compose

echo "[+] Starting Docker service..."
sudo systemctl enable --now docker

echo "[+] Adding user to docker group..."
sudo usermod -aG docker $USER
newgrp docker <<EOF
echo "Docker permissions applied"
EOF

echo "[+] Moving to Docker project..."
cd $DOCKERDIR

echo "[+] Building container with docker-compose..."
docker-compose build

echo "[+] Starting container..."
docker-compose up -d

echo "[+] Starting login server..."
python3 $LABDIR/login_server.py &

echo "[+] Starting HTTP request generator..."
python3 $LABDIR/send_requests.py &

echo ""
echo "===================================="
echo "LAB RUNNING"
echo ""
echo "Docker web app:"
echo "http://localhost:5000"
echo ""
echo "Login page:"
echo "http://localhost:5550"
echo ""
echo "Wireshark filter:"
echo "tcp.port == 5550"
