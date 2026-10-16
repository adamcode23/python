#!/bin/bash
set -euo pipefail

echo "=== Installation des dépendances graphiques ==="
if ! command -v Xvfb >/dev/null ||
   ! command -v fluxbox >/dev/null ||
   ! command -v x11vnc >/dev/null ||
   [ ! -x /usr/share/novnc/utils/novnc_proxy ] ||
   ! command -v websockify >/dev/null; then
    sudo apt-get update
    sudo apt-get install -y xvfb fluxbox x11vnc novnc
fi

echo "=== Configuration de l'affichage virtuel ==="
export DISPLAY=:1
if ! pgrep -f '^Xvfb :1 ' >/dev/null; then
    nohup Xvfb :1 -screen 0 1024x768x16 >/tmp/xvfb.log 2>&1 </dev/null &
    for attempt in {1..10}; do
        if pgrep -f '^Xvfb :1 ' >/dev/null; then
            break
        fi
        sleep 1
    done
fi
if ! pgrep -f '^Xvfb :1 ' >/dev/null; then
    echo "Erreur : Xvfb n'a pas démarré. Consulte /tmp/xvfb.log." >&2
    exit 1
fi

echo "=== Lancement du gestionnaire de fenêtres (Fluxbox) ==="
if ! pgrep -x fluxbox >/dev/null; then
    nohup fluxbox >/tmp/fluxbox.log 2>&1 </dev/null &
    sleep 2
fi

echo "=== Lancement du serveur VNC ==="
if ! (echo > /dev/tcp/127.0.0.1/5900) >/dev/null 2>&1; then
    nohup x11vnc -display :1 -nopw -forever -shared -listen localhost -xkb >/tmp/x11vnc.log 2>&1 </dev/null &
fi
for attempt in {1..10}; do
    if (echo > /dev/tcp/127.0.0.1/5900) >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
if ! (echo > /dev/tcp/127.0.0.1/5900) >/dev/null 2>&1; then
    echo "Erreur : x11vnc n'écoute pas sur le port 5900. Consulte /tmp/x11vnc.log." >&2
    exit 1
fi

echo "=== Lancement de noVNC (Port 6080) ==="
if ! (echo > /dev/tcp/127.0.0.1/6080) >/dev/null 2>&1; then
    nohup /usr/share/novnc/utils/novnc_proxy --web /usr/share/novnc --vnc localhost:5900 --listen 6080 >/tmp/novnc.log 2>&1 </dev/null &
fi
for attempt in {1..10}; do
    if (echo > /dev/tcp/127.0.0.1/6080) >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
if ! (echo > /dev/tcp/127.0.0.1/6080) >/dev/null 2>&1; then
    echo "Erreur : noVNC n'écoute pas sur le port 6080." >&2
    echo "Consulte /tmp/novnc.log pour le détail." >&2
    exit 1
fi

echo "=== Bureau prêt : ouvre le port 6080 dans VS Code, puis visite /vnc.html. ==="
echo "Pour lancer le jeu, utilise un autre terminal : DISPLAY=:1 python pendu.py"
