import pickle  # Utiliser pickle pour sérialiser les données
import os # pour interagir avec le systeme d'exploitation .
from tkinter import * # pour importer le bibliotheque de l'interface graphique .
from tkinter import simpledialog  as zone_dialogue # Pour les boîtes de dialogue de saisie
from tkinter import messagebox as boite_message # Pour les gestions de messages d'erreur et notifications
from tkinter import filedialog as dialogue_fichier  # Pour la boîte de dialogue "Ouvrir un fichier"
from PIL import Image, ImageTk  # Importer Pillow pour la gestion des images
import networkx as nx
import matplotlib.pyplot as plt

# Initialiser les variables globales pour suivre le nom du sommet
nom_sommet_courant = None  # Pour stocker le nom actuel du sommet
liste_sommets = []  # Liste pour stocker les sommets
cercles = []  # Liste pour stocker les cercles dessinés
textes_sommets = []  # Liste pour stocker les identifiants des textes des sommets
arcs = []  # Liste pour stocker les arêtes entre les sommets
chemin_fichier = None  # Variable pour suivre si le fichier a déjà été enregistré et son chemin

def incrementer_nom_sommet():
    global liste_sommets
    if not liste_sommets:  # Si la liste est vide, recommencer
        return zone_dialogue.askstring("Ajouter un sommet", 
                                        "Entrez la première lettre ou chiffre du sommet : ")
    
    # Récupérer les dernières valeurs de sommet
    derniers_noms = [s[0] for s in liste_sommets]
    # Trouver la plus grande valeur actuelle
    if all(nom.isdigit() for nom in derniers_noms):
        return str(max(map(int, derniers_noms)) + 1)
    else:
        return chr(max(map(ord, derniers_noms)) + 1)

def position_libre(x, y, liste_sommets):
    for sommet, (sx, sy) in liste_sommets:
        if (abs(sx - x) < 50 and abs(sy - y) < 50):  
            return False
    return True

def ajouter_sommet(canvas):
    global nom_sommet_courant
    
    nom_sommet_courant = incrementer_nom_sommet()  # Obtenir le nom courant
    if nom_sommet_courant is None or (not nom_sommet_courant.isalnum() or len(nom_sommet_courant) != 1):
        boite_message.showerror("Erreur", "Veuillez entrer une seule lettre alphabétique ou un chiffre.")
        return

    def lors_du_clic(event):
        global nom_sommet_courant
        x, y = event.x, event.y
        
        if not position_libre(x, y, liste_sommets):
            boite_message.showerror("Erreur", "Position trop proche d'un autre sommet.")
            return

        cercle = canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
        texte = canvas.create_text(x, y, text=nom_sommet_courant, fill="white")
        
        liste_sommets.append((nom_sommet_courant, (x, y)))
        cercles.append(cercle)  # Ajouter le cercle à la liste
        textes_sommets.append(texte)  # Ajouter le texte à la liste
        print(f"Sommet {nom_sommet_courant} ajouté à ({x}, {y})")

        nom_sommet_courant = incrementer_nom_sommet()  # Mettre à jour le nom pour le prochain sommet

    canvas.bind("<Button-1>", lors_du_clic)

def retirer_sommet(canvas):
    if not liste_sommets:  # Vérifier si la liste est vide
        boite_message.showerror("Erreur", "Aucun sommet à retirer.")
        return

    def lors_du_clic(event):
        x, y = event.x, event.y
        for i, (sommet, (sx, sy)) in enumerate(liste_sommets):
            if abs(sx - x) < 15 and abs(sy - y) < 15:  # Vérifier si le clic est sur un sommet
                canvas.delete(cercles[i])  # Supprimer le cercle du canvas
                canvas.delete(textes_sommets[i])  # Supprimer le texte du sommet

                # Supprimer toutes les arêtes associées à ce sommet
                arcs_a_supprimer = [arc for arc in arcs if sommet in arc[:2]]
                for arc in arcs_a_supprimer:
                    canvas.delete(arc[2])  # Supprimer la ligne de l'arête
                    arcs.remove(arc)  # Retirer l'arête de la liste

                del liste_sommets[i]  # Supprimer le sommet de la liste
                del cercles[i]  # Supprimer le cercle de la liste
                del textes_sommets[i]  # Supprimer le texte de la liste
                print(f"Sommet {sommet} retiré.")

                if not liste_sommets:  # Si la liste est vide après suppression
                    boite_message.showinfo("Notification", "Tous les sommets ont été supprimés.")
                    global nom_sommet_courant
                    nom_sommet_courant = None  # Réinitialiser pour demander à l'utilisateur de réinitialiser
                break

    canvas.bind("<Button-1>", lors_du_clic)

