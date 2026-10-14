#!/bin/bash
echo "=== Installation des dépendances graphiques ==="
sudo apt-get update
sudo apt-get install -y xvfb fluxbox x11vnc novnc python3-pip

echo "=== Configuration de l'affichage virtuel ==="
export DISPLAY=:1
Xvfb :1 -screen 0 1024x768x16 &
sleep 2

echo "=== Lancement du gestionnaire de fenêtres (Fluxbox) ==="
fluxbox &
sleep 2

echo "=== Lancement du serveur VNC ==="
x11vnc -display :1 -nopw -listen localhost -xkb &
sleep 2

echo "=== Lancement de noVNC (Port 6080) ==="
/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 6080 &
sleep 2

echo "=== Installation de Pygame ==="
pip3 install pygame

echo "=== TOUT EST PRÊT ! ==="
