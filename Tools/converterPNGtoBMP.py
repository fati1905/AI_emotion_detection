#Programme permettant de faire passer une arborescence de fichiers PNG en BMP
#Auteur: Antonin Carpentier & Fatima Ben Kadour
#Date: 21/03/2023

from PIL import Image
import os

#conversion d'un fichier PNG en BMP
def convertirPNGtoBMP(fichier,root):
    img = Image.open(root+'/'+fichier)
    file_out = fichier.replace('.png','.bmp')
    img.save(root+'/'+file_out)
    img.close()


#méthode pour parcourir toutes l'arborescence d'un répertoire
def parcoursRepertoire(repertoire):
    for root, directories, files in os.walk(repertoire):
        for file in files:
            if (root.startswith('./Images/train/') or root.startswith("./Images/test/")) and file.endswith('.png'):
                convertirPNGtoBMP(file,root)
                os.remove(root+'/'+file)

if __name__ == '__main__':
    print('Début conversion')
    parcoursRepertoire('./')
    print('Fin conversion')