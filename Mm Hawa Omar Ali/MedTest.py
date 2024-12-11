# Importation des bibliotheque .
import pickle  # Utiliser pickle pour sérialiser les données .
import os # pour interagir avec le systeme d'exploitation .
import time # Importation des modules time (gestion du temps)
import math  # Importation des modules math (fonctions mathématiques) .
from random import randint  # Importation de randint pour générer des valeurs aléatoires.
from tkinter import * # pour importer le bibliotheque de l'interface graphique .
from tkinter import ttk as note # Pour le widget Notebook
from tkinter import simpledialog  as zone_dialogue # Pour les boîtes de dialogue de saisie .
from tkinter import messagebox as boite_message # Pour les gestions de messages d'erreur et notifications .
from tkinter import filedialog as dialogue_fichier  # Pour la boîte de dialogue "Ouvrir un fichier"
from PIL import Image, ImageTk  , ImageDraw # Importer Pillow pour la gestion des images .
import networkx as nx  # Importation de la bibliothèque NetworkX pour la manipulation et l'analyse de graphes.
import matplotlib.pyplot as plt  # Importation de Matplotlib pour la visualisation de données .


# Variables globales pour la création du graphe

liste_sommets = []  # Liste des sommets du graphe
arcs = []  # Liste des arêtes du graphe
cercles = []  # Liste pour stocker les cercles dessinés
textes_sommets = []  # Liste pour stocker les identifiants des textes des sommets
etiquettes_arretes = []# Liste pour stocker les étiquettes des arêtes
creation_sommet = False  # Indicateur de création de sommet
creation_arete = False  # Indicateur de création d'arête
arete_orientee = False  # Indicateur pour les arêtes orientées
retirer_mode = False  # Indicateur pour le mode de suppression
sommet_selectionne = None  # Sommet sélectionné pour ajouter une arête
current_file = None  # Fichier en cours d'édition pour chaque onglet
graphe_orientee = None  # Type de graphe (orienté ou non, non défini au début)
compteur_onglets = 0 # Variable pour suivre le nombre d'onglets créés
elements_masques = False # Variable globale pour suivre l'état des éléments
sommet_selectionne_temp = []  # Stocke temporairement les sommets sélectionnés

# Dictionnaires pour stocker les données des onglets et les modifications

tab_data = {}  # Dictionnaire pour les données de chaque onglet
modifications = {}  # Dictionnaire pour suivre les modifications

# Creer la fenetre principale
fenetre = Tk()  # Création de la fenêtre principale de l'application
fenetre.title("Gestion des graphes")  # Définition du titre de la fenêtre
fenetre.geometry("800x600")  # Définition de la taille de la fenêtre
fenetre.iconbitmap("Icons/Bonjour.ico")  # Définition de l'icône de la fenêtre

# Amélioration de l'icône avec gestion d'erreur (exeption)
try:
    icon_nouveau = ImageTk.PhotoImage(Image.open("Icons/nouveau.png").resize((20, 20)))
    icon_ouvrir = ImageTk.PhotoImage(Image.open("Icons/ouvrir.png").resize((20, 20)))
    icon_enregistrer = ImageTk.PhotoImage(Image.open("Icons/enregistrer.png").resize((20, 20)))
    icon_enregistrer_sous = ImageTk.PhotoImage(Image.open("Icons/enregistrer_sous.png").resize((20, 20)))
    icon_fermer = ImageTk.PhotoImage(Image.open("Icons/fermer.png").resize((20, 20)))
    icon_quitter = ImageTk.PhotoImage(Image.open("Icons/Quitter.png").resize((20, 20)))
    icon_sommet = ImageTk.PhotoImage(Image.open("Icons/sommet.png").resize((20, 20)))
    icon_arret = ImageTk.PhotoImage(Image.open("Icons/arret.png").resize((20, 20)))
    icon_graphe = ImageTk.PhotoImage(Image.open("Icons/graphe.png").resize((20, 20)))
    icon_chaine = ImageTk.PhotoImage(Image.open("Icons/chaine.png").resize((20, 20)))
    icon_chaine_eulerienne = ImageTk.PhotoImage(Image.open("Icons/chaine_eulerienne.png").resize((20, 20)))
    icon_chaine_hamiltonienne = ImageTk.PhotoImage(Image.open("Icons/chaine_hamiltonienne.png").resize((20, 20)))
    icon_chemin = ImageTk.PhotoImage(Image.open("Icons/chemin.png").resize((20, 20)))
    icon_matrice = ImageTk.PhotoImage(Image.open("Icons/matrice.png").resize((20, 20)))
    icon_ma = ImageTk.PhotoImage(Image.open("Icons/MA.png").resize((20, 20)))
    icon_mi = ImageTk.PhotoImage(Image.open("Icons/MI.png").resize((20, 20)))
    icon_wp = ImageTk.PhotoImage(Image.open("Icons/wp.png").resize((20, 20)))
    #ma = pour matrice adjacente et mi = pour matrice incidence .

except Exception as e:
    print(f"Erreur lors du chargement des icônes : {e}")
    boite_message.showerror("Erreur", "Une ou plusieurs icônes ne peuvent pas être chargées. Vérifiez les fichiers.")

 # Ajouter les raccourcis clavier à la fenêtre principale
    fenetre.bind_all("<Control-n>", lambda event: nouveau())
    fenetre.bind_all("<Control-o>", lambda event: ouvrir_fichier)
    fenetre.bind_all("<Control-s>", lambda event: enregistrer_fichier)
    fenetre.bind_all("<Control-S>", lambda event: enregistrer_sous)  # Majuscule pour Shift
    fenetre.bind_all("<Control-l>", lambda event: creer_sommet)
    fenetre.bind_all("<Control-m>", lambda event: creer_arete_oriente)
    fenetre.bind_all("<Control-b>", lambda event: creer_arete_non_oriente)
    fenetre.bind_all("<Control-w>", lambda event: fermer_fichier)
    fenetre.bind_all("<Control-q>", lambda event: quitter_application)
    fenetre.bind_all("<Control-e>", lambda event: afficher_chaine_eulerienne())
    fenetre.bind_all("<Control-h>", lambda event: afficher_chaine_hamiltonienne())
    fenetre.bind_all("<Control-d>", lambda event: creer_arete_non_oriente)
    fenetre.bind_all("<Control-j>", lambda event: matrice_adjacence())
    fenetre.bind_all("<Control-i>", lambda event: matrice_incidence())
    fenetre.bind_all("<Control-p>", lambda event: parcours())
    fenetre.bind_all("<Control-W>", lambda event: welsh_powell())

# Creer un widget Notebook pour les onglets
notebook = note.Notebook(fenetre)  # Création d'un widget Notebook (onglets) dans la fenêtre principale
notebook.pack(expand=1, fill='both')  # Affichage du Notebook en remplissant tout l'espace disponible

# La gestion des onglets dans nouveau et ouvrir_fichier peut être factorisée.

