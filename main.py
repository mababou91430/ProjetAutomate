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
        print(str(i)+". "+file)
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

def creation_tableau(fichier_choisi):
    alphabet = "abcdefghijklmnopqrstuvxyz"
    headers = []
    epsilon = False
    last_column = 0
    sorted_output = "Automate/sorted_output.txt"

    #test si l'automate contient le mot vide ep
    with open(sorted_output) as test_epsi, open(fichier_choisi,"r") as fc:
        for i in range(0,int(fc.readlines()[4])):
            if test_epsi.readline().split()[1] == "ep":
                epsilon = True

    #création du header en utilisant la première ligne de l'automate
    headers.extend(["E/S","E"])
    with open(fichier_choisi, "r") as paramètre:
        nb_symbole = paramètre.readline()
        print(nb_symbole)
        for i in range(0,int(nb_symbole)):
            headers.append(alphabet[i])
    
    #ajout d'une colonne en plus si l'automate contient ep
    if epsilon == True:
        headers.append("ep")
    last_column = len(headers) - 1
    data = [[]]
    i = 0

    #lecture de toutes les lignes du fichier trier de l'automate
    with open(sorted_output,"r") as sort:
        all_line = sort.readlines()
    with open(sorted_output,"r") as so, open(fichier_choisi,"r") as fc:
        lines = fc.readlines()
        first_time = True

        #On récupère tous les paramètres de l'automate
        nb_etat = lines[1]
        nb_symbole = lines[0]
        etat_initiaux = lines[2][:0] + lines[2][0 + 1:]
        etat_finaux = lines[3][:0] + lines[3][0 + 1:]
        nb_transition = lines[4]

        line = so.readline()

        #Définition de la liste 2D si l'automate contient ep
        if epsilon == True:
            for i in range(0,int(nb_etat)):
                temp = []
                for j in range(0,int(nb_symbole)+3):
                    temp.append(" ")
                if first_time == True:
                    data[0] = temp
                    first_time = False
                else:
                    data.append(temp)

        #Définition de la liste 2D si l'automate ne contient pas ep
        else:
            for i in range(0,int(nb_etat)):
                temp = []
                for j in range(0,int(nb_symbole)+2):
                    temp.append(" ")
                if first_time == True:
                    data[0] = temp
                    first_time = False
                else:
                    data.append(temp)

        #Remplissage de la première colonne des états d'entrées/sorties
        for w in range(0,int(nb_etat)):
            if str(w) in etat_initiaux and str(w) in etat_finaux:
                data[w][0] = "E/S"
                data[w][1] = str(w)
            elif str(w) in etat_initiaux and str(w) not in etat_finaux:
                data[w][0] = "E"
                data[w][1] = str(w)
            elif str(w) not in etat_initiaux and str(w) in etat_finaux:
                data[w][0] = "S"
                data[w][1] = str(w)
            elif str(w) not in etat_initiaux and str(w) not in etat_finaux:
                data[w][0] = " "
                data[w][1] = str(w)

        #Remplissage de Data avec tous les états d'arrivées 
        for z in range(0,int(nb_transition)):
            end = False
            splitline = line.split()
            if splitline[1] == "ep":
                data[int(splitline[0])][last_column] += splitline[2]
            else:
                data[int(splitline[0])][alphabet.find(splitline[1])+2] += splitline[2]
            if z != int(nb_transition)-1:
                temp_ajout = all_line[z+1].split()
                end = True
                if temp_ajout[0] == splitline[0] and temp_ajout[1] == splitline[1] and end == True and epsilon == False:
                    data[int(splitline[0])][alphabet.find(splitline[1])+2] += ","
                elif temp_ajout[0] == splitline[0] and temp_ajout[1] == splitline[1] and end == True and epsilon == True:
                    data[int(splitline[0])][last_column] += ","
            line = so.readline()
            
        #Remplissage de Data en changeant les état vide " " par "--" pour une meilleur compréhension du tableau
        for i in range(0,int(nb_etat)):
            for j in range(0,last_column+1):
                if data[i][j] == " ":
                    data[i][j] = "--"
    return data

def afficher(data,fichier_choisi):

    alphabet = "abcdefghijklmnopqrstuvxyz"
    headers = []
    epsilon = False
    sorted_output = "Automate/sorted_output.txt"

    #test si l'automate contient le mot vide ep
    with open(sorted_output) as test_epsi, open(fichier_choisi,"r") as fc:
        for i in range(0,int(fc.readlines()[4])):
            if test_epsi.readline().split()[1] == "ep":
                epsilon = True

    #création du header en utilisant la première ligne de l'automate
    headers.extend(["E/S","E"])
    with open(fichier_choisi, "r") as paramètre:
        nb_symbole = paramètre.readline()
        for i in range(0,int(nb_symbole)):
            headers.append(alphabet[i])

    if epsilon == True:
        headers.append("ep")

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
    