def ajouter_arrete(canvas):

    if len(liste_sommets) < 2:  # Vérifier s'il y a suffisamment de sommets
        boite_message.showerror("Erreur", "Vous devez ajouter au moins deux sommets avant d'ajouter une arête.")
        return

    selection_sommets = []  # Liste temporaire pour stocker les deux sommets sélectionnés

    def selectionner_sommet(event):
        x, y = event.x, event.y

        # Rechercher si le clic est sur un sommet existant
        for i, (sommet, (sx, sy)) in enumerate(liste_sommets):
            if abs(sx - x) < 15 and abs(sy - y) < 15:
                selection_sommets.append((sommet, (sx, sy)))

                # Si deux sommets sont sélectionnés, on crée une arête
                if len(selection_sommets) == 2:
                    sommet1, (x1, y1) = selection_sommets[0]
                    sommet2, (x2, y2) = selection_sommets[1]

                    # Vérifier si l'utilisateur essaie de créer une boucle (arête vers soi-même)
                    if sommet1 == sommet2:
                        boite_message.showerror("Erreur", "Impossible de créer une arête sur le même sommet (boucle).")
                    else:
                        # Vérifier que l'arête n'existe pas déjà (ni dans un sens ni dans l'autre)
                        if (sommet1, sommet2) in [(s1, s2) for s1, s2, _ in arcs] or \
                           (sommet2, sommet1) in [(s1, s2) for s1, s2, _ in arcs]:
                            boite_message.showerror("Erreur", "Une arête entre ces deux sommets existe déjà.")
                        else:
                            # Si pas d'erreur, on crée l'arête
                            ligne = canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                            arcs.append((sommet1, sommet2, ligne))  # Stocker l'arête
                            print(f"Arête ajoutée entre {sommet1} et {sommet2}")

                    # Après l'ajout ou l'erreur, on vide la liste de sélection pour recommencer
                    selection_sommets.clear()

                break

    canvas.bind("<Button-1>", selectionner_sommet)

def retirer_arrete(canvas):
    if not arcs:  # Vérifier si la liste des arêtes est vide dès le début
        boite_message.showinfo("Notification", "Il n'y a plus d'arêtes à retirer.")
        return

    selection_sommets = []  # Liste pour stocker les sommets sélectionnés

    def selectionner_sommet_pour_supprimer(event):
        x, y = event.x, event.y

        # Rechercher si le clic est sur un sommet existant
        for i, (sommet, (sx, sy)) in enumerate(liste_sommets):
            if abs(sx - x) < 15 and abs(sy - y) < 15:
                selection_sommets.append((sommet, (sx, sy)))

                # Si deux sommets sont sélectionnés, on tente de supprimer l'arête correspondante
                if len(selection_sommets) == 2:
                    sommet1, (x1, y1) = selection_sommets[0]
                    sommet2, (x2, y2) = selection_sommets[1]

                    # Chercher l'arête correspondante et la supprimer si elle existe
                    for j, (s1, s2, ligne) in enumerate(arcs):
                        if (s1, s2) == (sommet1, sommet2) or (s2, s1) == (sommet1, sommet2):
                            canvas.delete(ligne)  # Supprimer la ligne de l'arête du canvas
                            del arcs[j]  # Supprimer l'arête de la liste
                            print(f"Arête entre {sommet1} et {sommet2} supprimée.")
                            break
                    else:
                        boite_message.showerror("Erreur", "Aucune arête n'existe entre ces sommets.")

                    selection_sommets.clear()  # Réinitialiser la sélection après chaque suppression

                    # Vérifier s'il reste encore des arêtes après la suppression
                    if not arcs:
                        boite_message.showinfo("Notification", "Toutes les arêtes ont été retirées.")
                        canvas.unbind("<Button-1>")  # Désactiver l'événement de suppression
                        return

    # Liaison de l'événement de clic pour sélectionner les sommets à connecter
    canvas.bind("<Button-1>", selectionner_sommet_pour_supprimer)

