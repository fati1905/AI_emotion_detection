#include <algorithm>
#include <iostream>
#include <list>
#include <filesystem>
#include <string>
#include <fstream>
#include <cstdlib>
#include <ctime>


using namespace std;

//Classe d'une image
class Picture{
    public:
    string category; //Angry, Happy, Fearful, disgusted
    double pix_entry[48][48]={0};
    double weight[48][48]={0};
};

// Classe d'un noeurone
class Neurone{
    public:
    int id = 0; //L'identité du neurone
    double h = 0; //L'entrée de la fonction sigmoide
    double y = 0; // La sortie de la fonction sigmoide
}

//Classe pour une couche
class Layer{
    public:
    list<Neurone> neurones;
    list<double> entries;
    list<double> weights;
    list<double> outputs;
    int nbr = 0; //Nombres de neurones 
    string category; //Catégorie des émotions

    //Ajouter les neurones dans la couche
    void addNeurones(int num){
        this->nbr = num;
        for(int i = 0; i < num; i++){

            Neurone neurone;
            neurone.id = neurone.id + i;

            neurones.push_front(neurone);
        }            
    }
    
    // Ajouter les entrées de la photos dans la premières couche 
    // Ajouter les poids de la photos dans la première couche 
    void upload_picture_to_network(Picture pic){
        
        for(int i = 0; i < 48; i++){

            for(int j = 0; j < 48; j++){

                entries.push_front(pic.pix_entry[i][j]);
                weights.push_front(pic.weight[i][j]);    
            }
        }
    }

    //Ajouter les sortie d'une couche dans les entrées d'une autre couche
    // void transfer_outputs_to_entries(Layer before_layer){
        
    //     for(int i = 0; i < )
    // }
};

// Fonction permet de lire les fichier contenant les entrées de chaques images
void read_entries(list<Picture>& list, string category, string pathfile, int nbpictures){
    Picture pic;
    double entry; // Lire les entrées dans le fichier
    double weight;
    int c1 = 0; //Les coordonnées de la matrice 
    int c2 = 0;

    //Lire les entrées des images de catégorie "ANGRY"
    for(int i=0; i < nbpictures; i++){
        //Récupérer le nom du fichier
        string num_file = to_string(i);
        pathfile = pathfile+num_file+".txt";
        //cout << pathfile << endl;

        // Créer un image
        pic.category = category;

        //Nous allons lire les entrées puis on va les convertir en double. Ensuites, on va les stocker dans le tableau pix_entry de l'image
        ifstream file;
        file.open(pathfile);

        //On lis les entrées qu'on stocke dans le tableau pix_entry et on remplis le tableau avec des poids compris entre -1 et 1
        while(file >> entry){
            // Les entrée
            pic.pix_entry[c1][c2] = entry;

            // Le poids de l'entrée
            weight = (double)rand()/RAND_MAX;
            weight = 2*weight -1;
            pic.weight[c1][c2] = weight;

            c2 += 1;

            if(c2 % 48 == 0){
                c2 = 0;
                c1 += 1;
            }

        }

        list.push_back(pic);
        file.close();
    }
}


// Fonction pour lire les fichiers contenant les entrées de chaques images
void read_all_entries(list<Picture>& happy, list<Picture>& disgusted, list<Picture>& angry, list<Picture>& fearful){
    
    // Lire les images dans le fichier "ANGRY"
    int nbpictures = 3995;
    string pathfile = "Données/angry_files/file";
    read_entries(angry, "Angry", pathfile, nbpictures);
    cout << "done with angry"<< endl;

    // Lire les images dans le fichier "HAPPY"
    nbpictures = 7215;
    pathfile = "Données/happy_files/file";
    read_entries(happy, "Happy", pathfile, nbpictures);
    cout << "done with happy"<< endl;

    // Lire les images dans le fichier "disugusted"
    nbpictures = 436;
    pathfile = "Données/disgusted_files/file";
    read_entries(disgusted, "Disgusted", pathfile, nbpictures);
    cout << "done with disgusted"<< endl;

    // Lire les images dans le fichier "Fearful"
    nbpictures = 4097;
    pathfile = "Données/fearful_files/file";
    read_entries(fearful, "Fearful", pathfile, nbpictures);
    cout << "done with fearful"<< endl;
}


int main(int argc, char const *argv[])
{
    list<Picture> pictures_happy;
    list<Picture> pictures_disgusted;
    list<Picture> pictures_angry;
    list<Picture> pictures_fearful;

    srand(time(0)); // Le temps courant
    read_all_entries(pictures_happy, pictures_disgusted, pictures_angry, pictures_fearful);
    
    //Créer les couches 
    Layer layer1;
    Layer layer2;
    Layer layer3;
    Layer layer4;
    Layer layer5;

    // Catégorie
    layer1.category = "Angry";
    layer2.category = "Angry";
    layer3.category = "Angry";
    layer4.category = "Angry";
    layer5.category = "Angry";

    //Ajouter les neurones dans les couches
    layer1.addNeurones(500);
    layer2.addNeurones(300);
    layer3.addNeurones(100);
    layer4.addNeurones(50);
    layer5.addNeurones(4);

    return 0;
}
