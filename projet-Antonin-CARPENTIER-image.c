#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define tailleTabChar 256

//--------------------------------TYPEDEF--------------------------------------------

typedef char string[tailleTabChar];

/**
 * @brief Structure alphabet, elle représente une cellule de notre alphabet, composée d'un pixel (r,g,b), son occurrence, sa probabilité, son entropie, son code, ainsi qu'un lien vers une potentielle prochaine lettre.
 *
 */
typedef struct Alphabet
{
    unsigned char pixel[3];   // les trois couleurs de notre pixel (unsigned pour pour que ça soit 1 octet)
    int occurrence;           // occurrence du pixel
    double probabilite;       // probabilité du pixel
    double entropie;          // entropie du pixel
    struct Alphabet *suivant; // lien vers la prochaine cellule (prochain pixel)
} Alphabet;

/**
 * @brief Structure qui va comporter chaque partie importante de la signature (basé sur le fichier du moodle sur les fichiers bmp). On peut y retrouver la taille de l'image (height, width), le nombre de pixel différent etc...
 *
 */
typedef struct Signature
{
    // HEADER (14 octets)
    char signature[3]; // 2 bytes : "BM"
    int tailleImage;   // 4 bytes : taille du fichier en octet
    // partie inutilisée
    int dataOffset; // 4 bytes : nombre d'octet avant le début de l'image (important)

    // INFOHEADER (40 octets)
    int size;       // 4 bytes : taille de l'info header(=40)
    int width;      // 4 bytes : taille largeur de l'image
    int height;     // 4 bytes : taille hauteur de l'image
    short planes;   // 2 bytes : nombre de plan dans l'image (=1)
    short bitCount; // 2 bytes : nombre de bits par pixel :
                    // 1 pour deux couleurs
                    // 4 pour 16 couleurs
                    // 8 pour 256 couleurs
                    // 16 pour 65536 couleurs
                    // 24 pour 16,8M de couleurs
    int compression;     // 4 bytes : 0 pour aucune, 1 pour RLE-8 et 2 pour RLE-4
    int imageSize;       // 4 bytes : taille de l'image en octet
    int XpixelsPerM;     // 4 bytes : résolution horizontale en pixel par mètre
    int YpixelsPerM;     // 4 bytes : résolution verticale en pixel par mètre
    int colorsUsed;      // 4 bytes : nombre de couleurs dans l'image
    int colorsImportant; // 4 bytes : nombre de couleurs "importantes" dans l'image (0 = toutes)
} Signature;

//--------------------------------FONCTIONS--------------------------------------------

/**
 * @brief Fonction permettant d'afficher le menu, ainsi que de faire le choix dans le menu.
 *
 * @return int le choix que l'utilisateur a fait
 */
int printMenu()
{

    int choix;
    printf("Menu :\n");
    printf("\t- Quitter le programme\t\t\t\t\t\t[0]\n");
    printf("\t- Afficher les pixels\t\t\t\t\t\t[1]\n");
    printf("\t- Afficher les informations d'un pixel en particulier \t\t[2]\n");
    printf("\t- Informations sur le fichier\t\t\t\t\t[3]\n");
    printf("\n[MON CHOIX] : ");

    scanf("%d", &choix);
    // Si le choix est invalide
    while (choix < 0 || choix > 3)
    {

        printf("[MON CHOIX] : ");
        scanf("%d", &choix);
    }
    system("clear");
    return choix;
}

/**
 * @brief Fonction permettant d'afficher tous les pixels présents dans notre alphabet, ainsi que leur occurrence, leur probabilité ou encore leur entropie.
 *
 * @param ensemble Notre alphabet / ensemble de pixel
 */
void afficherpix(Alphabet *ensemble)
{

    // Création d'un curseur pour le parcours de notre alphabet
    Alphabet *cursor = ensemble;
    // Tant que nous n'avons pas traité tous les éléments de notre alphabet nous continuons
    while (cursor != NULL)
    {

        printf("Pixel :\t\tr = %u\tg = %u\tb = %u\t\t|\t--> occurrence = %d\t|\t--> probabilité = %lf\t|\t--> entropie = %lf\n", cursor->pixel[0], cursor->pixel[1], cursor->pixel[2], cursor->occurrence, cursor->probabilite, cursor->entropie);
        cursor = cursor->suivant;
    }
}