# Fonction pour créer une nouvelle fenêtre indépendante (lorsque l'utilisateur clique sur "Nouveau")
def nouveau_fichier():
    global liste_sommets, cercles, arcs, nom_sommet_courant, chemin_fichier
    # Réinitialisation des variables globales
    liste_sommets = []
    cercles = []
    arcs = []
    nom_sommet_courant = None
    chemin_fichier = None  # Réinitialiser la variable chemin_fichier globale

    # Création d'une nouvelle fenêtre
    nouvelle_fenetre = Toplevel(fenetre)
    nouvelle_fenetre.title("Nouvelle Fenetre")
    # nouvelle_fenetre.chemin_fichier = None
   
    # Créer la fenêtre principale pour la nouvelle fenêtre
    creer_fenetre_principale(nouvelle_fenetre)
    nouvelle_fenetre.protocol("WM_DELETE_WINDOW", lambda: fermer_fenetre(nouvelle_fenetre))  # Appeler la fonction de fermeture
    

    nouvelle_fenetre.mainloop()

# Ajouter une fonction pour calculer la matrice d'adjacence
def afficher_matrice_adjacence():
    if not liste_sommets or not arcs:
        boite_message.showerror("Erreur", "Il faut d'abord créer un graphe avant d'afficher la matrice.")
        return

    # Initialiser une matrice de taille len(liste_sommets) x len(liste_sommets)
    n = len(liste_sommets)
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    
    # Remplir la matrice d'adjacence en fonction des arêtes
    for s1, s2, _ in arcs:
        i = next(i for i, (nom, _) in enumerate(liste_sommets) if nom == s1)
        j = next(i for i, (nom, _) in enumerate(liste_sommets) if nom == s2)
        matrice[i][j] = 1
        matrice[j][i] = 1  # Graphe non orienté, donc symétrique

    # Afficher la matrice dans le frame de droite
    afficher_matrice(matrice, "Matrice d'Adjacence")

# Fonction pour afficher la matrice d'incidence
def afficher_matrice_incidence():
    if not liste_sommets or not arcs:
        boite_message.showerror("Erreur", "Il faut d'abord créer un graphe avant d'afficher la matrice.")
        return

    # Initialiser une matrice de taille len(liste_sommets) x len(arcs)
    n = len(liste_sommets)  # Nombre de sommets
    m = len(arcs)           # Nombre d'arcs (arêtes)
    matrice = [[0 for _ in range(m)] for _ in range(n)]
    
    # Remplir la matrice d'incidence en fonction des arêtes
    for k, (s1, s2, _) in enumerate(arcs):
        i = next(i for i, (nom, _) in enumerate(liste_sommets) if nom == s1)
        j = next(i for i, (nom, _) in enumerate(liste_sommets) if nom == s2)
        
        matrice[i][k] = 1  # Le sommet de départ de l'arête
        matrice[j][k] = 1  # Le sommet d'arrivée de l'arête, pour graphe non orienté

    # Afficher la matrice dans le frame de droite
    afficher_matrice(matrice, "Matrice d'Incidence")

