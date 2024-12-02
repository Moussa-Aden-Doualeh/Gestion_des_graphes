from tkinter import *
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

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Gestion des graphes")
fenetre.geometry("800x600")
fenetre.config(bg="#FFFFFF")
fenetre.iconbitmap("Icons/Bonjour.ico")

# Barre de menus
barre_menu = Menu(fenetre)
fenetre.config(menu=barre_menu)

# Ajout des menus
barre_menu.add_command(label="Fichier")
barre_menu.add_command(label="Création")
barre_menu.add_command(label="Affichage")
barre_menu.add_command(label="Exécution")
barre_menu.add_command(label="Édition")

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