/**
 * @brief Fonction qui affiche les caractéristique d'une lettre choisie
 *
 * @param cara la lettre que nous avons choisie
 * @param ensemble notre alphabet
 */
void printPixel(unsigned int pix[], Alphabet *ensemble)
{

    // nous créons un "curseur" qui nous permet de nous déplacer dans la liste sans la supprimer /  l'écraser
    Alphabet *cursor = ensemble;
    int flag = 0;
    // on va parcourir notre alphabet pour chercher notre pixel

    // ne fonctionne pas toujours, je ne sais pas pourquoi..
    while (cursor != NULL && flag == 0)
    {

        // Si nous trouvons le pixel, nous sortons de la boucle, sinon on continue
        if (pix[0] == (unsigned int)cursor->pixel[0] && pix[1] == (unsigned int)cursor->pixel[1] && pix[2] == (unsigned int)cursor->pixel[2])
        {

            flag = 1;
            break;
        }
        cursor = cursor->suivant;
    }

    // si nous le trouvons pas
    if (!flag)
    {

        printf("Le pixel que vous avez entré n'existe pas !\n");

        // si nous le trouvons
    }
    else
    {

        printf("Pixel :\t\tr = %u\tg = %u\tb = %u\t\t|\t--> occurrence = %d\t|\t--> probabilité = %lf\t|\t--> entropie = %lf\n", cursor->pixel[0], cursor->pixel[1], cursor->pixel[2], cursor->occurrence, cursor->probabilite, cursor->entropie);
    }
    printf("\n");
}

/**
 * @brief Fonction qui va lire la signature du fichier image (bmp) et la renvoyer
 *
 * @param fichier le fichier image que nous voulons lire
 * @return Signature la signature de l'image lue
 */
Signature readSignature(FILE *fichier)
{

    Signature signature;
    // HEADER
    // Lecture de la signature du fichier
    fread(signature.signature, 2, 1, fichier);

    // Lecture de la taille du fichier
    fread(&signature.tailleImage, 4, 1, fichier);

    // On se déplace 4 octets plus loin, soit l'espace inutilisé
    fseek(fichier, 4, SEEK_CUR);

    // Lecture de l'offset
    fread(&signature.dataOffset, 4, 1, fichier);

    // INFOHEADER
    // Lecture de la taille de l'info header
    fread(&signature.size, 4, 1, fichier);

    // Lecture de la largeur de l'image
    fread(&signature.width, 4, 1, fichier);

    // Lecture de la hauteur de l'image
    fread(&signature.height, 4, 1, fichier);

    // Lecture du nombre de plan de l'image
    fread(&signature.planes, 2, 1, fichier);

    // Lecture du nombre de bits par pixel
    fread(&signature.bitCount, 2, 1, fichier);

    // Lecture du type de compression
    fread(&signature.compression, 4, 1, fichier);

    // Lecture de la taille de l'image (en octet)
    fread(&signature.imageSize, 4, 1, fichier);

    // Lecture de la résolution horizontal en pixel par mètre
    fread(&signature.XpixelsPerM, 4, 1, fichier);

    // Lecture de la résolution vertical en pixel par mètre
    fread(&signature.YpixelsPerM, 4, 1, fichier);

    // Lecture du nombre de couleurs dans l'image
    fread(&signature.colorsUsed, 4, 1, fichier);

    // Lecture du nombre de couleurs importantes dans l'image
    fread(&signature.colorsImportant, 4, 1, fichier);

    return signature;
}

/**
 * @brief Fonction qui va ouvrir le fichier
 *
 * @return FILE* NULL si le fichier n'a pas réussi à s'ouvrir
 */
// FILE * ouvertureFichier(){

//     string saisi;
//     printf("\tQuel est le nom de votre image ?\n");
//     printf("\n[MON CHOIX] : ");
//     scanf("%s",saisi);
//     system("clear");
//     return fopen(saisi,"rb");
// }

/**
 * @brief Fonction qui va libérer toutes les cellules d'une liste
 *
 * @param ensemble notre alphabet
 */
