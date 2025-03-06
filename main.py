import tkinter as tk
import os
import time
from tkinter import ttk
from tabulate import tabulate


def fichier_choix():
    print("Quel fichier prendre parmis les suivants :")
    chemin_dossier="Automate"
    i = 1
    choix = None
    for file in os.listdir(chemin_dossier):
        print(str(i)+"."+file)
        i+=1

    while True :
        try:
                choix = input("Choix (exemple : 1): ").strip()  # Suppression des espaces
                if not choix:  # Vérifie si l'entrée est vide
                    raise ValueError("Entrée vide.")

                choix = int(choix) - 1  # Convertir en entier
                if 0 <= choix < i - 1:  # Vérifier que la valeur est valide
                    break
                else:
                    print("La valeur saisie est incorrecte.\nVeuillez choisir une valeur correcte.")
            
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre valide.")

    fichiers = sorted([f for f in os.listdir(chemin_dossier) if os.path.isfile(os.path.join(chemin_dossier, f))])
    fichier_chemin = os.path.abspath(os.path.join(chemin_dossier, fichiers[choix]))

    return(fichier_chemin)

def afficher_tableau(fichier_choisi):
    alphabet = "abcdefghijklmnopqrstuvxyz"
    headers = []

    #création du header en utilisant la première ligne de l'automate
    headers.extend(["E/S","E"])
    with open(fichier_choisi, "r") as paramètre:
        nb_symbole = paramètre.readline()
        print(nb_symbole)
        for i in range(0,int(nb_symbole)):
            headers.append(alphabet[i])

    data = [[]]
    i = 0
    with open("Automate/sorted_output.txt","r") as sort:
        all_line = sort.readlines()
    with open("Automate/sorted_output.txt","r") as so, open(fichier_choisi,"r") as fc:
        lines = fc.readlines()
        nb_etat = lines[0]
        etat_initiaux = lines[2][:0] + lines[2][0 + 1:]
        etat_finaux = lines[3][:0] + lines[3][0 + 1:]
        nb_transition = lines[4]
        print("etat_finaux :", etat_finaux)
        print("etat_initiaux :", etat_initiaux)
        line = so.readline()
        print(line)
        for j in range(0,int(nb_transition)-1):
            executer = False
            temp = []
            
            if splitline[0] in etat_initiaux and splitline[0] in etat_finaux and executer == False:
                temp.extend(["E/S",splitline[0]])
                executer = True
            elif splitline[0] in etat_initiaux and splitline[0] not in etat_finaux and executer == False:
                temp.extend(["E",splitline[0]])
                executer = True
            elif splitline[0] not in etat_initiaux and splitline[0] in etat_finaux and executer == False:
                temp.extend(["S",splitline[0]])
                executer = True
            elif splitline[0] not in etat_initiaux and splitline[0] not in etat_finaux and executer == False:
                temp.extend(["--",splitline[0]])
                executer = True
            temp.append(splitline[2])
            line = so.readline()
            data.append(temp)
            


    
    # Affichage du tableau dans le terminal avec bordures
    print(tabulate(data, headers, tablefmt="grid"))
    
    # Création de la fenêtre
    root = tk.Tk()
    root.title("Tableau des Transitions")
    
    # Création du tableau
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    tree = ttk.Treeview(frame, columns=headers, show='headings')
    
    # Configuration des colonnes
    for col in headers:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=80)
    
    # Ajout des données
    for row in data:
        tree.insert("", tk.END, values=row)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Lancer l'interface
    root.mainloop()

def process_file(input_file):
    """
    Lit un fichier text d'on le chemin a été donné en argument
    """
    
    
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # vérifie que le fichier fait plus de 5 lignes
        if len(lines) < 5:
            print("Le fichier contient moins de 5 lignes. Rien à traiter.")
            return None

        # ignore les 5 premières lignes puis extrait le reste 
        selected_lines = lines[5:]

        # tri les lignes extrait en fonction du numéro de l'état
        sorted_lines = sorted(selected_lines, key=lambda line: (line.split()[0] if len(line.split()) > 0 else "", line.split()[1] if len(line.split()) > 1 else ""))
        # crée un fichier text qui contenir l'output de la fonction
        directory = os.path.dirname(input_file)
        output_file = os.path.join(directory, "sorted_output.txt")

        # écrit le contenue dans le fichier output
        with open(output_file, "w", encoding="utf-8") as file:
            file.writelines(sorted_lines)

        print(f"Le contenu trié a été sauvegardé dans : {output_file}")
        return output_file

    except FileNotFoundError:
        print("Erreur : Fichier non trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    

if __name__ == "__main__":
    filename = "Automate/sorted_output.txt"

    # regarde si un fichier "sorted_output.txt" existe
    if os.path.exists(filename):
        os.remove(filename)  # supprime le fichier si il existe
        print(f"{filename} has been deleted.")
    else:
        print(f"{filename} does not exist.")
    time.sleep(1)

    fichier_choisi = fichier_choix()
    process_file(fichier_choisi)

    afficher_tableau(fichier_choisi)

