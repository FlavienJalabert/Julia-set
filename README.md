# Julia-set
Ce programme est un projet étudiant permettant de visualiser et d'explorer l'auto-similarité des ensembles de Julia.

## Installation
Dépendances :
 - OpenGL : `sudo apt install python3-opengl`
 - NumPy : `sudo apt install python3-numpy`
 - PIL : `sudo apt install python3-pillow`

## Modification des valeurs de calcul
 - ```width, height``` pour la taille de la fenêtre
 - ```cX, cY``` pour la constante complexe
 - ```max_iter``` pour le nombre maximal d’itération
 - ```colors``` pour changer les couleurs (nombre compris entre [1;2], utiliser 3 valeurs différentes pour un meilleur rendu)

## Exécution
```bash
python3 julia_app.py
```

## Contrôles

 1. **zqsd** pour les déplacements orthogonaux
 2. **i** pour zoomer
 3. **k** pour dézoomer
 4.  **e** pour exporter
 5. **x** pour quitter
