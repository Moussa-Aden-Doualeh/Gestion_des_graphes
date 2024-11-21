from tkinter import * # la bibliotheque tkinter permet de creer une interface graphique

# Créer une première fenêtre grâce à tkinter
fenetre = Tk() # La classe Tk() permet de creer une fenetre .

# Personnaliser cette fenêtre 
fenetre.title("Modelisation des graphes") # pour donner un titre de la fenetre principale.
fenetre.geometry("500x500") #Definir la dimension de la fenetre en longueur et en largeur .
fenetre.minsize(480,360) 
fenetre.resizable(height=FALSE,width=False) #L'option de la redimension (elle est desactiver).
fenetre.config(background='greenyellow') # La couleur du fond .

# Permet de definir un icon sur l'application .
fenetre.iconbitmap("E:\Projects\Projet_Algorithme_de_graphe/Icons/Bonjour.ico")  


# Créer une menu vide  lier a la fenetre principale .
menu_bar = Menu(fenetre)

# creer les sous menus avec la fonction Menu
# tearoff permet d'empecher l'utilisateur de detacher le menu dans une nouvelle fenetre .
menu_fichier = Menu(menu_bar, tearoff=0 ) 
menu_creation = Menu(menu_bar, tearoff=0)
menu_affichage = Menu(menu_bar, tearoff=0)
menu_exe = Menu(menu_bar, tearoff=0)
menu_edition = Menu(menu_bar, tearoff=0)

#Personaliser les menus deroulants en donnant des titres .
#La fonction add_cascade permet d'ajouter un element dans le barre de menu avec son nom .
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_bar.add_cascade(label="Création", menu=menu_creation)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)
menu_bar.add_cascade(label="Exécution", menu=menu_exe)
menu_bar.add_cascade(label="Edition", menu=menu_edition)

# Affecter la barre de menu dans la fenêtre pour afficher en haut de la fenetre .
fenetre.config(menu=menu_bar)

# Afficher la fenêtre grâce à une boucle
fenetre.mainloop()