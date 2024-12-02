from tkinter import *
from PIL import Image, ImageTk
import qrcode

def creer_code_qr(texte, taille=(100, 100)):
    """Génère un code QR et le redimensionne."""
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(texte)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img = img.resize(taille)
    return ImageTk.PhotoImage(img)

# Créer une fenêtre principale
fenetre = Tk()
fenetre.title("Animation QR Code")
fenetre.geometry("800x600")
fenetre.config(bg="#FFFFFF")

# Cadre pour l'animation
canvas = Canvas(fenetre, bg="#FFFFFF", width=800, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Générer les codes QR
qr1 = creer_code_qr("Moussa Aden Doualeh")
qr2 = creer_code_qr("Mohamed Abdi Daher")

# Ajouter les codes QR sur le canvas
x1, y1 = 100, 200
x2, y2 = 600, 200
qr1_id = canvas.create_image(x1, y1, image=qr1, anchor="center")
qr2_id = canvas.create_image(x2, y2, image=qr2, anchor="center")

# Vitesse de déplacement
dx1, dy1 = 2, 1
dx2, dy2 = -2, -1

def animer():
    global x1, y1, x2, y2, dx1, dy1, dx2, dy2

    # Déplacer QR 1
    x1 += dx1
    y1 += dy1
    if x1 <= 50 or x1 >= 750:
        dx1 = -dx1
    if y1 <= 50 or y1 >= 550:
        dy1 = -dy1
    canvas.coords(qr1_id, x1, y1)

    # Déplacer QR 2
    x2 += dx2
    y2 += dy2
    if x2 <= 50 or x2 >= 750:
        dx2 = -dx2
    if y2 <= 50 or y2 >= 550:
        dy2 = -dy2
    canvas.coords(qr2_id, x2, y2)

    # Appeler cette fonction après 20ms
    fenetre.after(20, animer)

# Lancer l'animation
animer()

# Boucle principale
fenetre.mainloop()