# Fonction pour afficher les matrices dans le frame de droite
def afficher_matrice(matrice, titre):
    frame_matrice = Frame(fenetre, bg="#DDEEFF", bd=2)
    frame_matrice.place(x=550, y=60)
    
    # Affichage du titre de la matrice
    label_titre = Label(frame_matrice, text=titre, bg="#DDEEFF", font=("Arial", 14, "bold"))
    label_titre.grid(row=0, column=0, columnspan=len(matrice[0]), pady=10)

    # Affichage de la matrice sous forme de tableau
    for i, ligne in enumerate(matrice):
        for j, valeur in enumerate(ligne):
            Label(frame_matrice, text=valeur, width=4, height=2, relief="solid").grid(row=i+1, column=j)

# def verifier_chaine_eulerienne():
#     # Calculer les degrés de chaque sommet
#     degres = {sommet: 0 for sommet, _ in liste_sommets}  # Initialiser les degrés à zéro

#     # Parcourir chaque arête pour augmenter les degrés des sommets
#     for sommet1, sommet2, _ in arcs:
#         if sommet1 in degres:
#             degres[sommet1] += 1
#         if sommet2 in degres:
#             degres[sommet2] += 1

#     # Compter le nombre de sommets de degré impair
#     sommets_degre_impair = [sommet for sommet, degre in degres.items() if degre % 2 != 0]

#     # Vérifier la condition pour une chaîne eulérienne
#     if len(sommets_degre_impair) == 0:
#         boite_message.showinfo("Résultat", "Le graphe possède un cycle eulérien (tous les sommets sont de degré pair).")
#     elif len(sommets_degre_impair) == 2:
#         boite_message.showinfo("Résultat", "Le graphe possède une chaîne eulérienne (deux sommets de degré impair).")
#     else:
#         boite_message.showinfo("Résultat", "Le graphe ne possède pas de chaîne eulérienne (plus de deux sommets de degré impair).")

def chaine_eulerienne():
    # Créer un graphe vide
    G = nx.Graph()
    
    # Ajouter les sommets et arêtes à partir des variables globales
    for sommet, _ in liste_sommets:
        G.add_node(sommet)
    for sommet1, sommet2, _ in arcs:
        G.add_edge(sommet1, sommet2)
    
    # Vérifier le nombre de sommets de degré impair
    sommets_impairs = [sommet for sommet in G.nodes if G.degree(sommet) % 2 != 0]

    if len(sommets_impairs) == 2:  # Condition d'une chaîne eulérienne
        # Trouver la chaîne eulérienne et l'afficher
        chaine = list(nx.eulerian_path(G))
        chemin_str = " -> ".join(f"{u}-{v}" for u, v in chaine)
        boite_message.showinfo("Chaîne eulérienne", f"Chaîne eulérienne trouvée : {chemin_str}")
    elif len(sommets_impairs) == 0 and nx.is_connected(G):
        boite_message.showinfo("Information", "Ce graphe contient un cycle eulérien.")
    else:
        boite_message.showinfo("Information", "Pas de chaîne eulérienne trouvée.")

def chemin_entre_deux_sommets():
    # Demander au user de saisir les sommets de départ et d'arrivée
    sommet_depart = zone_dialogue.askstring("Sommet de départ", "Entrez le sommet de départ :")
    sommet_arrive = zone_dialogue.askstring("Sommet d'arrivée", "Entrez le sommet d'arrivée :")

    # Vérifier la validité des sommets
    if sommet_depart == sommet_arrive:
        boite_message.showerror("Erreur", "Les deux sommets doivent être différents.")
        return
    if sommet_depart not in [s for s, _ in liste_sommets] or sommet_arrive not in [s for s, _ in liste_sommets]:
        boite_message.showerror("Erreur", "Veuillez entrer des sommets présents dans le graphe.")
        return

    # Créer un graphe temporaire
    G = nx.Graph()
    for sommet, _ in liste_sommets:
        G.add_node(sommet)
    for sommet1, sommet2, _ in arcs:
        G.add_edge(sommet1, sommet2)

    # Vérifier l'existence d'un chemin et l'afficher
    try:
        chemin = nx.shortest_path(G, source=sommet_depart, target=sommet_arrive)
        chemin_str = " -> ".join(chemin)
        boite_message.showinfo("Chemin trouvé", f"Chemin entre {sommet_depart} et {sommet_arrive} : {chemin_str}")
    except nx.NetworkXNoPath:
        boite_message.showinfo("Pas de chemin", f"Aucun chemin entre {sommet_depart} et {sommet_arrive}.")

