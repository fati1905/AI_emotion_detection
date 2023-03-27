#Programme permettant de faire passer un fichier BMP dans un fichier csv
#Auteur: Antonin Carpentier & Fatima Ben Kadour
#Date: 21/03/2023

import os
import csv

def num(m):
    #retourne le nombre correspondant à 4 octets lus dans le fileier
    return m[0] + m[1] * 16 * 16 + m[2] * 16 ** 4 + m[3] * 16 ** 6

#readBMP(name,root) : lit un fichier BMP et retourne une liste contenant les pixels gris de l'image normalisés
def readBMP(name,root):
    file = open(root+"/"+name, "rb")
    file.seek(10)
    offset = num(file.read(4))
    file.seek(18)
    largeur = num(file.read(4))
    hauteur = num(file.read(4))
    file.seek(offset)
    gray = []
    for j in range(0, hauteur):
        for i in range(0, largeur):
            m = file.read(1)
            gray.append(m[0]/255)
    file.close()
    return gray


if __name__ == '__main__':
    print('Début création fichier csv')
    cpt = 0
    with open ("../Images2/train.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        for root, directories, files in os.walk("../"):
            for file in files:
                if (root.startswith('../Images2/train/')) and file.endswith('.bmp'):
                    gray = readBMP(file,root)
                    category = root.split('/')[-1]
                    toWrite = [cpt,file,category]
                    toWrite.extend(gray)
                    writer.writerow(toWrite)
                    cpt += 1


    print('Fin création fichier csv')