# Fonction pour gérer le clic sur "Nouveau" (ajouter un nouvel onglet)
def nouveau():
    global graphe_orientee, compteur_onglets, elements_masques, canvas, cadre_resultats  # Assurez-vous que les variables sont globales
    
    graphe_orientee = None  # Réinitialiser pour un nouveau graphe 
    
    # Créer un nouvel onglet
    new_tab = Frame(notebook)  # Nouvel onglet sous forme de cadre (Frame)
    notebook.add(new_tab, text=f"Fichier - {compteur_onglets + 1}")  # Ajouter l'onglet au notebook
    notebook.select(new_tab)  # Sélectionner le nouvel onglet
    
    # Créer un cadre principal pour les deux zones (canvas et résultats)
    cadre_principal = Frame(new_tab)
    cadre_principal.pack(fill="both", expand=True)

    # Zone canvas à gauche
    cadre_canvas = Frame(cadre_principal, width=400, height=600, bg='#fdd9f0')
    cadre_canvas.pack(side="left", fill="both", expand=True)

    # Créer un canvas dans la zone de gauche
    canvas = Canvas(cadre_canvas, bg='#DDEEFF', bd=3, relief="solid",
                    highlightbackground="white", highlightthickness=4, width=400, height=600)
    canvas.pack(fill="both", expand=True)

    # Zone d'affichage des résultats avec scrollbar
    cadre_resultats = Frame(cadre_principal, bg='#DDEEFF', bd=3, relief="solid",
                            highlightbackground="white", highlightthickness=3, width=400, height=600)
    cadre_resultats.pack(side="right", fill="both", expand=True)

    # Ajouter une barre de défilement verticale
    scrollbar = Scrollbar(cadre_resultats)
    scrollbar.pack(side="right", fill="y")

    # Ajouter un canvas pour les résultats
    canvas_resultats = Canvas(cadre_resultats, bg="#DDEEFF", yscrollcommand=scrollbar.set)
    canvas_resultats.pack(side="left", fill="both", expand=True)

    # Configurer la scrollbar pour le canvas
    scrollbar.config(command=canvas_resultats.yview)

    # Créer un cadre à l'intérieur du canvas pour contenir les widgets
    cadre_interieur = Frame(canvas_resultats, bg="#DDEEFF")
    cadre_interieur.bind(
        "<Configure>",
        lambda e: canvas_resultats.configure(scrollregion=canvas_resultats.bbox("all"))
    )

    # Ajouter le cadre au canvas
    canvas_resultats.create_window((0, 0), window=cadre_interieur, anchor="nw")

    # Ajouter des éléments dans le cadre des résultats
    label_resultats = Label(cadre_interieur, text="Le Console du graphe", bg="#DDEEFF", font=("Courier", 14))
    label_resultats.pack(pady=10)
    
    # Associer le canevas au clic
    canvas.bind("<Button-1>", lambda event: canvas_click(event, canvas))

    # Incrémenter le compteur des onglets
    compteur_onglets += 1
    
    # Ajouter les données initiales pour ce nouvel onglet
    tab_data[new_tab] = {'sommets': [], 'aretes': [], 'file_path': None, 'canvas': canvas}
    tab_data[new_tab]['cadre_interieur'] = cadre_interieur
    
    # Masquer les éléments si nécessaire
    if not elements_masques:
        zone_animation.place_forget()  # Masquer la zone d'animation
        etiquette_date.place_forget()  # Masquer l'étiquette de date et heure
        cadre_photos.place_forget()  # Masquer le cadre des photos
        texte_bas_droite.place_forget()  # Masquer le texte en bas à droite
        elements_masques = True  # Marquer les éléments comme masqués

# Fonction pour ouvrir un fichier existant
def ouvrir_fichier():
    global graphe_orientee, elements_masques, canvas, cadre_resultats , cadre_interieur

    # Réinitialiser le type du graphe (sera déterminé par le contenu du fichier)
    graphe_orientee = None  

    # Ouvrir un fichier via la boîte de dialogue
    file_path = dialogue_fichier.askopenfilename(filetypes=[("Fichiers Python", "*.py")])
    if file_path:
        # Créer un nouvel onglet dans le notebook
        new_tab = Frame(notebook)

        # Créer un cadre principal pour les deux zones (canvas et résultats)
        cadre_principal = Frame(new_tab)
        cadre_principal.pack(fill="both", expand=True)

        # Zone canvas à gauche
        cadre_canvas = Frame(cadre_principal, width=400, height=600, bg='#fdd9f0')
        cadre_canvas.pack(side="left", fill="both", expand=True)

        # Créer un canvas dans la zone de gauche
        canvas = Canvas(cadre_canvas, bg='#DDEEFF', bd=3, relief="solid",
                        highlightbackground="white", highlightthickness=4, width=400, height=600)
        canvas.pack(fill="both", expand=True)

        # Zone d'affichage des résultats avec scrollbar
        cadre_resultats = Frame(cadre_principal, bg='#DDEEFF', bd=3, relief="solid",
                                highlightbackground="white", highlightthickness=3, width=400, height=600)
        cadre_resultats.pack(side="right", fill="both", expand=True)

        # Ajouter une barre de défilement verticale
        scrollbar = Scrollbar(cadre_resultats)
        scrollbar.pack(side="right", fill="y")

        # Ajouter un canvas pour les résultats
        canvas_resultats = Canvas(cadre_resultats, bg="#DDEEFF", yscrollcommand=scrollbar.set)
        canvas_resultats.pack(side="left", fill="both", expand=True)

        # Configurer la scrollbar pour le canvas
        scrollbar.config(command=canvas_resultats.yview)

        # Créer un cadre à l'intérieur du canvas pour contenir les widgets
        cadre_interieur = Frame(canvas_resultats, bg="#DDEEFF")
        cadre_interieur.bind(
            "<Configure>",
            lambda e: canvas_resultats.configure(scrollregion=canvas_resultats.bbox("all"))
        )

        # Ajouter le cadre au canvas
        canvas_resultats.create_window((0, 0), window=cadre_interieur, anchor="nw")
        

        # Ajouter des éléments dans le cadre des résultats
        label_resultats = Label(cadre_interieur, text="Le Console du graphe", bg="#DDEEFF", font=("Courier", 14))
        label_resultats.pack(pady=10)

        # Ajouter l'onglet au notebook
        notebook.add(new_tab, text=file_path.split('/')[-1])
        notebook.select(new_tab)

        # Charger le contenu du fichier
        with open(file_path, 'r') as file:
            contenu = file.read()

        # Initialiser les données pour l'onglet
        tab_data[new_tab] = {'sommets': [], 'aretes': [], 'file_path': file_path,'canvas': canvas }
        tab_data[new_tab]['cadre_interieur'] = cadre_interieur

        # Charger le graphe dans le canvas et l'onglet
        charger_graphe(contenu, canvas, new_tab)

        # Masquer les éléments si nécessaire
        if not elements_masques:
            # Masquer les éléments secondaires
            zone_animation.place_forget()  # Masquer la zone d'animation
            etiquette_date.place_forget()  # Masquer la date et l'heure
            cadre_photos.place_forget()  # Masquer le cadre des photos
            texte_bas_droite.place_forget()  # Masquer le texte en bas à droite
            elements_masques = True  # Indiquer que les éléments sont masqués

# Fonction pour enregistre une graphe .
def enregistrer_fichier():
    global current_tab
    current_tab = notebook.nametowidget(notebook.select())
    file_path = tab_data[current_tab].get('file_path')

    if not file_path:  # Si pas encore enregistre, utiliser 'Enregistrer sous'
        enregistrer_sous()
    else:
        with open(file_path, 'w') as file:
            file.write(sauvegarder_graphe(current_tab))

# Fonction pour enregistre-sous une graphe .
def enregistrer_sous():
    current_tab = notebook.nametowidget(notebook.select())
    fichier = dialogue_fichier.asksaveasfilename(defaultextension=".py", filetypes=[("Fichiers Python", "*.py")])
    if fichier:
        tab_data[current_tab]['file_path'] = fichier
        notebook.tab(current_tab, text=fichier.split('/')[-1])
        with open(fichier, 'w') as file:
            file.write(sauvegarder_graphe(current_tab))

# Fonction pour afficher une graphe .
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

# Fonction pour vérifier si la position (x, y) est libre, c'est-à-dire
# qu'elle n'est pas trop proche des autres sommets dans la liste.
def position_libre(x, y, liste_sommets):
    for (sx, sy, _) in liste_sommets:  # On ignore le nom du sommet (le 3ème élément)
        # Vérifie si la distance entre (x, y) et le sommet existant est inférieure à 50
        if abs(sx - x) < 50 and abs(sy - y) < 50:
            return False  # La position est occupée par un autre sommet
    return True  # La position est libre