def afficher_graphe():
    # Ouvrir une boîte de dialogue pour sélectionner le fichier de graphe
    fichier = dialogue_fichier.askopenfilename(
        title="Afficher un graphe enregistré",
        filetypes=[("Python Files", "*.py"), ("All files", "*.*")]
    )
    
    if not fichier:
        boite_message.showerror("Erreur", "Aucun fichier sélectionné.")
        return

    # Charger le fichier sélectionné contenant le graphe avec pickle
    with open(fichier, 'rb') as f:
        data = pickle.load(f)

    # Créer le graphe NetworkX à partir des données
    G = nx.Graph()
    for nom, pos in data["sommets"]:
        G.add_node(nom, pos=pos)  # Ajout des sommets avec les positions enregistrées
    for s1, s2 in data["arcs"]:
        G.add_edge(s1, s2)

    # Récupérer les positions des sommets pour l'affichage, en utilisant les positions enregistrées
    pos = nx.get_node_attributes(G, 'pos')

    # Afficher les positions pour vérification
    print("Positions des sommets chargées :", pos)

    # Afficher le graphe avec Matplotlib en utilisant les positions sauvegardées
    plt.figure(figsize=(5, 5))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', 
            node_size=500, font_color='black', edge_color='gray')
    plt.title("Graphe enregistré")
    plt.show()

