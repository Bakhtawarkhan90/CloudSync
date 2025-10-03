#!/bin/bash

sudo apt-get update -y
sudo apt-get install docker.io -y
sudo apt-get install docker-compose-v2
sudo chown $USER /var/run/docker.sock
sudo usermod -aG docker $USER
git clone https://github.com/Bakhtawarkhan90/CloudSync.git
cd CloudSync
docker compose down && docker compose up -d --build
