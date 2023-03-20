#include <algorithm>
#include <iostream>
#include <list>
#include <filesystem>
#include <string>
#include <fstream>
#include <cstdlib>
#include <ctime>

using namespace std;

class Neuron{
    public:
    int id; //L'identité du neurone
    double weight; //Le poids du neurone
    double h = 0; //L'entrée de la fonction sigmoide
    

    //Création d'un neurone
    Neuron(int id){
        this->id = id;
        weight = 0.5;
    }
};

class Layer{
    public:
    int id; //Numéro de couche
    list<Neuron> neurons;
    Layer *prevLayer = NULL;
    Layer *nextLayer = NULL;

    //Création d'un layer
    Layer(int id, int nbr){
        this->id = id;
        for(int i = 0; i < nbr; i++){
            Neuron neuron(i);
            neurons.push_front(neuron);
        }
    }

    //ajout d'un layer précédent
    void addPrevLayer(Layer *prevLayer){
        this->prevLayer = prevLayer;
    }

    //ajout d'un layer suivant
    void addNextLayer(Layer *nextLayer){
        this->nextLayer = nextLayer;
    }

    //récupération du ième neurone
    Neuron getNeuron(int i){
        int j = 0;
        for (Neuron neuron : neurons){
            if (j == i){
                return neuron;
            }
            j++;
        }
    }
    
};
class Network{
    public:
    list<Layer> layers;

    //Ajout d'un layer dans le réseau
    void addLayer(int id, int nbr){
        Layer layer(id, nbr);
        layers.push_back(layer);
    }

    //boucle pour afficher les neurones de chaque couche
    void displayNetwork(){
        for (Layer layer : layers){
            cout << "Layer " << layer.id << endl;
            for (Neuron neuron : layer.neurons){
                cout << "Neuron " << neuron.id << " : " << neuron.weight << endl;
            }
        }
    }

    //récupération de la layer numéro id
    Layer getLayer(int id){
        for (Layer layer : layers){
            if (layer.id == id){
                return layer;
            }
        }
    }


};

int main(int argc, char const *argv[])
{
    Network network;
    // network.addLayer(0, 100);
    // network.addLayer(1, 50);
    network.addLayer(0, 10);
    network.addLayer(1, 5);
    network.addLayer(2, 1);

    //ajout des layers prédécesseurs et suivants
    network.getLayer(0).addNextLayer(&network.getLayer(1)); // Layer 0 -> Layer 1
    network.getLayer(1).addPrevLayer(&network.getLayer(0)); // Layer 1 <- Layer 0
    network.getLayer(1).addNextLayer(&network.getLayer(2)); // Layer 1 -> Layer 2
    network.getLayer(2).addPrevLayer(&network.getLayer(1)); // Layer 2 <- Layer 1


    network.displayNetwork();

    return 0;
}
