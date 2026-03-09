#!/bin/bash

LABDIR=$(pwd)
DOCKERDIR="$LABDIR/Dockerized"

echo "[+] Updating system..."
sudo apt update -y

echo "[+] Installing dependencies..."
sudo apt install -y docker.io docker-compose python3-flask python3-requests wireshark

echo "[+] Enabling Docker..."
sudo systemctl enable --now docker

echo "[+] Configuring Wireshark capture permissions..."
sudo usermod -aG wireshark $USER
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap

echo "[+] Cleaning previous lab runs..."
sudo docker rm -f mdo-web-container 2>/dev/null
pkill -f login_server.py 2>/dev/null
pkill -f send_requests.py 2>/dev/null

echo "[+] Building Docker container..."
cd "$DOCKERDIR"
sudo docker compose build

echo "[+] Starting Docker web server..."
sudo docker compose up -d

echo "[+] Waiting for container to initialize..."
sleep 5

echo "[+] Starting login server..."
cd "$LABDIR"
python3 login_server.py &

echo "[+] Starting HTTP request generator..."
python3 send_requests.py &

echo ""
echo "======================================"
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
echo "======================================"
