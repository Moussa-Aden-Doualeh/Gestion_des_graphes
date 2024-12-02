from tkinter import *
from tkinter import messagebox as boite_dialogue # Pour la boîte de dialogue de confirmation
from tkinter import ttk  # Pour le widget Notebook
from PIL import Image, ImageTk, ImageDraw
import time

# Fonction pour créer une image avec une bordure arrondie
def creer_image_arrondie_avec_bordure(chemin_image, taille, couleur_bordure, largeur_bordure, rayon):
    """
    Cette fonction crée une image avec des coins arrondis et une bordure personnalisée.

    :param chemin_image: Chemin du fichier image.
    :param taille: Tuple (largeur, hauteur) pour redimensionner l'image.
    :param couleur_bordure: Couleur de la bordure (en format hexadécimal ou nom de couleur).
    :param largeur_bordure: Largeur de la bordure en pixels.
    :param rayon: Rayon des coins arrondis.
    :return: PhotoImage avec bordure arrondie.
    """
    # Charger et redimensionner l'image
    image = Image.open(chemin_image).resize(taille, Image.Resampling.LANCZOS)

    # Créer un masque pour les coins arrondis
    masque = Image.new("L", taille, 0)
    dessin = ImageDraw.Draw(masque)
    dessin.rounded_rectangle((0, 0, taille[0], taille[1]), radius=rayon, fill=255)

    # Appliquer le masque pour rendre l'image arrondie
    image_arrondie = Image.new("RGBA", taille, (0, 0, 0, 0))
    image_arrondie.paste(image, mask=masque)

    # Ajouter une bordure arrondie
    taille_bordure = (taille[0] + 2 * largeur_bordure, taille[1] + 2 * largeur_bordure)
    image_avec_bordure = Image.new("RGBA", taille_bordure, couleur_bordure)
    masque_arrondi = Image.new("L", taille_bordure, 0)
    dessin = ImageDraw.Draw(masque_arrondi)
    dessin.rounded_rectangle((0, 0, taille_bordure[0], taille_bordure[1]),
                              radius=rayon + largeur_bordure, fill=255)
    image_avec_bordure.paste(image_arrondie, (largeur_bordure, largeur_bordure), mask=masque)

    return ImageTk.PhotoImage(image_avec_bordure)

# Fonction pour mettre à jour la date et l'heure en temps réel
def mettre_a_jour_heure():
    
    heure_actuelle = time.strftime("%H:%M:%S")
    date_actuelle = time.strftime("%d/%m/%Y")
    etiquette_date.config(text=f"Le date : {date_actuelle} | Heure : {heure_actuelle}")
    fenetre.after(1000, mettre_a_jour_heure)

# Fonction pour animer un texte lettre par lettre
def animer_texte():
    global zone_animation
    texte = "  Gestion des graphes"
    zone_animation = Canvas(
        fenetre,
        bg="#FFFFFF",
        height=30,
        highlightthickness=0
    )
    zone_animation.place(relx=0.5, rely=0.3, anchor="n")

    lettres = []
    for i, lettre in enumerate(texte):
        lettre_id = zone_animation.create_text(
            20 + i * 15, -20, text=lettre, fill="black", font=("Lucida Calligraphy", 16, "bold")
        )
        lettres.append((lettre_id, 15))  # Position finale Y = 15

    def deplacer_lettres():
        termine = True
        for lettre_id, y_final in lettres:
            coords = zone_animation.coords(lettre_id)
            if coords[1] < y_final:
                zone_animation.move(lettre_id, 0, 2)
                termine = False
        if not termine:
            zone_animation.after(50, deplacer_lettres)

    deplacer_lettres()


def fermer_onglet():
    global elements_masques , etiquette_date , onglets , texte_bas_droite , cadre_photos

    # Vérifier s'il y a un onglet actif
    if onglets.index("end") > 0:  # Il y a au moins un onglet
        onglet_actif = onglets.index(onglets.select())
        onglets.forget(onglet_actif)

    # Restaurer les éléments si tous les onglets sont fermés
    if onglets.index("end") == 0 and elements_masques:
        # Restaurer les éléments
        zone_animation.place(relx=0.5, rely=0.3, anchor="n")
        etiquette_date.place(relx=1, y=5, anchor="ne")
        cadre_photos.place(relx=0.5, rely=0.5, anchor="center")
        texte_bas_droite.place(relx=1, rely=1, anchor="se", x=-20, y=-20)
        elements_masques = False  # Mettre à jour l'état

# Fonction pour quitter avec confirmation
def quitter_interface():
    # Demander confirmation avant de fermer
    reponse = boite_dialogue.askyesno("Confirmer la fermeture", "Voulez-vous vraiment quitter ?")
    
    if reponse:  # Si l'utilisateur choisit "Oui"
        fenetre.destroy()  # Fermer la fenêtre
    # Si l'utilisateur choisit "Non", rien ne se passe

# Le reste de votre code...

# Fonction qui sera appelée lorsque la croix X est cliquée
def femer_la_fenetre_X():
    quitter_interface()  # Appeler la fonction de confirmation
    
# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Gestion des graphes")
fenetre.geometry("800x600")
fenetre.config(bg="#FFF")
fenetre.iconbitmap("Icons/Bonjour.ico")
fenetre.protocol("WM_DELETE_WINDOW", femer_la_fenetre_X)

# Variable pour suivre le nombre d'onglets créés
compteur_onglets = 0

# Création du widget Notebook pour les onglets
onglets = ttk.Notebook(fenetre)
onglets.pack(expand=1, fill="both")  # Remplit la fenêtre principale

# Variable globale pour suivre l'état des éléments
elements_masques = False

def creer_nouvel_onglet():
    global compteur_onglets, elements_masques , cadre_photos

    # Incrémenter le compteur des onglets
    compteur_onglets += 1

    # Nom de l'onglet
    nom_onglet = f"Fichier - {compteur_onglets}"

    # Création d'un cadre pour le contenu de l'onglet
    cadre_onglet = Frame(onglets, bg="#F5F5F5")
    cadre_onglet.pack(fill="both", expand=1)

    # Ajout d'un canvas dans l'onglet
    canvas = Canvas(cadre_onglet, bg="#DDEEFF", width=700, height=500, highlightthickness=1, highlightbackground="#DDEEFF")
    canvas.pack(expand=1, fill="both", padx=10, pady=10)

    # Ajouter l'onglet au Notebook
    onglets.add(cadre_onglet, text=nom_onglet)

    # Masquer les éléments si nécessaire
    if not elements_masques:
        # Masquer les éléments
        zone_animation.place_forget()
        etiquette_date.place_forget()
        cadre_photos.place_forget()
        texte_bas_droite.place_forget()
        elements_masques = True  # Mettre à jour l'état

# Créer une barre de menus
menu_bar = Menu(fenetre)

# Appliquer la barre de menu à la fenêtre
fenetre.config(menu=menu_bar)

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
menu_fichier.add_command(label="Fermer", command=fermer_onglet, compound=LEFT)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quiter", command=quitter_interface, compound=LEFT)

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


sous_menu_chaine = Menu(menu_affichage, tearoff=0)
sous_menu_chaine.add_command(label="Chaine eulerienne", compound=LEFT)
sous_menu_chaine.add_command(label="Chaine hamiltonienne", compound=LEFT)

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

# Affichage de la date et de l'heure
etiquette_date = Label(fenetre, text="", font=("Arial", 10, "italic"), bg="#FFFFFF", anchor="e")
etiquette_date.place(relx=1, y=5, anchor="ne")
mettre_a_jour_heure()

# Zone des animations
animer_texte()

# Section des photos (gauche et droite)
cadre_photos = Frame(fenetre, bg="#FFFFFF")
cadre_photos.place(relx=0.5, rely=0.5, anchor="center")

# Taille de l'image et configuration des bordures
taille_image = (100, 100)  # Taille de l'image
largeur_bordure = 2  # Largeur de la bordure
rayon = 10  # Rayon pour les coins arrondis

# === Photo de gauche (bordure bleu clair) ===
cadre_photo_gauche = Frame(cadre_photos, bg="#FFFFFF")
cadre_photo_gauche.grid(row=0, column=0, padx=50)
try:
    photo_gauche = creer_image_arrondie_avec_bordure(
        "Icons/Moussa.png", taille_image, "#ADD8E6", largeur_bordure, rayon  # Couleur bleu clair
    )
    etiquette_photo_gauche = Label(cadre_photo_gauche, image=photo_gauche, bg="#FFFFFF")
    etiquette_photo_gauche.pack()
except Exception as e:
    Label(cadre_photo_gauche, text="Image introuvable", bg="#FFFFFF", fg="red").pack()

etiquette_nom_gauche = Label(cadre_photo_gauche, text="Moussa Aden Doualeh", bg="#FFFFFF", font=("Arial", 10, "italic"))
etiquette_nom_gauche.pack(pady=5)

# === Photo de droite (bordure rouge "tomato") ===
cadre_photo_droite = Frame(cadre_photos, bg="#FFFFFF")
cadre_photo_droite.grid(row=0, column=1, padx=50)
try:
    photo_droite = creer_image_arrondie_avec_bordure(
        "Icons/Mohamed.png", taille_image, "tomato", largeur_bordure, rayon  # Couleur rouge tomato
    )
    etiquette_photo_droite = Label(cadre_photo_droite, image=photo_droite, bg="#FFFFFF")
    etiquette_photo_droite.pack()
except Exception as e:
    Label(cadre_photo_droite, text="Image introuvable", bg="#FFFFFF", fg="red").pack()

etiquette_nom_droite = Label(cadre_photo_droite, text="Mohamed Abdi Daher", bg="#FFFFFF", font=("Arial", 10, "italic"))
etiquette_nom_droite.pack(pady=5)

# Texte en bas à droite
texte_bas_droite = Label(fenetre, text="Encadré par Madame Hawa Omar Ali", bg="#FFFFFF", font=("Arial", 10, "italic"))
texte_bas_droite.place(relx=1, rely=1, anchor="se", x=-20, y=-20)

# Lancer la boucle principale
fenetre.mainloop()