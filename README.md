# python

## Jeu du pendu

Le bureau distant noVNC et le jeu du pendu démarrent automatiquement au démarrage du Codespace ; le port **6080** s'ouvre dans le navigateur. Après avoir ajouté la configuration `.devcontainer`, reconstruis le Codespace une fois pour l'activer. Pour démarrer le bureau manuellement :

```bash
./start-gui.sh
```

Dans l'onglet **Ports** de VS Code, ouvre le port **6080** dans un navigateur et ajoute `/vnc.html` à l'adresse si nécessaire. Le jeu s'affiche dans le bureau distant. Pour le relancer manuellement si besoin :

```bash
python -m pip install -r requirements.txt
DISPLAY=:1 python pendu.py
```

Les lettres peuvent être choisies en cliquant sur le clavier affiché ou en les tapant au clavier.
Clique sur **Nouvelle partie** pour changer de mot. Après une partie, appuie sur **Espace** ou **R** pour rejouer. **Échap** permet de quitter.