# Fonctions pour creer des sommets et des arretes .
def creer_sommet():
    global creation_sommet, creation_arete
    creation_sommet = True
    creation_arete = False

# Fonction qui est responsable de dessiner un graphe sur un canevas
def dessiner_graphe(canvas, current_tab):
    canvas.delete("all")  # Nettoyer le canevas
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']  # Utiliser le canevas de l'onglet actif

    # Dessiner les sommets
    for x, y, nom_sommet in sommets:
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="white")  # Rayon de 20 pour les sommets
        canvas.create_text(x, y, text=nom_sommet, fill="black")

    # Dessiner les arêtes
    arêtes_multiples = {}  # Dictionnaire pour gérer les arêtes multiples
    for s1, s2, orientee, nom_arete in aretes:
        x1, y1, _ = sommets[s1]
        x2, y2, _ = sommets[s2]

        # Vérification pour les boucles (arêtes revenant au même sommet)
        if s1 == s2:
            boite_message.showerror("Erreur", "Impossible de créer une boucle.")
            return  # Interdire la création d'une boucle

        # Identifier les arêtes multiples (même origine et destination)
        clé = tuple(sorted((s1, s2)))
        if clé not in arêtes_multiples:
            arêtes_multiples[clé] = []
        arêtes_multiples[clé].append((s1, s2, orientee, nom_arete))

    # Vérification des arêtes multiples
    for clé, liste_arêtes in arêtes_multiples.items():
        if len(liste_arêtes) > 1:
            boite_message.showerror("Erreur", "Impossible de créer une arête multiple.")
            return  # Ne pas dessiner l'arête multiple

    # Dessiner les arêtes (sans décalage pour les arêtes multiples)
    for s1, s2, orientee, nom_arete in aretes:
        x1, y1, _ = sommets[s1]
        x2, y2, _ = sommets[s2]

        # Calcul de l'angle et ajustement
        angle = math.atan2(y2 - y1, x2 - x1)
        offset = 20  # Rayon du sommet
        x1_adj = x1 + offset * math.cos(angle)
        y1_adj = y1 + offset * math.sin(angle)
        x2_adj = x2 - offset * math.cos(angle)
        y2_adj = y2 - offset * math.sin(angle)

        # Dessiner l'arête (sans décalage pour les arêtes multiples)
        if orientee:
            draw_arrow(canvas, x1_adj, y1_adj, x2_adj, y2_adj)
        else:
            canvas.create_line(x1_adj, y1_adj, x2_adj, y2_adj)

        # Afficher le nom de l'arête
        xm, ym = (x1_adj + x2_adj) / 2, (y1_adj + y2_adj) / 2
        canvas.create_text(xm, ym - 15, text=nom_arete, fill="red", font=("Helvetica", 9, "italic"))

# Fonction pour dessiner une ligne avec une flèche à son extrémité
def draw_arrow(canvas, x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1)
    x_arrow = x2 - 15 * math.cos(angle)
    y_arrow = y2 - 15 * math.sin(angle)
    canvas.create_line(x1, y1, x_arrow, y_arrow, arrow=LAST)

# Fonction qui gère les clics sur le canevas pour créer des sommets et des arêtes dans le graphe
def canvas_click(event, canvas):
    global sommet_selectionne, creation_sommet, creation_arete, retirer_mode

    # Vérification si le mode retrait est activé
    if retirer_mode:
        retirer_sommet_par_clic(event, canvas)  # Appeler la fonction pour retirer un sommet
        return  # Fin de l'exécution si le mode retrait est activé

    # Récupérer les données de l'onglet actif
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']  # Utiliser le canevas de l'onglet actif

    x, y = event.x, event.y  # Coordonnées du clic sur le canevas

    # Mode création de sommet
    if creation_sommet:
        # Vérifier si la position est libre avant d'ajouter un sommet
        if position_libre(x, y, sommets):
            nom_sommet = f"S{len(sommets) + 1}"  # Générer un nom unique pour le sommet
            sommets.append((x, y, nom_sommet))  # Ajouter le sommet aux données
            dessiner_graphe(canvas, current_tab)  # Redessiner le graphe
        else:
            boite_message.showinfo("Position Occupée", "Cette position est trop proche d'un autre sommet.")

    # Mode création d'arête
    elif creation_arete:
        for i, (sx, sy, nom_sommet) in enumerate(sommets):
            if math.sqrt((sx - x) ** 2 + (sy - y) ** 2) <= 30:  # Vérifier si le clic est proche d'un sommet
                if sommet_selectionne is None:
                    sommet_selectionne = i  # Sélectionner le sommet pour la première extrémité de l'arête
                else:
                    nom_arete = f"A{len(aretes) + 1}"  # Générer un nom unique pour l'arête
                    aretes.append((sommet_selectionne, i, arete_orientee, nom_arete))  # Ajouter l'arête
                    sommet_selectionne = None  # Réinitialiser la sélection du sommet
                    dessiner_graphe(canvas, current_tab)  # Redessiner le graphe
                    break

# Fonction pour préparer les données d'un graphe pour être sauvegardées sous forme de texte structuré.
def sauvegarder_graphe(current_tab):
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    contenu = f"sommets = {sommets}\naretes = {aretes}\n"
    return contenu

# Fonction pour afficher le graphe (ouvrir un fichier)
def charger_graphe(contenu, canvas, current_tab):
    try:
        # Execute le contenu du fichier pour recuperer les sommets et arretes
        local_data = {}
        exec(contenu, {}, local_data)
        sommets = local_data.get('sommets', [])
        aretes = local_data.get('aretes', [])

        # Verifie si le graphe est orientee ou non
        if aretes:
            graphe_orientee = aretes[0][2] if len(aretes[0]) > 2 else None  # Deduit a partir du premier element
        else:
            graphe_orientee = None  # Aucun type defini si aucune arete

        # Associe les donnees au bon onglet
        
        tab_data[current_tab]['sommets'] = sommets
        tab_data[current_tab]['aretes'] = aretes
        tab_data[current_tab]['orientee'] = graphe_orientee  # Stocke le type de graphe

        # Redessine le graphe sur le canevas
        dessiner_graphe(canvas, current_tab)
    except Exception as e:
        boite_message.showerror("Erreur", f"Erreur lors du chargement : {e}")

# Fonction pour creer une graphe orientée
def creer_arete_oriente():
    global creation_sommet, creation_arete, arete_orientee, graphe_orientee
    if graphe_orientee is None or graphe_orientee is True:
        creation_sommet = False
        creation_arete = True
        arete_orientee = True
        graphe_orientee = True  # Definir le type de graphe comme orientee
    else:
        boite_message.showerror("Erreur", "Ce graphe est défini comme non orienté. Veuillez continuer avec des arêtes non orientées.")