void liberationListe(Alphabet *ensemble)
{

    // On parcourt toute la liste jusqu'au bout, puis en remontant nous libérons les cellules une à une
    if (ensemble != NULL)
    {

        liberationListe(ensemble->suivant);
        ensemble->suivant = NULL; // optionnel voire inutile mais je préfère pour être sûr
        free(ensemble);
    }
}

/**
 * @brief Fonction pour créer la liste de pixel différent
 *
 * @param ensemble notre ensemble de pixel
 * @param pix pixel à ajouter (ou augmenter l'occurrence)
 * @return Alphabet* l'ensemble actualisé
 */
Alphabet *initPixel(Alphabet *ensemble, Alphabet pix)
{

    Alphabet *cursor = ensemble;
    int flag = 0;
    while (cursor != NULL)
    {

        if (cursor->pixel[0] == pix.pixel[0] && cursor->pixel[1] == pix.pixel[1] && cursor->pixel[2] == pix.pixel[2])
        {

            flag = 1;
            break;
        }
        cursor = cursor->suivant;
    }
    if (flag)
    {

        cursor->occurrence += 1;

        return ensemble;
    }
    else
    {

        // Création d'un nouveau bloc
        Alphabet *newPixel = (Alphabet *)malloc(sizeof(Alphabet));

        // initialisation des différentes données
        newPixel->pixel[0] = pix.pixel[0];
        newPixel->pixel[1] = pix.pixel[1];
        newPixel->pixel[2] = pix.pixel[2];
        newPixel->occurrence = 1;
        newPixel->entropie = 0;
        newPixel->probabilite = 0;
        newPixel->suivant = ensemble;

        return newPixel;
    }
}

/**
 * @brief Fonction qui va mettre l'entropie pour chaque pixel dans notre alphabet
 *
 * @param ensemble notre alphabet
 * @return double l'entropie total, soit l'entropie de la source
 */
double setEntropie(Alphabet *ensemble)
{

    // nous créons un "curseur" qui nous permet de nous déplacer dans la liste sans la supprimer /  l'écraser
    Alphabet *cursor = ensemble;
    double entropieTotal = 0;

    while (cursor != NULL)
    {

        cursor->entropie = -log2(cursor->probabilite);
        entropieTotal += ((cursor->entropie) * (cursor->probabilite));
        cursor = cursor->suivant;
    }
    return entropieTotal;
}

/**
 * @brief Fonction qui va mettre la probabilité de chaque pixel dans l'alphabet
 *
 * @param ensemble notre alphabet
 * @param pixelDiff l'adresse d'une variable de type int (permet d'avoir le nombre de pixel différent dans le programme)
 * @return int le nombre total de pixel
 */
int setProba(Alphabet *ensemble, int *pixelDiff)
{

    // nombre total de lettre
    int total = 0;
    // nous créons un "curseur" qui nous permet de nous déplacer dans la liste sans la supprimer /  l'écraser
    Alphabet *cursor = ensemble;

    // boucle calculant le nombre total de pixel dans le fichier
    while (cursor != NULL)
    {

        total += cursor->occurrence;
        cursor = cursor->suivant;
    }

    // Après avoir calculé le nombre de pixel total, on se remet au début pour faire la probabilité.
    // On aurait pu faire le nombre de pixel total directement dans l'insertion d'un pixel
    cursor = ensemble;

    // On calcule la probabilité pour chaque pixel
    while (cursor != NULL)
    {

        cursor->probabilite = ((double)(cursor->occurrence)) / total;
        *(pixelDiff) += 1;
        cursor = cursor->suivant;
    }
    return total;
}

