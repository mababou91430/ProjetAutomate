import tkinter as tk
import os
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
    print(fichier_chemin)



def afficher_tableau():
    # Définition des données avec colonne États (E/S) et Étapes
    headers = ["E/S", "État", "a", "b", "c"]
    data =   [
        ["E", "0", "0,1", "0,4", "0"],
        ["", "1", "--", "--", "2"],
        ["", "2", "--", "3", "--"],
        ["S", "3", "3", "--", "--"],
        ["S", "4", "--", "--", "2"],
    ]
    
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


if __name__ == "__main__":
    #print(fichier_choix())
    afficher_tableau()