def retirer_arrets_orienter():
    """
    Fonction pour supprimer une arête orientée entre deux sommets sélectionnés.
    Vérifie d'abord si le graphe contient des arêtes orientées avant de procéder.
    """
    global tab_data, sommet_selectionne_temp

    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "Aucun graphe actif dans cet onglet.")
        return

    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']

    # Vérification : s'assurer que le graphe contient des arêtes orientées
    def verifier_graphe_oriente(aretes):
        return any(orientee for _, _, orientee, _ in aretes)

    if not verifier_graphe_oriente(aretes):
        boite_message.showerror("Erreur", "Le graphe n'est pas orienté ou ne contient aucune arête orientée.")
        return

    # Vérification : s'assurer qu'il existe des arêtes à supprimer
    if not aretes:
        boite_message.showinfo("Notification", "Il n'y a plus d'arêtes à retirer.")
        return

    # Liste temporaire pour stocker les sommets sélectionnés
    sommet_selectionne_temp = []

    def selectionner_sommet(event):
        """
        Sélectionne un sommet sur le canevas en cliquant.
        """
        x, y = event.x, event.y

        # Trouver le sommet le plus proche du clic
        for i, (sx, sy, nom) in enumerate(sommets):
            if ((sx - x) ** 2 + (sy - y) ** 2) ** 0.5 <= 20:  # Rayon du sommet
                sommet_selectionne_temp.append(i)
                boite_message.showinfo("Sélection", f"Sommet {nom} sélectionné.")
                break

        # Si deux sommets sont sélectionnés, tenter de supprimer l'arête correspondante
        if len(sommet_selectionne_temp) == 2:
            sommet1, sommet2 = sommet_selectionne_temp
            supprimer_arrete(sommet1, sommet2)
            sommet_selectionne_temp.clear()  # Réinitialiser après traitement

    def supprimer_arrete(sommet1, sommet2):
        """
        Supprime une arête orientée entre deux sommets si elle existe.
        """
        for i, (s1, s2, orientee, ids_canvas) in enumerate(aretes):
            if orientee and s1 == sommet1 and s2 == sommet2:
                # Vérifier si l'identifiant contient la ligne et le texte
                if isinstance(ids_canvas, dict) and "ligne" in ids_canvas and "texte" in ids_canvas:
                    # Supprimer graphiquement les objets du canvas
                    canvas.delete(ids_canvas["ligne"])
                    canvas.delete(ids_canvas["texte"])

                # Supprimer l'arête de la liste
                aretes.pop(i)

                # Mettre à jour le canvas après suppression
                dessiner_graphe(canvas, current_tab)

                boite_message.showinfo("Succès", f"L'arête orientée de {sommets[s1][2]} vers {sommets[s2][2]} a été supprimée.")
                return

        # Si aucune arête orientée n'existe entre les sommets sélectionnés
        boite_message.showerror("Erreur", "Aucune arête orientée n'existe entre ces sommets.")

    # Liaison de l'événement pour sélectionner les sommets
    canvas.bind("<Button-1>", selectionner_sommet)

def retirer_sommet():
    """
    Fonction pour supprimer un sommet sélectionné et toutes les arêtes associées (orientées ou non orientées).
    """
    global tab_data, sommet_selectionne_temp

    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "Aucun graphe actif dans cet onglet.")
        return

    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']

    # Liste temporaire pour stocker le sommet sélectionné
    sommet_selectionne_temp = []

    def selectionner_sommet(event):
        """
        Sélectionne un sommet sur le canevas en cliquant et procède à sa suppression.
        """
        x, y = event.x, event.y

        # Trouver le sommet le plus proche du clic
        for i, (sx, sy, nom) in enumerate(sommets):
            if ((sx - x) ** 2 + (sy - y) ** 2) ** 0.5 <= 20:  # Rayon du sommet
                sommet_selectionne_temp.append(i)
                boite_message.showinfo("Sélection", f"Sommet {nom} sélectionné pour suppression.")
                break

        if sommet_selectionne_temp:
            sommet_a_supprimer = sommet_selectionne_temp.pop()
            supprimer_sommet(sommet_a_supprimer)

    def supprimer_sommet(sommet_index):
        """
        Supprime un sommet et toutes les arêtes associées.
        """
        # Vérifier que le sommet existe
        if sommet_index >= len(sommets):
            boite_message.showerror("Erreur", "Le sommet sélectionné est invalide.")
            return

        # Supprimer toutes les arêtes associées au sommet
        aretes_a_supprimer = []
        for i, (s1, s2, _, ids_canvas) in enumerate(aretes):
            if s1 == sommet_index or s2 == sommet_index:
                # Supprimer graphiquement les objets associés à l'arête
                if isinstance(ids_canvas, dict):
                    canvas.delete(ids_canvas.get("ligne", ""))
                    canvas.delete(ids_canvas.get("texte", ""))
                aretes_a_supprimer.append(i)

        # Supprimer les arêtes de la liste
        for i in sorted(aretes_a_supprimer, reverse=True):
            del aretes[i]

        # Supprimer le sommet du canevas
        sx, sy, nom = sommets[sommet_index]
        canvas.delete(nom)  # Supprimer le nom du sommet
        canvas.delete(f"sommet_{sommet_index}")  # Supprimer le cercle du sommet

        # Supprimer le sommet de la liste
        sommets.pop(sommet_index)

        # Mettre à jour les indices des arêtes et des sommets restants
        for i, (s1, s2, orientee, ids_canvas) in enumerate(aretes):
            if s1 > sommet_index:
                aretes[i] = (s1 - 1, s2, orientee, ids_canvas)
            if s2 > sommet_index:
                aretes[i] = (s1, s2 - 1, orientee, ids_canvas)

        boite_message.showinfo("Succès", f"Sommet {nom} et ses arêtes associées ont été supprimés.")

        # Mettre à jour le canvas après suppression
        dessiner_graphe(canvas, current_tab)

    # Liaison de l'événement pour sélectionner un sommet
    canvas.bind("<Button-1>", selectionner_sommet)

# Fonction pour creer une graphe non orientée
def creer_arete_non_oriente():
    global creation_sommet, creation_arete, arete_orientee, graphe_orientee
    if graphe_orientee is None or graphe_orientee is False:
        creation_sommet = False
        creation_arete = True
        arete_orientee = False
        graphe_orientee = False  # Définir le type de graphe comme non orienté
    else:
        boite_message.showerror("Erreur", "Ce graphe est défini comme orienté. Veuillez continuer avec des arêtes orientées.")

def retirer_arrets_non_orienter():
    """
    Fonction pour supprimer une arête non orientée entre deux sommets sélectionnés.
    Vérifie d'abord si le graphe est non orienté avant de procéder.
    """
    global tab_data, sommet_selectionne_temp

    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "Aucun graphe actif dans cet onglet.")
        return

    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']

    # Vérification : s'assurer que le graphe est non orienté
    def verifier_graphe_non_oriente(aretes):
        return all(not orientee for _, _, orientee, _ in aretes)

    if not verifier_graphe_non_oriente(aretes):
        boite_message.showerror("Erreur", "Le graphe est orienté ou ne contient aucune arête non orientée.")
        return

    # Vérification : s'assurer qu'il existe des arêtes à supprimer
    if not aretes:
        boite_message.showinfo("Notification", "Il n'y a plus d'arêtes à retirer.")
        return

    # Liste temporaire pour stocker les sommets sélectionnés
    sommet_selectionne_temp = []

    def selectionner_sommet(event):
        """
        Sélectionne un sommet sur le canevas en cliquant.
        """
        x, y = event.x, event.y

        # Trouver le sommet le plus proche du clic
        for i, (sx, sy, nom) in enumerate(sommets):
            if ((sx - x) ** 2 + (sy - y) ** 2) ** 0.5 <= 20:  # Rayon du sommet
                sommet_selectionne_temp.append(i)
                boite_message.showinfo("Sélection", f"Sommet {nom} sélectionné.")
                break

        # Si deux sommets sont sélectionnés, tenter de supprimer l'arête correspondante
        if len(sommet_selectionne_temp) == 2:
            sommet1, sommet2 = sommet_selectionne_temp
            supprimer_arrete(sommet1, sommet2)
            sommet_selectionne_temp.clear()  # Réinitialiser après traitement

    def supprimer_arrete(sommet1, sommet2):
        """
        Supprime une arête entre deux sommets si elle existe.
        """
        for i, (s1, s2, orientee, ids_canvas) in enumerate(aretes):
            if (s1 == sommet1 and s2 == sommet2) or (s1 == sommet2 and s2 == sommet1):
                # Vérifier si l'identifiant contient la ligne et le texte
                if isinstance(ids_canvas, dict) and "ligne" in ids_canvas and "texte" in ids_canvas:
                    # Supprimer graphiquement les objets du canvas
                    canvas.delete(ids_canvas["ligne"])
                    canvas.delete(ids_canvas["texte"])

                # Supprimer l'arête de la liste
                aretes.pop(i)

                # Mettre à jour le canvas après suppression
                dessiner_graphe(canvas, current_tab)

                boite_message.showinfo("Succès", f"L'arête entre {sommets[s1][2]} et {sommets[s2][2]} a été supprimée.")
                return

        # Si aucune arête n'existe entre les sommets sélectionnés
        boite_message.showerror("Erreur", "Aucune arête n'existe entre ces sommets.")

    # Liaison de l'événement pour sélectionner les sommets
    canvas.bind("<Button-1>", selectionner_sommet)