def afficherDeter(data,fichier_choisi):
    headers = []
    alphabet = "abcdefghijklmnopqrstuvxyz"
    headers.extend(["E/S","E"])
    with open(fichier_choisi, "r") as paramètre:
        nb_symbole = paramètre.readline()
        for i in range(0,int(nb_symbole)):
            headers.append(alphabet[i])

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

    

def supprimer_lignes_vides(nom_fichier):
    # Ouvrir le fichier en mode lecture
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        # Lire toutes les lignes du fichier
        lignes = fichier.readlines()

    # Filtrer les lignes non vides
    lignes_non_vides = [ligne for ligne in lignes if ligne.strip()]

    # Ouvrir le fichier en mode écriture pour écraser le contenu
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        # Écrire les lignes non vides dans le fichier
        fichier.writelines(lignes_non_vides)

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

def complementarisation(data,fichier_choisi):
    nb_etat = 0
    with open(fichier_choisi,"r") as f:
        nb_etat = int(f.readlines()[1])

    for i in range(0,nb_etat):
        if data[i][0] == "E/S":
            data[i][0] = "E"
        elif data[i][0] == "S":
            data[i][0] = "--"
        elif data[i][0] == "--":
            data[i][0] = "S"
        elif data[i][0] == "E":
            data[i][0] = "E/S"
    return data

def est_standard(data, fichier_choisi):
    """
    Vérifie si l'automate dont le tableau (data) est mis en paramètre est standardisé
    Retourne True si il est standadisé et False si ce n'est pas le cas 
    """
    entre = None
    nb_entres = 0
    for i in range (0, len(data)):
        if data[i][0]=="E" or data[i][0]=="E/S":
            entre = data[i][1]
            nb_entres += 1 
    if nb_entres > 1 :
        return False
    for i in range (0, len(data)):
        for j in data[i][2:]:
            if j == entre:
                return False
    return True 

def standardisation(data,fichier_choisi):
    """
    Prend en paramètre un automate sous forme d'un tableau
    Vérifie si l'automate est déjà standard, si non : standardise
    Retourne un tableau 2D de l'automate standard, directement utilisable dans le programme.
    """
    if est_standard(data, fichier_choisi):
        return data
    list_entres = []
    for i in range (0, len(data)):
        if data[i][0]=="E":
            list_entres.append(i)
            data[i][0]="--"
        elif data[i][0]=="E/S":
            list_entres.append(i)
            data[i][0]="S"
    nouv_ligne = ["E","i"] + ["--"] * (len(data[0])-2)
    for i in list_entres:
        for j in range (2,len(data[i])):
            if nouv_ligne[j]=="--":
                nouv_ligne[j]=data[i][j]
            elif data[i][j] not in nouv_ligne[j].split():
                nouv_ligne[j]+=','+ data[i][j]
    data.append(nouv_ligne)
    return data


def est_determinise(data, fichier_choisi):
    """
    Vérifie si l'automate dont le tableau (data) est mis en paramètre est déterminisé
    Retourne True si il est déterminisé et False si ce n'est pas le cas 
    """
    nb_entres = 0
    for i in range (0, len(data)):
        if data[i][0]=="E" or data[i][0]=="E/S":
            nb_entres += 1 
    if nb_entres > 1 :
        return False
    liste_etats = []
    for i in range (0, len(data)):
        liste_etats.append(data[i][1])
    for i in range (0, len(data)):
        for j in data[i][2:]:
            if j not in liste_etats and j!="--":
                return False
    return True

def est_determinise_et_complet (data, fichier_choisi):
    """
    Vérifie si l'automate dont le tableau (data) est mis en paramètre est complet (et détermisé) 
    Retourne True si il est complet (et déterminisé) et False si ce n'est pas le cas 
    """
    if not est_determinise(data,fichier_choisi):
        return False 
    for i in range (0, len(data)):
        for j in data [i][2:]:
            if j=='--':
                return False
    return True

def completer (data, fichier_choisi):
    """
    Prend en paramètre un automate sous forme d'un tableau
    Vérifie si l'automate est déterminisé (si non : déterminise) puis rends complet l'automate
    Retourne un tableau 2D de l'automate complet, directement utilisable dans le programme.
    """
    new_data = data
    if est_determinise_et_complet (new_data, fichier_choisi) :
        return new_data
    elif not est_determinise(new_data,fichier_choisi):
        new_data = determinisation(new_data,fichier_choisi)
    for i in range (0, len(new_data)):
        for j in range (2, len(new_data[i])):
            if new_data[i][j]=="--":
                new_data[i][j]="P"
    new_data.append(["--"] + ["P"] * (len(new_data[0])-1))
    return new_data

from collections import deque

