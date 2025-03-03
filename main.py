import tkinter as tk
from tkinter import ttk
from tabulate import tabulate

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
    afficher_tableau()