# Fonction pour afficher la chaine eulerienne .
def afficher_chaine_eulerienne():
    global cadre_interieur
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    cadre_interieur = data.get('cadre_interieur')  # Récupérer le cadre_interieur associé
    sommets = data['sommets']
    aretes = data['aretes']

    # Construire une représentation du graphe
    graphe = {i: [] for i in range(len(sommets))}
    for s1, s2, orientee, nom_arete in aretes:
        graphe[s1].append((s2, nom_arete))
        if not orientee:
            graphe[s2].append((s1, nom_arete))

    odd_vertices = [v for v in graphe if len(graphe[v]) % 2 != 0]
    if len(odd_vertices) not in [0, 2]:
        message = "Ce graphe ne contient aucune chaîne eulérienne !"
    else:
        def find_eulerian_path(v, path):
            while graphe[v]:
                next_vertex, edge_name = graphe[v].pop()
                graphe[next_vertex].remove((v, edge_name))
                find_eulerian_path(next_vertex, path)
            path.append(v)

        start_vertex = odd_vertices[0] if odd_vertices else 0
        path = []
        find_eulerian_path(start_vertex, path)
        message = "Chaîne eulérienne trouvée : " + " -> ".join(f"S{i + 1}" for i in path[::-1])

    # Afficher dans le cadre défilable
    cadre_message = Frame(cadre_interieur, bg="#DDEEFF")
    cadre_message.pack(pady=5, padx=10, fill="x")

    label_titre = Label(cadre_message, text="Chaîne eulérienne", bg="#DDEEFF", font=("Arial", 12, "bold"))
    label_titre.pack()

    label_message = Label(cadre_message, text=message, bg="#FFFFFF", font=("Arial", 10), wraplength=400, justify="left", relief="solid", padx=10, pady=5)
    label_message.pack()

# Fonction pour afficher la chaine eulerienne .
def afficher_chaine_hamiltonienne():
    global cadre_interieur
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    cadre_interieur = data.get('cadre_interieur')  # Récupérer le cadre_interieur associé
    sommets = data['sommets']
    aretes = data['aretes']

    graphe = {i: [] for i in range(len(sommets))}
    for s1, s2, orientee, nom_arete in aretes:
        graphe[s1].append(s2)
        if not orientee:
            graphe[s2].append(s1)

    n = len(sommets)

    def hamiltonian_path(v, visited, path):
        if len(path) == n:
            return path

        for neighbor in graphe[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                result = hamiltonian_path(neighbor, visited, path)
                if result:
                    return result
                path.pop()
                visited.remove(neighbor)
        return None

    message = "Ce graphe ne contient aucune chaîne hamiltonienne !"
    for start_vertex in range(n):
        visited = {start_vertex}
        path = [start_vertex]
        result = hamiltonian_path(start_vertex, visited, path)
        if result:
            message = "Chaîne hamiltonienne trouvée : " + " -> ".join(f"S{i + 1}" for i in result)
            break

    cadre_message = Frame(cadre_interieur, bg="#DDEEFF")
    cadre_message.pack(pady=5, padx=10, fill="x")

    label_titre = Label(cadre_message, text="Chaîne hamiltonienne", bg="#DDEEFF", font=("Arial", 12, "bold"))
    label_titre.pack()

    label_message = Label(cadre_message, text=message, bg="#FFFFFF", font=("Arial", 10), wraplength=400, justify="left", relief="solid", padx=10, pady=5)
    label_message.pack()

def chemin_entre_deux_sommets():
    """
    Fonction pour afficher le chemin entre deux sommets dans un graphe, sans prendre d'arguments.
    Utilise les variables globales pour accéder aux données du graphe.
    Prend en charge les arêtes orientées et non orientées.
    """
    global tab_data

    # Demander au user de saisir les sommets de départ et d'arrivée
    sommet_depart = zone_dialogue.askstring("Sommet de départ", "Entrez le sommet de départ :")
    sommet_arrive = zone_dialogue.askstring("Sommet d'arrivée", "Entrez le sommet d'arrivée :")

    # Vérifier la validité des sommets dans le graphe actif
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "L'onglet sélectionné n'est pas valide.")
        return

    # Récupérer les données du graphe
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    # Vérifier la validité des sommets
    if sommet_depart == sommet_arrive:
        boite_message.showerror("Erreur", "Les deux sommets doivent être différents.")
        return
    if sommet_depart not in [nom for _, _, nom in sommets] or sommet_arrive not in [nom for _, _, nom in sommets]:
        boite_message.showerror("Erreur", "Veuillez entrer des sommets présents dans le graphe.")
        return

    # Créer un graphe temporaire pour utiliser les fonctionnalités de NetworkX
    G = nx.DiGraph() if any(orientee for _, _, orientee, _ in aretes) else nx.Graph()

    for _, _, nom in sommets:
        G.add_node(nom)

    for s1, s2, orientee, _ in aretes:
        if orientee:
            G.add_edge(sommets[s1][2], sommets[s2][2])  # Arête orientée
        else:
            G.add_edge(sommets[s1][2], sommets[s2][2])  # Arête non orientée

    # Vérifier l'existence d'un chemin et l'afficher
    try:
        chemin = nx.shortest_path(G, source=sommet_depart, target=sommet_arrive)
        chemin_str = " -> ".join(chemin)

        # Afficher le chemin trouvé
        boite_message.showinfo("Chemin trouvé", f"Chemin entre {sommet_depart} et {sommet_arrive} : {chemin_str}")

        # Dessiner le chemin sur le canevas
        canvas = data['canvas']
        rayon = 20  # Rayon des cercles représentant les sommets
        coordonnees_chemin = []

        # Récupérer les coordonnées des sommets dans le chemin
        for nom_sommet in chemin:
            for x, y, nom in sommets:
                if nom == nom_sommet:
                    coordonnees_chemin.append((x, y))

        # Dessiner le chemin entre les sommets
        for i in range(len(coordonnees_chemin) - 1):
            x1, y1 = coordonnees_chemin[i]
            x2, y2 = coordonnees_chemin[i + 1]

            # Calculer les points d'extrémité des arêtes pour qu'elles n'intersectent pas les sommets
            dx, dy = x2 - x1, y2 - y1
            distance = (dx**2 + dy**2)**0.5
            x1_ext = x1 + rayon * dx / distance
            y1_ext = y1 + rayon * dy / distance
            x2_ext = x2 - rayon * dx / distance
            y2_ext = y2 - rayon * dy / distance

            # Dessiner l'arête (chemin) en rouge entre les deux sommets
            canvas.create_line(x1_ext, y1_ext, x2_ext, y2_ext, fill="red", width=2)

    except nx.NetworkXNoPath:
        boite_message.showinfo("Pas de chemin", f"Aucun chemin entre {sommet_depart} et {sommet_arrive}.")

