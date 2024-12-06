from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import sys
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

# Paramètres globaux de la fenêtre et fractale
width, height = 1920, 1080
max_iter = 100  # Nombre maximum d'itérations
zoom = 1.0  # Niveau de zoom
moveX, moveY = 0.0, 0.0  # Déplacement de la fractale
cX, cY = -0.7, 0.27015  # Valeurs de la constante complexe pour la génération
new_event = True # Booléen pour gérer le retraçage de la fractale
ch1, ch2 = 2.5, 1.5 # Valeurs de proportionnalité du crosshair (longueur et position relative)
colors = [1.2,1,2] # Valeurs pour les couleurs de la fractale (RGB)

# Afficher la barre de progression
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # nouvelle ligne après completion
    if iteration == total:
        print()

# Fonction pour gérer l'exportation de l'image
def export():
    glutSwapBuffers()
    image = Image.frombytes("RGBA", (width, height), glReadPixels(0,0,width, height, GL_RGBA, GL_UNSIGNED_BYTE))
    image.save("./out.png", "PNG")
    return 0

# Fonction de génération des points de la fractale Julia
def julia_set(x, y, width, height, zoom, moveX, moveY, cX, cY):
    zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + moveX
    zy = (y - height / 2) / (0.5 * zoom * height) + moveY
    i = 0
    while zx * zx + zy * zy < 4 and i < max_iter:
        tmp = zx * zx - zy * zy + cX
        zy, zx = 2.0 * zx * zy + cY, tmp
        i += 1
    return i

# Fonction pour dessiner la fractale Julia
def draw_julia():
    global new_event
    if (new_event):
        glClear(GL_COLOR_BUFFER_BIT)  # Efface le buffer de l'écran
        glBegin(GL_POINTS)  # Démarre l'affichage des points
        #initialisation de la barre de progression
        printProgressBar(0, width-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
        # Parcours de chaque pixel de la fenêtre
        for x in range(width):
            for y in range(height):
                if(x == width / 2 and height / ch1 < y < height / ch1 * ch2) or (y == height / 2 and width / ch1 < x < width / ch1 * ch2):
                    # Peindre un crosshair pour ajouter de la précision
                    glColor3f(0.05,1,0)
                    glVertex2f(x / (width / 2) - 1, y / (height / 2) - 1)
                else :
                    i = julia_set(x, y, width, height, zoom, moveX, moveY, cX, cY)
                    # Définir la couleur en fonction du nombre d'itérations
                    glColor3f(i*colors[0]/max_iter,i*colors[1]/max_iter, i*colors[2]/max_iter)
                    glVertex2f(x / (width / 2) - 1, y / (height / 2) - 1)
            #actualisation de la barre de progression
            printProgressBar(x, width-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
        glEnd()
        new_event = False
    glutSwapBuffers()

# Initialisation OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fond noir
    glMatrixMode(GL_PROJECTION)  # Définit la matrice de projection
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)  # Définit l’espace de la fenêtre

# Callback pour gérer les touches du clavier
def keyboard(key, x, y):
    global zoom, moveX, moveY, cX, cY, new_event
    if key == b'i':  # Zoom avant
        zoom *= 10
        new_event = True
    elif key == b'k':  # Zoom arrière
        zoom1 = max(1.0, zoom / 10)
        if (zoom1 != zoom) :
            zoom = zoom1
            new_event = True
    elif key == b'q':  # Déplacer à gauche
        moveX -= 1 / zoom
        new_event = True
    elif key == b'd':  # Déplacer à droite
        moveX += 1 / zoom
        new_event = True
    elif key == b'z':  # Monter
        moveY += 1 / zoom
        new_event = True
    elif key == b's':  # Descendre
        moveY -= 1 / zoom
        new_event = True
    elif key == b'x':  # Quitter
        sys.exit()
    elif key == b'e':  # Exporter l'image
        export()

    glutPostRedisplay()  # Redessiner après chaque changement

# Fonction principale
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Double buffer et mode RGB
    glutInitWindowSize(width, height)  # Taille de la fenêtre
    glutCreateWindow(b"Ensemble de Julia - OpenGL")  # Titre de la fenêtre

    glutDisplayFunc(draw_julia)  # Fonction de dessin
    glutKeyboardFunc(keyboard)  # Fonction pour gérer les touches du clavier

    init() # appelle l'initialisation d'OpenGL

    glutMainLoop() # Démarre l'actualisation automatique pour chaque nouvel événement

# Définit le programme comme module
if __name__ == "__main__":
    main()
