from tkinter import *  # La bibliothèque tkinter permet de créer une interface graphique
from tkinter import filedialog as file # Pour la boîte de dialogue "Ouvrir un fichier"
from tkinter import messagebox as msg # Pour afficher des boîtes de dialogue
from PIL import Image, ImageTk  # Importer Pillow pour la gestion des images

# Fonction pour créer un nouveau fichier
def nouveau_fichier():
    msg.showinfo("Nouveau", "Création d'un nouveau fichier.")

# Fonction pour ouvrir un fichier
def ouvrir_fichier():
    fichier = file.askopenfilename(title="Ouvrir un fichier", filetypes=[("Tous les fichiers", "*.*")])
    if fichier:
        print(f"Fichier sélectionné : {fichier}")
        msg.showinfo("Ouvrir", f"Fichier ouvert : {fichier}")

# Fonction pour enregistrer un fichier
def enregistrer_fichier():
    fichier = file.asksaveasfilename(title="Enregistrer le fichier", defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        print(f"Fichier enregistré : {fichier}")
        msg.showinfo("Enregistrer", f"Fichier enregistré sous : {fichier}")

# Fonction pour enregistrer sous
def enregistrer_sous():
    fichier = file.asksaveasfilename(title="Enregistrer sous", defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        print(f"Fichier enregistré sous : {fichier}")
        msg.showinfo("Enregistrer sous", f"Fichier enregistré sous : {fichier}")

# Fonction pour fermer la fenêtre
def fermer_fenetre():
    fenetre.quit()

# Créer la fenêtre principale
fenetre = Tk()
fenetre.title("Modélisation des graphes")
fenetre.geometry("500x500")
fenetre.minsize(480, 360)
fenetre.resizable(height=False, width=False)
fenetre.config(background='greenyellow')

# Définir une icône pour l'application
fenetre.iconbitmap("E:/Projects/Projet_Algorithme_de_graphe/Icons/Bonjour.ico")

# Créer une barre de menus
menu_bar = Menu(fenetre)

# Créer les sous-menus
menu_fichier = Menu(menu_bar, tearoff=0)
menu_creation = Menu(menu_bar, tearoff=0)
menu_affichage = Menu(menu_bar, tearoff=0)
menu_exe = Menu(menu_bar, tearoff=0)
menu_edition = Menu(menu_bar, tearoff=0)

# Charger les icônes pour les sous-menus (assurez-vous que les chemins sont corrects)
# Utiliser Pillow pour charger les icônes
icon_nouveau = ImageTk.PhotoImage(Image.open("Icons/nouveau.png").resize((20, 20)))
icon_ouvrir = ImageTk.PhotoImage(Image.open("Icons/ouvrir.png").resize((20, 20)))
icon_enregistrer = ImageTk.PhotoImage(Image.open("Icons/enregistrer.png").resize((20, 20)))
icon_enregistrer_sous = ImageTk.PhotoImage(Image.open("Icons/enregistrer_sous.png").resize((20, 20)))
icon_fermer = ImageTk.PhotoImage(Image.open("Icons/fermer.png").resize((20, 20)))

# Ajouter des options au sous-menu "Fichier" avec des icônes et des actions
menu_fichier.add_command(label="Nouveau", image=icon_nouveau, compound=LEFT, command=nouveau_fichier)  
menu_fichier.add_command(label="Ouvrir", image=icon_ouvrir, compound=LEFT, command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", image=icon_enregistrer, compound=LEFT, command=enregistrer_fichier)
menu_fichier.add_command(label="Enregistrer sous", image=icon_enregistrer_sous, compound=LEFT, command=enregistrer_sous)
menu_fichier.add_separator()
menu_fichier.add_command(label="Fermer", image=icon_fermer, compound=LEFT, command=fermer_fenetre)

# Ajout d'options aux autres sous-menus (sans icônes dans cet exemple)
menu_creation.add_command(label="Sommet")  
menu_creation.add_command(label="Arête")  
menu_affichage.add_command(label="Graphe")  
menu_affichage.add_command(label="Chaînes")  
menu_affichage.add_command(label="Matrices")  
menu_exe.add_command(label="Plus court chemin")  
menu_exe.add_command(label="Coloration")  
menu_edition.add_command(label="Graphe")

# Incorporation des sous-menus dans la barre de menus
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_bar.add_cascade(label="Création", menu=menu_creation)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)
menu_bar.add_cascade(label="Exécution", menu=menu_exe)
menu_bar.add_cascade(label="Édition", menu=menu_edition)

# Affecter la barre de menus à la fenêtre principale
fenetre.config(menu=menu_bar)

# Lancement de la boucle principale
fenetre.mainloop()