# Fonction pour afficher la matrice d'adjacence
def matrice_adjacence():
    global cadre_interieur
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    cadre_interieur = data.get('cadre_interieur')  # Récupérer le cadre_interieur associé
    sommets = data['sommets']
    aretes = data['aretes']

    n = len(sommets)
    matrice = [[0] * n for _ in range(n)]
    for s1, s2, orientee, _ in aretes:
        matrice[s1][s2] = 1
        if not orientee:
            matrice[s2][s1] = 1

    # Utiliser le troisième élément des sommets pour récupérer leurs vrais noms
    noms_sommets = [sommet[2] for sommet in sommets]
    afficher_matrice_adjacente(matrice, "Matrice d'Adjacence", noms_sommets)

def afficher_matrice_adjacente(matrice, titre, sommets):
    global cadre_interieur
    cadre_matrice = Frame(cadre_interieur, bg="#DDEEFF")
    cadre_matrice.pack(padx=10, pady=5, fill="x")

    label_titre_matrice = Label(cadre_matrice, text=titre, bg="#DDEEFF", font=("Arial", 14, "bold"))
    label_titre_matrice.pack(pady=10)

    frame_matrice = Frame(cadre_matrice, bg="#DDEEFF")
    frame_matrice.pack(padx=10, pady=10)

    for j, sommet in enumerate(sommets):
        Label(frame_matrice, text=sommet, width=4, height=2, relief="solid", bg="#F0F0F0", font=("Arial", 12, "bold")).grid(row=0, column=j + 1, sticky="nsew")

    for i, ligne in enumerate(matrice):
        Label(frame_matrice, text=sommets[i], width=4, height=2, relief="solid", bg="#F0F0F0", font=("Arial", 12, "bold")).grid(row=i + 1, column=0, sticky="nsew")
        for j, valeur in enumerate(ligne):
            Label(frame_matrice, text=valeur, width=4, height=2, relief="solid", bg="white", font=("Arial", 12)).grid(row=i + 1, column=j + 1, sticky="nsew")

# Fonction pour afficher la matrice d'incidence
def matrice_incidence():
    global cadre_interieur
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    cadre_interieur = data.get('cadre_interieur')  # Récupérer le cadre_interieur associé
    sommets = data['sommets']
    aretes = data['aretes']

    n_sommets = len(sommets)
    n_aretes = len(aretes)
    
    # Initialisation de la matrice d'incidence avec des zéros
    matrice = [[0] * n_aretes for _ in range(n_sommets)]

    # Utiliser le troisième élément des sommets pour récupérer leurs vrais noms
    noms_sommets = [sommet[2] for sommet in sommets]  # Noms des sommets
    noms_arcs = [arete[3] for arete in aretes]  # Noms des arêtes

    # Parcours des arêtes pour remplir la matrice
    for j, (s1, s2, orientee, _) in enumerate(aretes):
        if orientee:
            # Si l'arc est orienté, l'élément correspondant pour s1 sera -1 (sortant)
            # et pour s2 sera 1 (entrant)
            matrice[s1][j] = -1  # Arc sortant de s1
            matrice[s2][j] = 1   # Arc entrant dans s2
        else:
            # Si l'arc est non orienté, on met 1 pour les deux sommets (relation bidirectionnelle)
            matrice[s1][j] = 1  # Arc entre s1 et s2
            matrice[s2][j] = 1  # Arc entre s2 et s1

    afficher_matrice_incidence(matrice, "Matrice d'Incidence", noms_sommets, noms_arcs)

def afficher_matrice_incidence(matrice, titre, sommets, arcs):
    global cadre_interieur
    cadre_matrice = Frame(cadre_interieur, bg="#DDEEFF")
    cadre_matrice.pack(padx=10, pady=5, fill="x")

    label_titre_matrice = Label(cadre_matrice, text=titre, bg="#DDEEFF", font=("Arial", 14, "bold"))
    label_titre_matrice.pack(pady=10)

    frame_matrice = Frame(cadre_matrice, bg="#DDEEFF")
    frame_matrice.pack(padx=10, pady=10)

    for j, arc in enumerate(arcs):
        Label(frame_matrice, text=arc, width=4, height=2, relief="solid", bg="#F0F0F0", font=("Arial", 12, "bold")).grid(row=0, column=j + 1, sticky="nsew")

    for i, ligne in enumerate(matrice):
        Label(frame_matrice, text=sommets[i], width=4, height=2, relief="solid", bg="#F0F0F0", font=("Arial", 12, "bold")).grid(row=i + 1, column=0, sticky="nsew")
        for j, valeur in enumerate(ligne):
            Label(frame_matrice, text=valeur, width=4, height=2, relief="solid", bg="white", font=("Arial", 12)).grid(row=i + 1, column=j + 1, sticky="nsew")

# Fonction pour effectuer un parcours en largeur
def parcours():
    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "L'onglet sélectionné n'est pas valide ou n'a pas de graphe associé.")
        return

    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']  # Utiliser le canevas de l'onglet actif
    graphe_oriente = data.get('oriente', False)  # Déterminer si le graphe est orienté

    if not sommets:
        boite_message.showerror("Erreur", "Le graphe ne contient aucun sommet.")
        return

    n = len(sommets)

    # Construire une liste d'adjacence pour représenter le graphe
    graphe = {i: [] for i in range(n)}
    for s1, s2, orientee, _nom_arete in aretes:
        graphe[s1].append(s2)
        if not orientee:  # Si l'arête est non orientée
            graphe[s2].append(s1)

    # Demander à l'utilisateur le sommet de départ
    sommet_depart = zone_dialogue.askinteger(
        "Parcours BFS", 
        "Entrez le sommet de départ (entre 1 et N) :", 
        minvalue=1, 
        maxvalue=n
    )
    if sommet_depart is None:
        return

    sommet_depart -= 1  # Ajuster l'indice pour la représentation interne (0-based)

    # Parcours en largeur (BFS)
    visite = [False] * n
    file = [sommet_depart]
    ordre_parcours = []

    visite[sommet_depart] = True

    while file:
        sommet = file.pop(0)
        ordre_parcours.append(sommet + 1)  # Ajouter 1 pour rétablir 1-based pour l'affichage
        for voisin in graphe[sommet]:
            if not visite[voisin]:
                visite[voisin] = True
                file.append(voisin)

    # Dessiner le parcours sur le canevas
    canvas.delete("all")  # Nettoyer le canevas
    for x, y, nom_sommet in sommets:
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="white")  # Dessiner les sommets
        canvas.create_text(x, y, text=nom_sommet, fill="black")

    for i in range(len(ordre_parcours) - 1):
        s1 = ordre_parcours[i] - 1  # Indice réel du sommet (0-based)
        s2 = ordre_parcours[i + 1] - 1
        x1, y1, _ = sommets[s1]
        x2, y2, _ = sommets[s2]
        canvas.create_line(
            x1, y1, x2, y2, 
            fill="blue", 
            width=2, 
            arrow="last" if graphe_oriente else None  # Afficher la flèche uniquement si le graphe est orienté
        )

    # Afficher le résultat du parcours
    boite_message.showinfo(
        "Résultat du parcours BFS",
        f"Ordre du parcours en largeur : {' -> '.join(map(str, ordre_parcours))}"
    )

