import Network

nbImages_apprises = 0
nbImages_csv = 0

if __name__ == '__main__':
    print('Début création réseau')
    network = Network.Network(0.4)
    network.addLayer(2304)
    network.addLayer(20)
    network.addLayer(16)
    network.addLayer(10)
    network.addLayer(8)
    network.addLayer(2)
    print('Fin création réseau')

    csvfile = open("./Images/test.csv", "r")
    nbImages_csv = len(csvfile.readlines())
    csvfile.seek(0)  # on revient au début du fichier
    network.setPictures(csvfile)
    print("Nombre d'images : " + str(len(network.pictures)))
    csvfile.close()

    for i in range(0, 2000):
        print("\ntour " + str(i))

        # affiche les poids de la dernière couche
        print("Poids de la dernière couche : ")
        for neuron in network.layers[-1].neurons:
            print(str(neuron.weights[1]))

        for j in range(0, len(network.pictures)):
            network.chosePicture(j)
            network.propagation()
            network.putError(j)
            network.clearLists()

        nbImages_apprises = len(network.pictures) - len(network.erroredPicture)
        print("\nNombre d'images apprises : " + str(nbImages_apprises))
        print("Nombre d'images non apprises : " + str(len(network.erroredPicture)))

        if len(network.erroredPicture) > len(network.pictures) * 0.5 // 10:
            print("Erreur")
            network.retropropagation()
            network.clearLists()
        else:
            print("**************** Learned !! *********************")
            # Import test data
            network.pictures.clear()
            network.clearLists()
            csvfile = open("./Images2/train.csv", "r")
            # Add them to the lisr
            network.setPictures(csvfile)

            false = 0
            for num in range(0, len(network.pictures)):
                network.chosePicture(int(num))
                network.propagation()
                print("picture type : " + str(network.category))
                if network.hasError():
                    if network.category == "happy":
                        print("--> sad")
                    else:
                        print("--> happy")
                    false += 1
                else:
                    if network.category == "happy":
                        print("--> happy")
                    else:
                        print("--> sad")

                network.clearLists()

            print("Nombre d'image totales :" + str(len(network.pictures)))
            print("nombre de réponse négatif :" + str(false))
            csvfile.close()
            break
        network.erroredPicture.clear()

    # affichage des sorties de la couche de sortie
    for neuron in network.layers[-1].neurons:
        print(neuron.output)
