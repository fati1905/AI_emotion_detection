import os

# Ce fichier permet de lire les entrées des images.
# Nous avons des listes des images de toutes les catégories
angry_picture = []
happy_picture = []
fearful_picture = []
disgusted_picture = []


# Class qui représente les images
class Picture:
    def __init__(self, cat, n):
        # Category of the image either "Angry", "Happy", "disgusted" or "fearful"
        self.category = cat,
        # Les pixels de l'image
        self.pixel = []
        # Le nom de l'image
        self.name = n


# Read an image
def read_image(picture, pathfile):
    image = open(pathfile, "r")

    # Read doubles from the file

    for line in image:
        # delete spaces
        line = line.strip()

        # Turn a line to values ex : "0,99 0.78 0.8" becomes a list of : [0,99, 078, 0.8]
        line = line.split()
        #print("line:" + str(line))
        for d in line:
            # convert the value into a double
            value = float(d)
            picture.pixel.append(value)
            #print("value :" + str(value))


# This function reads all the files and adds them to the lists above
def read_all_files(path):  # The path is where all the directories of images are
    # Nous allons utiliser les valeurs globales
    global angry_picture, happy_picture, fearful_picture, disgusted_picture

    print("Start angry files")
    # ************************** Angry pictures *******************************
    # Read the files of angry folder
    dir_angry = path + str("/angry_files")

    # Get all the files inside the directory
    files = os.listdir(dir_angry)
    count = 0
    for file in files:
        if os.path.isfile(os.path.join(dir_angry, file)):
            # Create an image
            pic = Picture("Angry", file)
            print("file :"+str(file))
            read_image(pic, str("Données/angry_files/")+file)
            angry_picture.append(pic)
        count += 1
        #print("Just read an image")

    #print("Total images read :" + str(count))

    print("Start happy files")
    # ************************** Happy pictures *******************************
    # Read the files of angry folder
    dir_angry = path + str("/happy_files")

    # Read the files of happy folder
    files = os.listdir(dir_angry)
    count = 0
    for file in files:
        if os.path.isfile(os.path.join(dir_angry, file)):
            # Create an image
            pic = Picture("Happy", file)
            read_image(pic, str("Données/happy_files/") + file)
            happy_picture.append(pic)
        count += 1
        #print("Just read an image")

    #print("Total images read :" + str(count))

    print("Start fearful files")
    # ************************** Fearful pictures *******************************
    # Read the files of angry folder
    dir_angry = path + str("/fearful_files")

    # Read the files of fearful folder
    files = os.listdir(dir_angry)
    count = 0
    for file in files:
        if os.path.isfile(os.path.join(dir_angry, file)):
            # Create an image
            pic = Picture("Fearful", file)
            read_image(pic, str("Données/fearful_files/") + file)
            fearful_picture.append(pic)
        count += 1
        #print("Just read an image")

    #print("Total images read :" + str(count))
    print("Start disgust files")
    # ************************** Disgusted pictures *******************************
    # Read the files of angry folder
    dir_angry = path + str("/disgusted_files")

    # Read the files of disgusted folder
    files = os.listdir(dir_angry)
    count = 0
    for file in files:
        if os.path.isfile(os.path.join(dir_angry, file)):
            # Create an image
            pic = Picture("Disgusted", file)
            read_image(pic, str("Données/disgusted_files/") + file)
            disgusted_picture.append(pic)
        count += 1
        #print("Just read an image")

    #print("Total images read :" + str(count))


# Nous allons lire tous les fichiers dans les dossiers Données qui contient les dossiers de chaque emotions
read_all_files("Données")

print("angry : "+str(len(angry_picture)))
print("happy : "+str(len(happy_picture)))
print("fearful : "+str(len(fearful_picture)))
print("disgusted : "+str(len(disgusted_picture)))