def ouvrir_fichier(canvas):
    # Demander à l'utilisateur de choisir un fichier
    fichier = dialogue_fichier.askopenfilename(
        title="Ouvrir un fichier",
        filetypes=[
            ("Python Files", "*.py"),
            ("Image Files", "*.png"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("All files", "*.*")
        ]
    )
    
    if fichier:
        # Vérifier l'extension du fichier
        if fichier.endswith('.py'):
            # Ouvrir le fichier .py contenant les données du graphe
            with open(fichier, 'rb') as f:
                data = pickle.load(f)

            # Effacer les éléments actuels du canvas
            for cercle in cercles:
                canvas.delete(cercle)
            for texte in textes_sommets:
                canvas.delete(texte)
            for _, _, arc in arcs:
                canvas.delete(arc)

            liste_sommets.clear()
            cercles.clear()
            textes_sommets.clear()
            arcs.clear()

            # Charger les sommets
            for nom, (x, y) in data["sommets"]:
                cercle = canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
                texte = canvas.create_text(x, y, text=nom, fill="white")
                liste_sommets.append((nom, (x, y)))
                cercles.append(cercle)
                textes_sommets.append(texte)

            # Charger les arêtes
            for s1, s2 in data["arcs"]:
                x1, y1 = next(pos for sommet, pos in liste_sommets if sommet == s1)
                x2, y2 = next(pos for sommet, pos in liste_sommets if sommet == s2)
                ligne = canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                arcs.append((s1, s2, ligne))

        elif fichier.endswith('.png'):
            ouvrir_image(fichier)
        elif fichier.endswith('.pdf'):
            ouvrir_pdf(fichier)
        elif fichier.endswith('.docx'):
            ouvrir_docx(fichier)
        else:
            boite_message.showerror("Erreur", "Format de fichier non pris en charge!")

def ouvrir_image(fichier):
    img = Image.open(fichier)
    img.show()  # Ouvre l'image dans le visualiseur d'images par défaut

def ouvrir_pdf(fichier):
    os.startfile(fichier)  # Cela ouvrira le PDF dans le visualiseur par défaut

def ouvrir_docx(fichier):
    os.startfile(fichier)  # Cela ouvrira le document Word dans le visualiseur par défaut

def enregistrer_fichier(canvas, fenetre_actuelle):
    if fenetre_actuelle.chemin_fichier is None:
        fenetre_actuelle.chemin_fichier = dialogue_fichier.asksaveasfilename(
            title="Enregistrer le graphe", defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All files", "*.*")]
        )

    if fenetre_actuelle.chemin_fichier:
        data = {
            "sommets": [(nom, pos) for nom, pos in liste_sommets],
            "arcs": [(s1, s2) for s1, s2, _ in arcs]
        }
        with open(fenetre_actuelle.chemin_fichier, 'wb') as f:
            pickle.dump(data, f)

        boite_message.showinfo("Enregistrement réussi", f"Graphe enregistré sous : {fenetre_actuelle.chemin_fichier}")

def enregistrer_sous(canvas, fenetre_actuelle):
    nouveau_fichier = dialogue_fichier.asksaveasfilename(
        title="Enregistrer sous", defaultextension=".py",
        filetypes=[("Python Files", "*.py"), ("All files", "*.*")]
    )

    if nouveau_fichier:
        fenetre_actuelle.chemin_fichier = nouveau_fichier
        data = {
            "sommets": [(nom, pos) for nom, pos in liste_sommets],
            "arcs": [(s1, s2) for s1, s2, _ in arcs]
        }
        with open(fenetre_actuelle.chemin_fichier, 'wb') as f:
            pickle.dump(data, f)

        boite_message.showinfo("Enregistrement réussi", f"Graphe enregistré sous : {fenetre_actuelle.chemin_fichier}")

# Fonction pour fermer la fenêtre avec confirmation
def fermer_fenetre(fenetre):
    reponse = boite_message.askyesno("Fermer", "Voulez-vous vraiment fermer la fenêtre ?")
    if reponse:
        fenetre.destroy()

# Fonction pour créer la fenêtre principale
def creer_fenetre_principale(fenetre): 
    fenetre.geometry("800x600")
    fenetre.minsize(480, 360)
    # fenetre.resizable(height=False, width=False)  
    fenetre.config(background='#DDEEFF')  
    fenetre.iconbitmap("Icons/Bonjour.ico")

    fenetre.chemin_fichier = None
    
    # Créer un cadre principal pour contenir les deux zones
    cadre_principal = Frame(fenetre)
    cadre_principal.pack(fill="both", expand=True)

    # Zone canvas à gauche
    cadre_canvas = Frame(cadre_principal, width=400, height=600 , bg='#fdd9f0')
    cadre_canvas.pack(side="left", fill="both", expand=True)

    # Zone d'affichage des résultats à droite
    cadre_resultats = Frame(cadre_principal, bg='#DDEEFF', bd=3, relief="solid", 
                    highlightbackground="white", highlightthickness=3, width=400, height=600)
    cadre_resultats.pack(side="right", fill="both", expand=True)

    # Créer un canvas dans la zone de gauche
    canvas = Canvas(cadre_canvas, bg='#DDEEFF', bd=3, relief="solid", 
                    highlightbackground="white", highlightthickness=4, width=400, height=600)
    canvas.pack(fill="both", expand=True)

    # Ajouter un label dans la zone de résultats
    label_resultats = Label(cadre_resultats, text="Le Console du graphe", bg="#DDEEFF" , font=("Courier", 14))
    label_resultats.pack(pady=10)

    # Créer une barre de menus
    menu_bar = Menu(fenetre)

    # Créer les sous-menus
    menu_fichier = Menu(menu_bar, tearoff=0)  # Sous-menu Fichier
    menu_creation = Menu(menu_bar, tearoff=0)  # Sous-menu Création
    menu_affichage = Menu(menu_bar, tearoff=0)  # Sous-menu Affichage
    menu_exe = Menu(menu_bar, tearoff=0)  # Sous-menu Exécution
    menu_edition = Menu(menu_bar, tearoff=0)  # Sous-menu Édition

    # Créer les sous-menus avec des raccourcis clavier
    menu_fichier.add_command(label="Nouveau", image=icon_nouveau, compound=LEFT, 
                             command= nouveau_fichier , accelerator="Ctrl+N")  
    menu_fichier.add_command(label="Ouvrir", image=icon_ouvrir, compound=LEFT, 
                             command=lambda: ouvrir_fichier(canvas) , accelerator="Ctrl+O")
    menu_fichier.add_command(label="Enregistrer", image=icon_enregistrer, compound=LEFT,
                         command=lambda: enregistrer_fichier(canvas, fenetre) , accelerator="Ctrl+S")
    menu_fichier.add_command(label="Enregistrer sous", image=icon_enregistrer_sous, compound=LEFT, 
                         command=lambda: enregistrer_sous(canvas, fenetre) , accelerator="Ctrl+Shift+S")

    menu_fichier.add_separator()  # Séparateur dans le menu
    menu_fichier.add_command(label="Fermer", image=icon_fermer, compound=LEFT, 
                             command=lambda: fermer_fenetre(fenetre) , accelerator="Ctrl+Q")  # Option Fermer
    fenetre.protocol("WM_DELETE_WINDOW", lambda: fermer_fenetre(fenetre))  # Appeler la fonction de fermeture

    sous_menu_sommet = Menu(menu_creation, tearoff=0)
    sous_menu_sommet.add_command(label="Ajouter Un Sommet", image=icon_sommet, compound=LEFT , 
                                 command=lambda: ajouter_sommet(canvas) , accelerator="Ctrl+L" )
    sous_menu_sommet.add_command(label="Retirer Un Sommet", image=icon_sommet, compound=LEFT , 
                                 command=lambda: retirer_sommet(canvas) , accelerator="Del") 
    menu_creation.add_cascade(label="Sommet", image=icon_sommet, compound=LEFT , menu=sous_menu_sommet)

    sous_menu_arret = Menu(menu_creation, tearoff=0)
    sous_menu_arret.add_command(label="Ajouter Une Arête", image=icon_arret, compound=LEFT , 
                                command=lambda: ajouter_arrete(canvas) , accelerator="Ctrl+M")
    sous_menu_arret.add_command(label="Retirer Une Arête", image=icon_arret, compound=LEFT , 
                                command=lambda: retirer_arrete(canvas) , accelerator="ALT+Del")
    menu_creation.add_cascade(label="Arête" , image=icon_arret, compound=LEFT ,  menu=sous_menu_arret) 

    menu_affichage.add_command(label="Graphe" , image=icon_graphe, compound=LEFT ,
                               command=afficher_graphe, accelerator="Ctrl+F")

    sous_menu_chaine = Menu(menu_affichage , tearoff=0)
    sous_menu_chaine.add_command(label="Chaine eulerienne", image=icon_chaine_eulerienne, compound=LEFT , 
                            command=chaine_eulerienne, accelerator="Ctrl+H")
    sous_menu_chaine.add_command(label="Chemins entre deux sommets", image=icon_chemin, compound=LEFT , 
                            command=chemin_entre_deux_sommets, accelerator="Ctrl+I")
    menu_affichage.add_cascade(label="Chaines" , image=icon_chaine, compound=LEFT ,
                                menu=sous_menu_chaine)

    sous_menu_matrice_ma = Menu(menu_affichage , tearoff=0)
    sous_menu_matrice_ma.add_command(label="Matrice adjacents", image=icon_ma, compound=LEFT , 
                                command=afficher_matrice_adjacence, accelerator="Ctrl+H")
    sous_menu_matrice_ma.add_command(label="Matrice incidence", image=icon_mi, compound=LEFT , 
                       command=afficher_matrice_incidence , accelerator="Ctrl+I")
    menu_affichage.add_cascade(label="Matrices" , image=icon_matrice, compound=LEFT , 
                                menu=sous_menu_matrice_ma)

    menu_exe.add_command(label="Plus court chemin")
    menu_exe.add_command(label="Coloration")
    menu_edition.add_command(label="Graphe")

    # Ajouter la barre de menu à la fenêtre principale
    menu_bar.add_cascade(label="Fichier", menu=menu_fichier) # Ajouter le sous-menu Fichier
    menu_bar.add_cascade(label="Création", menu=menu_creation)  # Ajouter le sous-menu Création
    menu_bar.add_cascade(label="Affichage", menu=menu_affichage) # Ajouter le sous-menu Affichage
    menu_bar.add_cascade(label="Exécution", menu=menu_exe) # Ajouter le sous-menu Execution
    menu_bar.add_cascade(label="Édition", menu=menu_edition) # Ajouter le sous-menu Edition

    # Ajouter les raccourcis clavier à la fenêtre principale
    fenetre.bind_all("<Control-n>", lambda event: nouveau_fichier())
    fenetre.bind_all("<Control-o>", lambda event: ouvrir_fichier(Canvas))
    fenetre.bind_all("<Control-s>", lambda event: enregistrer_fichier(Canvas , fenetre))
    fenetre.bind_all("<Control-S>", lambda event: enregistrer_sous(Canvas , fenetre))  # Majuscule pour Shift
    fenetre.bind_all("<Control-l>", lambda event: ajouter_sommet(canvas))
    fenetre.bind_all("<Delete>", lambda event: retirer_sommet(canvas))
    fenetre.bind_all("<Control-m>", lambda event: ajouter_arrete(canvas))
    fenetre.bind_all("<Alt-Delete>", lambda event: retirer_arrete(canvas))
    fenetre.bind_all("<Control-q>", lambda event: fermer_fenetre(fenetre))
    fenetre.bind_all("<Control-f>", lambda event: afficher_graphe())
    fenetre.bind_all("<Control-g>", lambda event: fermer_fenetre(fenetre))
    fenetre.bind_all("<Control-h>", lambda event: retirer_arrete(canvas))
    fenetre.bind_all("<Control-i>", lambda event: fermer_fenetre(fenetre))
    
    
    # Appliquer la barre de menu à la fenêtre
    fenetre.config(menu=menu_bar)

# Créer la fenêtre principale
fenetre = Tk()

fenetre.title("Gestion des graphes")

# Amélioration de l'icône avec gestion d'erreur (exeption)
try:
    icon_nouveau = ImageTk.PhotoImage(Image.open("Icons/nouveau.png").resize((20, 20)))
    icon_ouvrir = ImageTk.PhotoImage(Image.open("Icons/ouvrir.png").resize((20, 20)))
    icon_enregistrer = ImageTk.PhotoImage(Image.open("Icons/enregistrer.png").resize((20, 20)))
    icon_enregistrer_sous = ImageTk.PhotoImage(Image.open("Icons/enregistrer_sous.png").resize((20, 20)))
    icon_fermer = ImageTk.PhotoImage(Image.open("Icons/fermer.png").resize((20, 20)))
    icon_sommet = ImageTk.PhotoImage(Image.open("Icons/sommet.png").resize((20, 20)))
    icon_arret = ImageTk.PhotoImage(Image.open("Icons/arret.png").resize((20, 20)))
    icon_graphe = ImageTk.PhotoImage(Image.open("Icons/graphe.png").resize((20, 20)))
    icon_chaine = ImageTk.PhotoImage(Image.open("Icons/chaine.png").resize((20, 20)))
    icon_chaine_eulerienne = ImageTk.PhotoImage(Image.open("Icons/chaine_eulerienne.png").resize((20, 20)))
    icon_chemin = ImageTk.PhotoImage(Image.open("Icons/chemin.png").resize((20, 20)))
    icon_matrice = ImageTk.PhotoImage(Image.open("Icons/matrice.png").resize((20, 20)))
    icon_ma = ImageTk.PhotoImage(Image.open("Icons/MA.png").resize((20, 20)))
    icon_mi = ImageTk.PhotoImage(Image.open("Icons/MI.png").resize((20, 20)))

    #ma = pour matrice adjacente et mi = pour matrice incidence .

except Exception as e:
    print(f"Erreur lors du chargement des icônes : {e}")
    boite_message.showerror("Erreur", "Une ou plusieurs icônes ne peuvent pas être chargées. Vérifiez les fichiers.")

creer_fenetre_principale(fenetre)
fenetre.mainloop()