# Fonction pour créer et dessiner l'arbre couvrant à partir du parcours BFS
def creer_arbre_couvrant():
    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "L'onglet sélectionné n'est pas valide ou n'a pas de graphe associé.")
        return

    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    canvas = data['canvas']  # Utiliser le canevas de l'onglet actif
    graphe_oriente = data.get('oriente', False)  # Déterminer si le graphe est orienté

    if not sommets:
        boite_message.showerror("Erreur", "Le graphe ne contient aucun sommet.")
        return

    n = len(sommets)

    # Construire une liste d'adjacence
    graphe = {i: [] for i in range(n)}
    for s1, s2, orientee, _nom_arete in aretes:
        graphe[s1].append(s2)
        if not orientee:  # Si l'arête est non orientée
            graphe[s2].append(s1)

    # Demander à l'utilisateur le sommet de départ
    sommet_depart = zone_dialogue.askinteger(
        "Arbre couvrant BFS", 
        "Entrez le sommet de départ (entre 1 et N) :",
        minvalue=1,
        maxvalue=n
    )
    if sommet_depart is None:
        return

    sommet_depart -= 1  # Ajuster l'indice pour la représentation interne (0-based)

    # Générer l'arbre couvrant via BFS
    visite = [False] * n
    file = [sommet_depart]
    arbre_couvrant = []

    visite[sommet_depart] = True

    while file:
        sommet = file.pop(0)
        for voisin in graphe[sommet]:
            if not visite[voisin]:
                visite[voisin] = True
                file.append(voisin)
                arbre_couvrant.append((sommet, voisin))  # Ajouter l'arête dans l'arbre

    # Dessiner l'arbre couvrant
    canvas.delete("all")  # Effacer l'ancien graphe
    for x, y, nom_sommet in sommets:
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="green")
        canvas.create_text(x, y, text=nom_sommet, fill="white")
    for s1, s2 in arbre_couvrant:
        x1, y1, _ = sommets[s1]
        x2, y2, _ = sommets[s2]
        canvas.create_line(
            x1, y1, x2, y2, 
            fill="blue", 
            width=2, 
            arrow="last" if graphe_oriente else None  # Afficher la flèche uniquement si le graphe est orienté
        )

    boite_message.showinfo("Arbre couvrant BFS", "L'arbre couvrant a été généré et dessiné.")

def welsh_powell():
    # Fonction interne pour générer une palette dynamique de couleurs
    def generer_palette_couleurs(n):
        """Génère dynamiquement une palette de couleurs pour s'assurer qu'il y en a suffisamment."""
        from random import randint
        # Palette de couleurs de base
        palette = ["red", "blue", "green", "yellow", "purple", "orange", "pink"]
        # Ajouter des couleurs aléatoires jusqu'à ce qu'il y en ait suffisamment
        while len(palette) < n:
            # Générer une couleur aléatoire en hexadécimal
            couleur = f"#{randint(0, 255):02x}{randint(0, 255):02x}{randint(0, 255):02x}"
            # Ajouter la couleur à la palette si elle n'y est pas déjà
            if couleur not in palette:
                palette.append(couleur)
        return palette

    # Récupérer l'onglet actif et ses données
    current_tab = notebook.nametowidget(notebook.select())
    # Vérifier si l'onglet actif contient des données de graphe
    if current_tab not in tab_data:
        boite_message.showerror("Erreur", "L'onglet sélectionné n'est pas valide ou n'a pas de graphe associé.")
        return

    data = tab_data[current_tab]  # Récupérer les données du graphe de l'onglet actif
    sommets = data['sommets']  # Liste des sommets sous forme de tuples (x, y, nom_sommet)
    aretes = data['aretes']  # Liste des arêtes sous forme de tuples (s1, s2, orientée, nom_arete)
    canvas = data['canvas']  # Canevas pour dessiner le graphe

    # Vérifier si les sommets et arêtes sont valides
    if not sommets or not aretes:
        boite_message.showerror("Erreur", "Le graphe doit contenir des sommets et des arêtes.")
        return

    # Fonction pour vérifier si le graphe est orienté
    def verifier_type_graphe(aretes):
        return any(orientee for _, _, orientee, _ in aretes)

    # Vérifier si le graphe est orienté
    if verifier_type_graphe(aretes):
        boite_message.showerror("Erreur", "L'algorithme Welsh-Powell ne s'applique pas aux graphes orientés.")
        return

    # Fonction pour vérifier si le graphe est connexe
    def verifier_graphe_connexe(sommets, aretes):
        def dfs(sommet, visites, adj):
            visites.add(sommet)
            # Parcours en profondeur des voisins
            for voisin in adj.get(sommet, []):
                if voisin not in visites:
                    dfs(voisin, visites, adj)

        # Créer une représentation du graphe sous forme de liste d'adjacence
        adjacence = {nom_sommet: [] for _, _, nom_sommet in sommets}
        for s1, s2, _, _ in aretes:
            adjacence[sommets[s1][2]].append(sommets[s2][2])
            adjacence[sommets[s2][2]].append(sommets[s1][2])

        # Effectuer un DFS pour vérifier la connexité
        visites = set()
        dfs(sommets[0][2], visites, adjacence)
        return len(visites) == len(sommets)

    # Vérification de la connexité du graphe
    if not verifier_graphe_connexe(sommets, aretes):
        boite_message.showerror("Erreur", "Le graphe n'est pas connexe.")
        return

    # Étape 1 : Déterminer les degrés des sommets
    def determiner_degre_sommet(aretes, sommets):
        # Initialiser un dictionnaire de degrés avec 0
        degre = {nom_sommet: 0 for _, _, nom_sommet in sommets}
        # Calculer le degré pour chaque sommet en fonction des arêtes
        for s1, s2, _, _ in aretes:
            degre[sommets[s1][2]] += 1
            degre[sommets[s2][2]] += 1
        return degre

    # Étape 2 : Trier les sommets par degré décroissant
    def trier_sommets_par_degre(degre):
        # Trier les sommets par degré décroissant
        return sorted(degre.keys(), key=lambda nom: -degre[nom])

    # Étape 3 : Attribuer les couleurs aux sommets
    def attribuer_couleur_sommet(sommets_tries, aretes, sommets):
        couleurs = {}
        # Pour chaque sommet trié par degré
        for sommet in sommets_tries:
            # Trouver les voisins du sommet
            voisins = [sommets[s1][2] if sommets[s2][2] == sommet else sommets[s2][2]
                       for s1, s2, _, _ in aretes if sommet in (sommets[s1][2], sommets[s2][2])]
            # Collecter les couleurs des voisins
            couleurs_voisins = {couleurs[voisin] for voisin in voisins if voisin in couleurs}
            # Trouver la première couleur non utilisée
            couleur = 0
            while couleur in couleurs_voisins:
                couleur += 1
            couleurs[sommet] = couleur
        return couleurs

    # Calculer le degré de chaque sommet
    degre_sommets = determiner_degre_sommet(aretes, sommets)

    # Trier les sommets par degré décroissant
    sommets_tries = trier_sommets_par_degre(degre_sommets)

    # Calculer le nombre de couleurs nécessaires
    nombre_couleurs = max(degre_sommets.values()) + 1

    # Générer une palette de couleurs suffisante
    palette_couleurs = generer_palette_couleurs(nombre_couleurs)

    # Attribuer les couleurs aux sommets
    couleurs = attribuer_couleur_sommet(sommets_tries, aretes, sommets)

    # Étape 4 : Dessiner le graphe coloré
    canvas.delete("all")  # Effacer tous les éléments précédemment dessinés sur le canevas
    rayon = 20  # Définir le rayon des cercles représentant les sommets

    # Dessiner chaque sommet avec sa couleur
    for x, y, nom_sommet in sommets:
        couleur = palette_couleurs[couleurs[nom_sommet]]  # Obtenir la couleur du sommet
        canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, fill=couleur)  # Dessiner un cercle coloré
        canvas.create_text(x, y, text=nom_sommet, fill="black")  # Ajouter le nom du sommet

    # Dessiner les arêtes avec leurs étiquettes
    for s1, s2, _, nom_arete in aretes:
        x1, y1, _ = sommets[s1]  # Coordonnées du premier sommet
        x2, y2, _ = sommets[s2]  # Coordonnées du deuxième sommet

        # Calculer les coordonnées d'extrémité des arêtes en fonction du rayon des sommets
        dx, dy = x2 - x1, y2 - y1
        distance = (dx**2 + dy**2)**0.5
        x1_ext = x1 + rayon * dx / distance
        y1_ext = y1 + rayon * dy / distance
        x2_ext = x2 - rayon * dx / distance
        y2_ext = y2 - rayon * dy / distance

        # Dessiner l'arête entre les deux sommets
        canvas.create_line(x1_ext, y1_ext, x2_ext, y2_ext, fill="black", width=2)
        
        # Afficher l'étiquette au centre de l'arête
        x_milieu = (x1_ext + x2_ext) / 2
        y_milieu = (y1_ext + y2_ext) / 2
        canvas.create_text(x_milieu, y_milieu, text=nom_arete, fill="black", font=("Arial", 13, "bold"))  # Ajouter le nom de l'arête

    # Afficher les résultats de la coloration dans une fenêtre popup
    resultats = "\n".join([f"{sommet}: {palette_couleurs[couleurs[sommet]]}" for sommet in sommets_tries])
    boite_message.showinfo("Coloration des Sommets", f"Résultats de la coloration :\n\n{resultats}")