int main(int argc, char const *argv[])
{

    for (int t = 3000; t < 3995; t++)
    {

        int choix = 10, nbPixel = 0, nbPixelDiff = 0, saisiPix[3], decalage;
        // double entropie = 0;
        Signature signature;
        FILE *fichier = NULL;
        FILE *pixel_fichier = NULL;
        Alphabet *Ensemble = NULL, pix;
        double entry;
        string buffer;

        /***Récupération du nom de l'image ***/
        char str[10];
        string path = "Données/angry_bmp/im";
        sprintf(str, "%d", t);
        
        strcat(path, str);
        strcat(path,".bmp");
        printf("nom de l'image :%s\n", path);

        // Ouvrir l'image
        fichier = fopen(path,"rb");

        /**** Créer le nom du fichier ****/
        string filepath = "Données/angry_files/file";
        strcat(filepath, str);
        strcat(filepath,".txt");
        printf("nom du fichier :%s\n", filepath);

        //Créer le fichier
        pixel_fichier = fopen(filepath, "wb");

        if(pixel_fichier == NULL){
            fprintf(stderr, "[ERREUR] : Ouverture du fichierr\n");
            return 1;            
        }

        // Si le fichier n'a pu être ouvert, code erreur et on quitte le programme
        if (fichier == NULL)
        {

            fprintf(stderr, "[ERREUR] : Ouverture du fichier\n");
            return 1;
        }
        else
        {

            printf("Chargement de l'image\n");
            signature = readSignature(fichier);

            // on retourne au début du fichier et on se déplace juste après la signature (on la passe) pour avoir accès aux pixels
            rewind(fichier);
            fseek(fichier, signature.dataOffset, SEEK_CUR);

            // Vu que nous travaillons sur des fichiers bitmap, il faut savoir que la largeur doit être un multiple de 4, sinon le fichier met automatiquement des pixels noirs. De ce fait nous regardons le décalage qu'il y a (nombre d'octet que nous devrons passer à chaque ligne)
            decalage = signature.width % 4;

            for (int i = 0; i < signature.height; i++)
            {

                for (int j = 0; j < signature.width; j++)
                {

                    fread(&pix.pixel[2], 1, 1, fichier); // pixel bleu
                    fread(&pix.pixel[1], 1, 1, fichier); // pixel vert
                    fread(&pix.pixel[0], 1, 1, fichier); // pixel rouge
                    Ensemble = initPixel(Ensemble, pix);
                    entry = (double)(pix.pixel[1]+pix.pixel[0]+pix.pixel[2])/765;
                    fprintf(pixel_fichier, "%f ", entry);
                    //printf("pixel %d %d = r:%d g:%d b:%d, entry : %f\n", i, j, pix.pixel[0], pix.pixel[1], pix.pixel[2], entry);
                }
                // on passe les octets inutiles
                fread(buffer, decalage, 1, fichier);
            }

            nbPixel = setProba(Ensemble, &nbPixelDiff);
            printf("Il y a au total :\n\t- %d pixel au total\n\t- L'image fait %d x %d pixels\n\n", nbPixel, signature.width, signature.height);

            fclose(fichier);
            fclose(pixel_fichier);
            liberationListe(Ensemble);
        }
    }

    // while (choix){

    //     //J'aurais pu faire un switch, ce qui est bien plus logique, cependant je trouve ça beaucoup moins lisible, j'ai donc préféré faire une suite de if / else if

    //      //choix 1 : Pour afficher tout notre alphabet avec leurs données
    //     if (choix == 1){

    //         afficherpix(Ensemble);
    //     }

    //     //choix 2 : Pour afficher un seul pixel avec ses caractéristique (nombre d'occurrence, probabilité, ...)
    //     else if (choix == 2){

    //         printf("Veuillez entrer un pixel :\nR = ");
    //         scanf("%u", &saisiPix[0]);
    //         printf("G = ");
    //         scanf("%u", &saisiPix[1]);
    //         printf("B = ");
    //         scanf("%u", &saisiPix[3]);
    //         printPixel(saisiPix,Ensemble);

    //     }

    //     // choix 3 : Pour afficher les informations sur le fichier
    //     else if (choix == 3){

    //         printf("Il y a au total :\n\t- %d pixel différents\n\t- %d pixel au total\n\t- l'entropie de la source est %lf\n\t- L'image fait %d x %d pixels\n\n",nbPixelDiff,nbPixel,entropie,signature.width,signature.height);
    //     }

    //     choix = printMenu();
    // }
    // printf("Vous avez quitté le programme.\nLibération de la liste\n");
    // if (Ensemble != NULL){

    //     liberationListe(Ensemble);
    // }
    return 0;
}
