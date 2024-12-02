from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import time

# Configuration globale
COULEUR_FOND = "#FFFFFF"
TAILLE_IMAGE = (100, 100)
LARGEUR_BORDURE = 2
RAYON = 10
COULEUR_BORDURE_GAUCHE = "#ADD8E6"
COULEUR_BORDURE_DROITE = "tomato"


# --- Fonctions principales --- #

def creer_image_arrondie_avec_bordure(chemin_image, taille, couleur_bordure, largeur_bordure, rayon):
    """Créer une image avec des coins arrondis et une bordure personnalisée."""
    try:
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
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {chemin_image}: {e}")
        return None


def afficher_date_heure():
    """Met à jour la date et l'heure en temps réel."""
    heure_actuelle = time.strftime("%H:%M:%S")
    date_actuelle = time.strftime("%d/%m/%Y")
    etiquette_date.config(text=f"Date : {date_actuelle} | Heure : {heure_actuelle}")
    fenetre.after(1000, afficher_date_heure)


def animer_texte(texte, canvas, couleur="black"):
    """Anime un texte lettre par lettre dans un Canvas."""
    lettres = []
    for i, lettre in enumerate(texte):
        lettre_id = canvas.create_text(
            20 + i * 15, -20, text=lettre, fill=couleur, font=("Lucida Calligraphy", 16, "bold")
        )
        lettres.append((lettre_id, 15))  # Position finale Y = 15

    def deplacer_lettres():
        termine = True
        for lettre_id, y_final in lettres:
            coords = canvas.coords(lettre_id)
            if coords[1] < y_final:
                canvas.move(lettre_id, 0, 2)
                termine = False
        if not termine:
            canvas.after(50, deplacer_lettres)

    deplacer_lettres()


# --- Initialisation de l'interface --- #

# Fenêtre principale
fenetre = Tk()
fenetre.title("Gestion des graphes")
fenetre.geometry("800x600")
fenetre.config(bg=COULEUR_FOND)

# Barre de menus
barre_menu = Menu(fenetre)
fenetre.config(menu=barre_menu)
for label in ["Fichier", "Création", "Affichage", "Exécution", "Édition"]:
    barre_menu.add_command(label=label)

# Date et heure
etiquette_date = Label(fenetre, text="", font=("Arial", 10, "italic"), bg=COULEUR_FOND, anchor="e")
etiquette_date.place(relx=1, y=5, anchor="ne")
afficher_date_heure()

# Animation du texte
zone_animation = Canvas(fenetre, bg=COULEUR_FOND, height=30, highlightthickness=0)
zone_animation.place(relx=0.5, rely=0.3, anchor="n")
animer_texte("  Gestion des graphes ", zone_animation)

# Section des photos
cadre_photos = Frame(fenetre, bg=COULEUR_FOND)
cadre_photos.place(relx=0.5, rely=0.5, anchor="center")

# Photo gauche
cadre_photo_gauche = Frame(cadre_photos, bg=COULEUR_FOND)
cadre_photo_gauche.grid(row=0, column=0, padx=50)
photo_gauche = creer_image_arrondie_avec_bordure(
    "Icons/Moussa.png", TAILLE_IMAGE, COULEUR_BORDURE_GAUCHE, LARGEUR_BORDURE, RAYON
)
if photo_gauche:
    Label(cadre_photo_gauche, image=photo_gauche, bg=COULEUR_FOND).pack()
else:
    Label(cadre_photo_gauche, text="Image introuvable", bg=COULEUR_FOND, fg="red").pack()
Label(cadre_photo_gauche, text="Moussa Aden Doualeh", bg=COULEUR_FOND, font=("Arial", 10, "italic")).pack(pady=5)

# Photo droite
cadre_photo_droite = Frame(cadre_photos, bg=COULEUR_FOND)
cadre_photo_droite.grid(row=0, column=1, padx=50)
photo_droite = creer_image_arrondie_avec_bordure(
    "Icons/Mohamed.png", TAILLE_IMAGE, COULEUR_BORDURE_DROITE, LARGEUR_BORDURE, RAYON
)
if photo_droite:
    Label(cadre_photo_droite, image=photo_droite, bg=COULEUR_FOND).pack()
else:
    Label(cadre_photo_droite, text="Image introuvable", bg=COULEUR_FOND, fg="red").pack()
Label(cadre_photo_droite, text="Mohamed Abdi Daher", bg=COULEUR_FOND, font=("Arial", 10, "italic")).pack(pady=5)

# Texte en bas à droite
Label(fenetre, text="Encadré par Madame Hawa Omar Ali", bg=COULEUR_FOND, font=("Arial", 10, "italic")).place(
    relx=1, rely=1, anchor="se", x=-20, y=-20
)

# Lancer l'application
fenetre.mainloop()