# Fonction pour fermer l'onglet actuel
def fermer_fichier():
    global elements_masques  # Assurez-vous que cette variable est globale
    if notebook.index("end") > 0:
        # Obtenir l'onglet courant
        current_tab = notebook.select()
        
        # Fermer l'onglet
        notebook.forget(current_tab)
        
        # Verifier et supprimer les donnees associees a l'onglet, si elles existent
        if current_tab in tab_data:
            del tab_data[current_tab]
        
        # Restaurer les éléments si tous les onglets sont fermés
        if notebook.index("end") == 0 and elements_masques:
            # Restaurer les éléments
            zone_animation.place(relx=0.5, rely=0.3, anchor="n")
            etiquette_date.place(relx=1, y=5, anchor="ne")
            cadre_photos.place(relx=0.5, rely=0.5, anchor="center")
            texte_bas_droite.place(relx=1, rely=1, anchor="se", x=-20, y=-20)
            elements_masques = False  # Mettre à jour l'état

# Fonction pour quitter l'application
def quitter_application():
    confirmation = boite_message.askyesno("Quitter", "etes-vous sur de vouloir quitter?")
    if confirmation:
        fenetre.quit()

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

# Créer une barre de menus
menu_bar = Menu(fenetre)

# Créer les sous-menus
menu_fichier = Menu(menu_bar, tearoff=0)  # Sous-menu Fichier
menu_creation = Menu(menu_bar, tearoff=0)  # Sous-menu Création
menu_affichage = Menu(menu_bar, tearoff=0)  # Sous-menu Affichage
menu_exe = Menu(menu_bar, tearoff=0)  # Sous-menu Exécution
menu_edition = Menu(menu_bar, tearoff=0)  # Sous-menu Édition

# Menu Fichier
menu_fichier.add_command(label="Nouveau", image=icon_nouveau,compound=LEFT,command=nouveau, accelerator="Ctrl+N")
menu_fichier.add_command(label="Ouvrir", image=icon_ouvrir, compound=LEFT,command=ouvrir_fichier , accelerator="Ctrl+O")
menu_fichier.add_command(label="Enregistrer", image=icon_enregistrer , compound=LEFT,command=enregistrer_fichier , accelerator="Ctrl+S")
menu_fichier.add_command(label="Enregistrer sous",image=icon_enregistrer_sous,command= enregistrer_sous,compound=LEFT , accelerator="Ctrl+Shift+S")
menu_fichier.add_command(label="Fermer",image=icon_fermer , compound=LEFT,command=fermer_fichier , accelerator="Ctrl+W")
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter",image=icon_quitter , compound=LEFT, command=quitter_application,accelerator="Ctrl+W")

# Menu Création
sous_menu_sommet = Menu(menu_creation, tearoff=0)
sous_menu_sommet.add_command(label="Ajouter Un Sommet",image=icon_sommet ,command= creer_sommet ,compound=LEFT , accelerator="Ctrl+L" )
sous_menu_sommet.add_command(label="Retirer Un Sommet",compound=LEFT,command=retirer_sommet)
menu_creation.add_cascade(label="Sommet", image=icon_sommet, compound=LEFT, menu=sous_menu_sommet)

# Sous-menu Arête
sous_menu_arret = Menu(menu_creation, tearoff=0)

# Sous-menu pour les arêtes orientées
sous_menu_arret_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_orientee.add_command(label="Ajouter une arête orientée",image=icon_arret ,command=creer_arete_oriente,compound=LEFT , accelerator="Ctrl+M")
sous_menu_arret_orientee.add_command(label="Retirer une arête orientée",compound=LEFT,command=retirer_arrets_orienter)


# Sous-menu pour les arêtes non orientées
sous_menu_arret_non_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_non_orientee.add_command(label="Ajouter une arête non orientée",image=icon_arret ,command=creer_arete_non_oriente,compound=LEFT ,accelerator="Ctrl+B")
sous_menu_arret_non_orientee.add_command(label="Retirer une arête non orientée",compound=LEFT,command=retirer_arrets_non_orienter)


# Ajouter les options des arêtes au menu principal
sous_menu_arret.add_cascade(label="Arête Orientée",image=icon_arret , compound=LEFT ,menu=sous_menu_arret_orientee)
sous_menu_arret.add_cascade(label="Arête Non Orientée",image=icon_arret , compound=LEFT , menu=sous_menu_arret_non_orientee)
menu_creation.add_cascade(label="Arête",image=icon_arret , compound=LEFT, menu=sous_menu_arret)

# Menu Affichage
sous_menu_chaine = Menu(menu_affichage, tearoff=0)
sous_menu_chaine.add_command(label="Chaine Eulerienne",image=icon_chaine_eulerienne , command=afficher_chaine_eulerienne,compound=LEFT , accelerator="Ctrl+E")
sous_menu_chaine.add_command(label="Chaine Hamiltonienne",image=icon_chaine_hamiltonienne , command=afficher_chaine_hamiltonienne,compound=LEFT , accelerator="Ctrl+H")
sous_menu_chaine.add_command(label="Chemins entre deux sommets", image=icon_chemin, compound=LEFT , 
                    command=chemin_entre_deux_sommets , accelerator="Ctrl+D")
menu_affichage.add_cascade(label="Chaines", image=icon_chaine,compound=LEFT, menu=sous_menu_chaine)

sous_menu_matrice_ma = Menu(menu_affichage, tearoff=0)
sous_menu_matrice_ma.add_command(label="Matrice adjacents",image=icon_ma ,command=matrice_adjacence,compound=LEFT , accelerator="Ctrl+J")
sous_menu_matrice_ma.add_command(label="Matrice incidence",image=icon_mi ,command=matrice_incidence,compound=LEFT , accelerator="Ctrl+I")
menu_affichage.add_cascade(label="Matrices", image=icon_matrice,compound=LEFT, menu=sous_menu_matrice_ma)

# Menu Exécution 
menu_exe.add_command(label="Parours en Largeur ",image=icon_graphe ,compound=LEFT, command=parcours , accelerator="Ctrl+P")
menu_exe.add_command(label="Plus court chemin")

# Sous menu execution -- Colorage
sous_menu_exe = Menu(menu_exe, tearoff=0)
sous_menu_exe.add_command(label="Welsh And Powell",image=icon_wp , command=welsh_powell,compound=LEFT , accelerator="Ctrl+Shift+W")
menu_exe.add_cascade(label="Coloration" , image=icon_chemin ,compound=LEFT , menu=sous_menu_exe)

# Ajouter la barre de menu à la fenêtre principale
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_bar.add_cascade(label="Création", menu=menu_creation)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)
menu_bar.add_cascade(label="Exécution", menu=menu_exe)
menu_bar.add_cascade(label="Édition", menu=menu_edition)


fenetre.config(menu=menu_bar) # Appliquer la barre de menu à la fenêtre
fenetre.protocol("WM_DELETE_WINDOW", quitter_application) # Pour quitter l'application si le croix (X) est cliquer .
fenetre.mainloop() # Demarrer la boucle principale de l'interface