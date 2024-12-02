from tkinter import *  # pour importer le bibliotheque de l'interface graphique.
from tkinter import ttk  # Pour le widget Notebook

#Creer la fenetre principale 
fenetre = Tk()

fenetre.title("Gestion des graphes")
fenetre.geometry("600x500")
fenetre.minsize(480, 360)
fenetre.resizable(height=False, width=False)
fenetre.config(background='#DDEEFF')
fenetre.iconbitmap("Icons/Bonjour.ico")

# Variable pour suivre le nombre d'onglets créés
compteur_onglets = 0

# Création du widget Notebook pour les onglets
onglets = ttk.Notebook(fenetre)
onglets.pack(expand=1, fill="both")  # Remplit la fenêtre principale

# Fonction pour créer un nouvel onglet
def creer_nouvel_onglet():
    global compteur_onglets
    compteur_onglets += 1
    
    # Nom de l'onglet
    nom_onglet = f"Fichier -{compteur_onglets}"
    
    # Création d'un cadre pour le contenu de l'onglet
    cadre_onglet = Frame(onglets, bg="#F5F5F5")
    cadre_onglet.pack(fill="both", expand=1)
    
    # Ajout du canvas dans l'onglet
    canvas = Canvas(cadre_onglet, bg="#DDEEFF", width=700, height=500, highlightthickness=1, highlightbackground="#CCCCCC")
    canvas.pack(expand=1, fill="both", padx=10, pady=10)
    
    # Ajout de l'onglet au Notebook
    onglets.add(cadre_onglet, text=nom_onglet)

# Créer une barre de menus
menu_bar = Menu(fenetre)

# Créer les sous-menus
menu_fichier = Menu(menu_bar, tearoff=0)  # Sous-menu Fichier
menu_creation = Menu(menu_bar, tearoff=0)  # Sous-menu Création
menu_affichage = Menu(menu_bar, tearoff=0)  # Sous-menu Affichage
menu_exe = Menu(menu_bar, tearoff=0)  # Sous-menu Exécution
menu_edition = Menu(menu_bar, tearoff=0)  # Sous-menu Édition

# Menu Fichier
menu_fichier.add_command(label="Nouveau", command=creer_nouvel_onglet, compound=LEFT)
menu_fichier.add_command(label="Ouvrir", compound=LEFT)
menu_fichier.add_command(label="Enregistrer", compound=LEFT)
menu_fichier.add_command(label="Enregistrer sous", compound=LEFT)
menu_fichier.add_command(label="Fermer", compound=LEFT)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quiter", command=fenetre.quit ,compound=LEFT)

# Menu Création
sous_menu_sommet = Menu(menu_creation, tearoff=0)
sous_menu_sommet.add_command(label="Ajouter Un Sommet", compound=LEFT)
sous_menu_sommet.add_command(label="Retirer Un Sommet", compound=LEFT)
menu_creation.add_cascade(label="Sommet", compound=LEFT, menu=sous_menu_sommet)

# Sous-menu Arête
sous_menu_arret = Menu(menu_creation, tearoff=0)

# Sous-menu pour les arêtes orientées
sous_menu_arret_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_orientee.add_command(label="Ajouter une arête orientée", compound=LEFT)
sous_menu_arret_orientee.add_command(label="Retirer une arête orientée", compound=LEFT)

# Sous-menu pour les arêtes non orientées
sous_menu_arret_non_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_non_orientee.add_command(label="Ajouter une arête non orientée", compound=LEFT)
sous_menu_arret_non_orientee.add_command(label="Retirer une arête non orientée", compound=LEFT)

# Ajouter les options des arêtes au menu principal
sous_menu_arret.add_cascade(label="Arête Orientée", menu=sous_menu_arret_orientee)
sous_menu_arret.add_cascade(label="Arête Non Orientée", menu=sous_menu_arret_non_orientee)
menu_creation.add_cascade(label="Arête", menu=sous_menu_arret)

# Menu Affichage
menu_affichage.add_command(label="Graphe", compound=LEFT)

sous_menu_chaine = Menu(menu_affichage, tearoff=0)
sous_menu_chaine.add_command(label="Chaine eulerienne", compound=LEFT)
sous_menu_chaine.add_command(label="Chaine hamiltonienne", compound=LEFT)
sous_menu_chaine.add_command(label="Chemins entre deux sommets", compound=LEFT)

menu_affichage.add_cascade(label="Chaines", compound=LEFT, menu=sous_menu_chaine)

sous_menu_matrice_ma = Menu(menu_affichage, tearoff=0)
sous_menu_matrice_ma.add_command(label="Matrice adjacents", compound=LEFT)
sous_menu_matrice_ma.add_command(label="Matrice incidence", compound=LEFT)
menu_affichage.add_cascade(label="Matrices", compound=LEFT, menu=sous_menu_matrice_ma)

# Menu Exécution et Édition
menu_exe.add_command(label="Plus court chemin")
menu_exe.add_command(label="Parcours en profondeurs")
menu_exe.add_command(label="Coloration")
menu_edition.add_command(label="Graphe")

# Ajouter la barre de menu à la fenêtre principale
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_bar.add_cascade(label="Création", menu=menu_creation)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)
menu_bar.add_cascade(label="Exécution", menu=menu_exe)
menu_bar.add_cascade(label="Édition", menu=menu_edition)

# Appliquer la barre de menu à la fenêtre
fenetre.config(menu=menu_bar)

fenetre.mainloop()