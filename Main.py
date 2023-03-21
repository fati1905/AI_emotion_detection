#main du projet
#Auteur: Fatima BEN KADOOUR et Antonin CARPENTIER
#Date: 2023-05-21

import Network 
import file_reader as fr

if __name__ == '__main__':

    # Lecture des données
    print("Lecture des données")
    fr.read_all_files("Données")
    print("Fin de lecture des données")

    #création du réseau de neurones
    print("Création du réseau de neurones")
    network = Network.Network(0.3)
    network.setPicture(fr.angry_picture[0])

    # Ajout des couches
    network.addFirstLayer(0, 8)
    network.addLayer(1, 8)
    network.addLayer(2, 8)
    network.addLayer(3, 4)
    print("Fin de la création du réseau de neurones\n")

    print("nombre de layers: "+ str(len(network.layers)))
    #print le nombre de neurones dans chaque couche
    for layer in network.layers:
        print("Nombre de neurones dans la couche "+str(layer.id)+": "+str(len(layer.neurons)))

    # Propagation des données dans le réseau
    network.propage()

    for n in network.layers[-1].neurons:
        print("output : "+str(n.output))


    # print("Poids de chaque neurone:")
    # for l in network.layers:
    #     for n in l.neurons:
    #         print("Neurone "+str(n.id)+":"+str(n.weights)+"\n")

    # Affichage des erreurs
    print("Erreur: "+str(network.hasError()))

    if network.hasError():
        print("Erreur de classification")
        network.errorCalculus()
        #affichage des erreurs dans la première couche
        for l in network.layers:
            print("Couche "+str(l.id)+":")
            for n in l.neurons:
                print("Erreur du neurone "+str(n.id)+": "+str(n.error))


    
