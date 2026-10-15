# python

## Jeu du pendu

Le jeu graphique se lance avec Pygame dans le bureau distant. Démarre d'abord ce bureau :

```bash
./start-gui.sh
```

Le port **6080** ouvre le bureau distant dans noVNC ; il ne lance pas le jeu à lui seul. Ouvre ce port dans l'onglet **Ports** de VS Code, puis lance le jeu dans un autre terminal :

```bash
python -m pip install -r requirements.txt
DISPLAY=:1 python pendu.py
```

Les lettres peuvent être choisies en cliquant sur le clavier affiché ou en les tapant au clavier.
Clique sur **Nouvelle partie** pour changer de mot. Après une partie, appuie sur **Espace** ou **R** pour rejouer. **Échap** permet de quitter.