def determinisation(data, fichier_choisi):
    """
    Permet de transformer un automate non déterministe en un automate déterministe avec un tableau 2D en entrée.
    Retourne un tableau 2D déterminisé, directement utilisable dans le programme.
    """
    
    # Récupération des paramètres de l'automate depuis le fichier
    with open(fichier_choisi, "r") as fichier:
        lines = fichier.readlines()
        nb_symbole = int(lines[0])  # Nombre de symboles de l'alphabet
        nb_etat = int(lines[1])  # Nombre d'états
    
    # Construction de l'alphabet en fonction du nombre de symboles
    alphabet = "abcdefghijklmnopqrstuvxyz"[:nb_symbole]

    # Détection des états initiaux
    etats_initiaux = set()
    for ligne in data:
        if ligne[0] in ["E", "E/S"]:
            etats_initiaux.add(ligne[1])

    # File pour parcourir les nouveaux états déterministes
    queue = deque()
    queue.append(",".join(sorted(etats_initiaux)))  # L'état initial est l'union des états initiaux

    # Structure pour le nouvel automate déterminisé
    nouveaux_etats = {}
    transitions = {}

    # Traitement de la déterminisation
    while queue:
        etat_actuel = queue.popleft()
        etats_composants = etat_actuel.split(",")

        # Initialisation des nouvelles transitions
        transitions[etat_actuel] = {symbole: set() for symbole in alphabet}

        for etat in etats_composants:
            etat = int(etat)  # Convertir en entier pour indexer data
            for i, symbole in enumerate(alphabet):
                if data[etat][i + 2] != "--":
                    transitions[etat_actuel][symbole].update(data[etat][i + 2].split(","))

        # Ajout des nouveaux états détectés dans la file
        for symbole in alphabet:
            nouvel_etat = ",".join(sorted(transitions[etat_actuel][symbole]))
            if nouvel_etat and nouvel_etat not in nouveaux_etats:
                queue.append(nouvel_etat)
                nouveaux_etats[nouvel_etat] = None

    # Création du tableau 2D déterminisé
    headers = ["E/S", "E"] + list(alphabet)
    data_determinise = []

    for etat in sorted(transitions.keys()):
        ligne = ["--", etat] + ["--"] * len(alphabet)

        # Définition des états initiaux et finaux
        etats_composants = etat.split(",")
        etat_initial = any(e in etats_initiaux for e in etats_composants)
        etat_final = any(data[int(e)][0] in ["S", "E/S"] for e in etats_composants)

        if etat_initial and etat_final:
            ligne[0] = "E/S"
        elif etat_initial:
            ligne[0] = "E"
        elif etat_final:
            ligne[0] = "S"

        # Remplissage des transitions
        for i, symbole in enumerate(alphabet):
            ligne[i + 2] = ",".join(sorted(transitions[etat][symbole])) if transitions[etat][symbole] else "--"

        data_determinise.append(ligne)

    return data_determinise


if __name__ == "__main__":
    filename = "Automate/sorted_output.txt"

    # regarde si un fichier "sorted_output.txt" existe
    if os.path.exists(filename):
        os.remove(filename)  # supprime le fichier si il existe
        print(f"{filename} has been deleted.")
    else:
        print(f"{filename} does not exist.")
    time.sleep(1)

    fichier_choisi = fichier_choix()#permet a l'utilisateur de choisir le fichier
    process_file(fichier_choisi)#crée un fichier text qui contient toutes les transitions trier dans l'ordre croissant
    supprimer_lignes_vides("Automate/sorted_output.txt")#supprime les lignes vides
    data = creation_tableau(fichier_choisi)#crée un tableau de transition sous forme d'une liste2D pour permettre une manipulation plus simple des données
    afficher(data,fichier_choisi)#affiche le tableau de donnée
    complémentaire = complementarisation(data,fichier_choisi)
    afficher(complémentaire,fichier_choisi)
    deter = determinisation(data,fichier_choisi)
    afficherDeter(deter,fichier_choisi)


    if os.path.exists(filename):
        os.remove(filename)  # supprime le fichier si il existe
        print(f"{filename} has been deleted.")
    else:
        print(f"{filename} does not exist.")
    time.sleep(1)


"""test"""
M = [['E','0','0','1'],['S','1','0','1']]
L = [['E','0','1',"--"],["--",'1','--','1']]
O = [['E','0','0','1'],['E/S','1','1','1']]
print(est_determinise_et_complet(M,'smt'))
print(est_determinise(L,'smt'))
print(est_determinise_et_complet(L,'smt'))
P = completer(L,'smt')
print(P)
print(est_determinise_et_complet(P,'smt'))
print(est_standard(M,'smh'))
print(est_standard(L,'smh'))
N = standardisation(M, 'smh')
print(N)
Q = standardisation(O, 'smh')
print (Q)
