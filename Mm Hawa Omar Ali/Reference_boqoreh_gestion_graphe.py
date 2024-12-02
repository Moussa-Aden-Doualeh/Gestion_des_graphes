import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math
from collections import defaultdict
from tkinter import Toplevel, Text, END, messagebox



# Variables globales


sommets = []
aretes = []
creation_sommet = False # Variable qui indique si un sommet est en cours de création (True ou False)
creation_arete = False # Variable qui indique si une arête est en cours de création (True ou False)
sommet_selectionne = None # Variable qui garde l'index du sommet actuellement sélectionné, ou None s'il n'y a pas de sommet sélectionné
arete_orientee = None  # Définit à None pour ne pas mélanger les types d'arêtes
modifications = {} # Dictionnaire qui stocke les modifications dans le graphe pour chaque onglet (par exemple : canevas, sommets, arêtes)


# Fonction pour ajouter un nouvel onglet avec un canevas pour dessiner
def nouveau_fichier():
    global arete_orientee
    arete_orientee = None  # Réinitialise le type d'arête
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Nouveau fichier")
    notebook.select(tab)
   
    # Créer un canevas pour dessiner le graphe dans l'onglet
    canvas = tk.Canvas(tab, bg="white", width=600, height=400)
    canvas.pack(fill="both", expand=True)
   
    # Enregistrer le canevas et les données associées (sommets et arêtes)
    modifications[tab] = {"canvas": canvas, "sommets": [], "aretes": []}
   
    # Ajouter un gestionnaire d'événements de clic sur le canevas
    canvas.bind("<Button-1>", canvas_click)

# Fonction pour ouvrir un fichier
def ouvrir_fichier():
    global arete_orientee
    fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", ".txt"), ("Tous les fichiers", ".*")])
    if fichier:
        tab = tk.Frame(notebook)# Crée un nouvel onglet sous forme de cadre (Frame) dans le widget notebook
        notebook.add(tab, text=fichier.split('/')[-1])
        notebook.select(tab)
       
        # Créer un canevas pour dessiner le graphe dans l'onglet
        canvas = tk.Canvas(tab, bg="white", width=600, height=400)
        canvas.pack(fill="both", expand=True)
       
        # Enregistrer les données du fichier
        modifications[tab] = {"canvas": canvas, "sommets": [], "aretes": []}
       
        # Charger les données du fichier et les dessiner (si nécessaire)
        with open(fichier, 'r') as f:
            contenu = f.readlines()
            sommets = []
            aretes = []
            is_sommets = False
            is_aretes = False
            for ligne in contenu:
                if ligne.strip() == "Sommets:":
                    is_sommets = True
                    is_aretes = False
                elif ligne.strip() == "Arêtes:":
                    is_sommets = False
                    is_aretes = True
                elif is_sommets:
                    x, y = map(int, ligne.strip().split(','))
                    sommets.append((x, y))
                elif is_aretes:
                    s1, s2, orientee = ligne.strip().split(',')
                    aretes.append((int(s1), int(s2), bool(int(orientee))))
            # Dessiner le graphe avec les données chargées
            modifications[tab]["sommets"] = sommets
            modifications[tab]["aretes"] = aretes
            dessiner_graphe(tab)
           
            # Définir le type d'arête à partir du fichier
            if aretes:
                arete_orientee = aretes[0][2]

        canvas.bind("<Button-1>", canvas_click)  # Ajouter le gestionnaire d'événements pour le clic

# Fonction pour enregistrer un fichier
def enregistrer_fichier():
    tab = notebook.nametowidget(notebook.select())
    fichier = filedialog.asksaveasfilename(defaultextension=".txt")
    if fichier:
        # Enregistrer les sommets et les arêtes dans le fichier
        with open(fichier, 'w') as f:
            sommets = modifications[tab]["sommets"]
            aretes = modifications[tab]["aretes"]
            f.write(f"Sommets:\n")
            for (x, y) in sommets:
                f.write(f"{x},{y}\n")
            f.write(f"Arêtes:\n")
            for (s1, s2, orientee) in aretes:
                f.write(f"{s1},{s2},{int(orientee)}\n")  # Convertir l'orientation en 0 ou 1
        notebook.tab(tab, text=fichier.split('/')[-1])
        
# Fonction pour fermer un onglet et demander un enregistrement si nécessaire
def fermer_onglet():
    tab = notebook.nametowidget(notebook.select())
    if modifications[tab]["sommets"] or modifications[tab]["aretes"]:  # Vérifier si des modifications ont été faites
        reponse = messagebox.askyesnocancel("Enregistrer", "Voulez-vous enregistrer les modifications avant de fermer ?")
        if reponse:  # Si l'utilisateur choisit d'enregistrer
            enregistrer_fichier()
        elif reponse is None:  # Si l'utilisateur annule
            return
    notebook.forget(tab)

# Fonction pour quitter l'application
def quitter_application():
    root.quit()
    

"""Dans le menu cretion d'un graphe non_orientée creer les sommets et les arretes"""

# Fonction pour créer un sommet
def creer_sommet():
    global creation_sommet, creation_arete
    creation_sommet = True
    creation_arete = False

# Fonction pour créer une arête non orientée
def creer_arete_non_orientee():
    global creation_sommet, creation_arete, arete_orientee
    arete_orientee = False
    creation_sommet = False
    creation_arete = True

#Dessine une arête multiple entre deux sommets avec un décalage pour éviter les superpositions
def dessiner_arrete_multiple(canvas, x1, y1, x2, y2, count):
   
    offset = 5 * count  # Le décalage est basé sur le nombre d'arêtes déjà dessinées
    
    # Décaler légèrement l'arête pour la dessiner sans superposition
    canvas.create_line(x1 + offset, y1 + offset, x2 + offset, y2 + offset)

def dessiner_graphe(tab):
    canvas = modifications[tab]["canvas"]# Récupère le canevas (widget Canvas) associé à l'onglet 'tab' depuis le dictionnaire 'modifications'
    canvas.delete("all")
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]
   
    # Parcourt chaque sommet dans la liste 'sommets' avec son index
    for i, (x, y) in enumerate(sommets):
        # Dessiner un cercle noir pour représenter le sommet sur le canevas
        # (x-10, y-10) et (x+10, y+10) définissent le rectangle qui englobe l'ovale (ici, un cercle)
        # Le cercle est centré sur (x, y) avec un rayon de 10 pixels
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")
        # Ajouter un texte au centre du sommet pour afficher son numéro
        # Le numéro est calculé en prenant l'index i et en ajoutant 1 (pour commencer à 1)
        # Le texte sera blanc et sera placé à la position (x, y) du sommet
        canvas.create_text(x, y, text=str(i+1), fill="white")
   
    # Dessiner les arêtes (arrete non_orientée)
    arêtes_tracées = {}  # Pour compter et gérer les arêtes multiples entre les mêmes sommets
    # Parcourt chaque arête dans la liste 'aretes'
    # Chaque arête est définie par deux sommets (s1, s2) et l'orientation de l'arête (orientee)
    for s1, s2, orientee in aretes:
        x1, y1 = sommets[s1]# Récupère les coordonnées du sommet s1 (premier sommet de l'arête)
        x2, y2 = sommets[s2]

        # Identifier la paire de sommets de manière ordonnée pour éviter de traiter (s1, s2) et (s2, s1) séparément
        paire_sommets = tuple(sorted((s1, s2)))

        # Compter le nombre d'arêtes entre ces deux sommets
        # On vérifie si la paire de sommets (s1, s2) n'a pas encore été rencontrée dans 'arêtes_tracées'
        if paire_sommets not in arêtes_tracées:
            # Si la paire de sommets n'est pas encore présente, on l'ajoute à 'arêtes_tracées'
            # avec un compteur initialisé à 0
            arêtes_tracées[paire_sommets] = 0

        # Utiliser le compteur pour tracer l'arête avec un décalage si nécessaire
        # Récupérer le compteur actuel pour la paire de sommets 'paire_sommets'
        count = arêtes_tracées[paire_sommets]
        # Incrémenter le compteur pour cette paire de sommets
        arêtes_tracées[paire_sommets] += 1

        if s1 == s2:  # Cas d'une boucle (arête reliant un sommet à lui-même)
            draw_arrow(canvas, x1, y1, x1, y1)  # Dessiner la boucle 
        elif orientee:  # Cas d'une arête orientée
            draw_arrow(canvas, x1, y1, x2, y2)
        else:  # Cas d'une arête non orientée
            # Appeler la fonction pour dessiner l'arête avec un décalage si multiple
            dessiner_arrete_multiple(canvas, x1, y1, x2, y2, count)


"""Dans le menu cretion d'un graphe orientée creer les sommets et les arretes"""

# Fonction pour créer une arête orientée
def creer_arete_orientee():
    global creation_sommet, creation_arete, arete_orientee
    arete_orientee = True
    creation_sommet = False
    creation_arete = True

# Fonction pour dessiner une flèche (arête orientée) ou une boucle
def draw_arrow(canvas, x1, y1, x2, y2):
    if (x1, y1) == (x2, y2):  # Cas d'une boucle
        # Dessiner une boucle comme un arc
        radius = 20  # Rayon de la boucle
        canvas.create_arc(
            x1 - radius, y1 - radius - 20,  # Coin supérieur gauche de la boîte englobante
            x1 + radius, y1 + radius - 20,  # Coin inférieur droit de la boîte englobante
            start=0, extent=300, style=tk.ARC, width=2
        )
    else:  # Cas d'une arête normale
        angle = math.atan2(y2 - y1, x2 - x1)
        x_arrow = x2 - 15 * math.cos(angle)
        y_arrow = y2 - 15 * math.sin(angle)
        canvas.create_line(x1, y1, x_arrow, y_arrow, arrow=tk.LAST)
        
# Fonction pour gérer le clic de l'utilisateur dans le canevas (lorsqu'un utilisateur clique sur le canevas)
def canvas_click(event):
    # Récupère les coordonnées (x, y) du clic de souris dans le canevas
    global sommet_selectionne
    x, y = event.x, event.y
    
    # Récupère l'onglet actuel et le canevas associé à cet onglet
    tab = notebook.nametowidget(notebook.select())
    canvas = modifications[tab]["canvas"]
    
    # Récupère les listes de sommets et d'arêtes du graphe
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]
   
    # Si on est en mode de création de sommet
    if creation_sommet:
        # Ajouter un nouveau sommet à la liste avec les coordonnées du clic
        sommets.append((x, y))
        # Redessiner le graphe avec le nouveau sommet ajouté
        dessiner_graphe(tab)
    
    # Si on est en mode de création d'arête
    elif creation_arete:
        # Vérifier chaque sommet pour savoir si le clic est proche de ce sommet
        for i, (sx, sy) in enumerate(sommets):
            # Calcul de la distance entre le clic et le sommet actuel (avec hypot pour la distance euclidienne)
            if math.hypot(sx - x, sy - y) <= 10:
                # Si aucun sommet n'a été sélectionné, on sélectionne ce sommet
                if sommet_selectionne is None:
                    sommet_selectionne = i
                # Sinon, on ajoute une arête entre le sommet sélectionné et le sommet cliqué
                else:
                    aretes.append((sommet_selectionne, i, arete_orientee))
                    # Réinitialiser la sélection de sommet après avoir ajouté l'arête
                    sommet_selectionne = None
                    # Redessiner le graphe après avoir ajouté l'arête
                    dessiner_graphe(tab)
                break


"""Dans le menus affichage La matrice d'ajacence du graphe non_orientée"""
    
def matrice_adjacence_non_orientée():
    # Récupérer les données du graphe actuel
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]

    # Nombre de sommets dans le graphe
    n = len(sommets)

    # Créer une matrice d'adjacence initialisée à 0
    matrice = [[0 for _ in range(n)] for _ in range(n)]

    # Dictionnaire pour compter le nombre d'arêtes multiples entre les sommets
    arêtes_tracées = {}

    # Remplir la matrice d'adjacence en fonction des arêtes
    for s1, s2, orientee in aretes:
        if s1 == s2:  # Cas d'une boucle (arête reliant un sommet à lui-même)
            matrice[s1][s1] += 1  # Incrémenter pour chaque boucle (plusieurs boucles possibles)
        else:
            # Identifier la paire de sommets (triée pour éviter les doublons)
            paire_sommets = tuple(sorted((s1, s2)))

            # Compter les arêtes multiples
            if paire_sommets not in arêtes_tracées:
                arêtes_tracées[paire_sommets] = 0

            arêtes_tracées[paire_sommets] += 1

            # Mettre à jour la matrice d'adjacence avec le nombre d'arêtes multiples
            matrice[s1][s2] = arêtes_tracées[paire_sommets]
            matrice[s2][s1] = arêtes_tracées[paire_sommets]  # Graphe non orienté

    # Créer une nouvelle fenêtre pour afficher la matrice
    fenetre_matrice = tk.Toplevel(root)
    fenetre_matrice.title("Matrice d'Adjacence")

    # Créer un widget Text pour afficher la matrice
    text_widget = tk.Text(fenetre_matrice, wrap=tk.WORD, width=70, height=40)
    text_widget.pack(padx=45, pady=5)

    # Ajouter les sommets dans la première ligne et la première colonne
    matrice_text = "    "  # Espaces avant les indices des colonnes
    for i in range(n):
        matrice_text += f"  {i+1} "  # Ajouter les indices des colonnes
    matrice_text += "\n"

    # Ajouter les lignes de la matrice avec les indices des sommets
    for i in range(n):
        matrice_text += f" {i+1} "  # Ajouter l'indice du sommet pour chaque ligne
        for j in range(n):
            matrice_text += f"  {matrice[i][j]} "  # Ajouter les valeurs de la matrice
        matrice_text += "\n"

    # Insérer la matrice dans le widget Text
    text_widget.insert(tk.END, matrice_text)

    # Désactiver l'édition dans le widget Text
    text_widget.config(state=tk.DISABLED)

    
def matrice_incidence_non_orientée():
    # Récupérer les données du graphe actuel
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]

    # Noms des sommets (numéros) et arêtes (lettres)
    noms_sommets = [str(i + 1) for i in range(len(sommets))]  # '1', '2', '3', etc.
    noms_aretes = [chr(65 + i) for i in range(len(aretes))]  # 'A', 'B', 'C', etc.

    # Nombre de sommets et d'arêtes dans le graphe
    n_sommets = len(sommets)
    n_aretes = len(aretes)

    # Créer une matrice d'incidence initialisée à 0
    matrice = [[0 for _ in range(n_aretes)] for _ in range(n_sommets)]

    # Remplir la matrice d'incidence en utilisant vos conditions
    for j, (s1, s2, orientee) in enumerate(aretes):
        # Condition 1 : vérifie si le sommet est l'un des sommets de l'arête
        for i, sommet in enumerate(sommets):
            if sommet == sommets[s1] or sommet == sommets[s2]:
                # Condition 2 : vérifie si les coordonnées correspondent
                if sommets[s1] == sommet and sommets[s2] == sommet:
                    matrice[i][j] = 2
                else:
                    matrice[i][j] = 1
            else:
                matrice[i][j] = 0

    # Créer une nouvelle fenêtre pour afficher la matrice
    fenetre_matrice = tk.Toplevel(root)
    fenetre_matrice.title("Matrice d'Incidence (Conditions)")

    # Créer un widget Text pour afficher la matrice
    text_widget = tk.Text(fenetre_matrice, wrap=tk.WORD, width=70, height=45)
    text_widget.pack(padx=45, pady=45)

    # Ajouter les noms des arêtes dans la première ligne
    matrice_text = "   "  # Espaces avant les noms des arêtes
    for nom in noms_aretes:
        matrice_text += f"  {nom} "  # Ajouter les noms des arêtes
    matrice_text += "\n"

    # Ajouter les lignes de la matrice avec les indices des sommets
    for i, nom_sommet in enumerate(noms_sommets):
        matrice_text += f"{nom_sommet}  "  # Ajouter le numéro du sommet pour chaque ligne
        for j in range(n_aretes):
            matrice_text += f"  {matrice[i][j]} "  # Ajouter les valeurs de la matrice
        matrice_text += "\n"

    # Insérer la matrice dans le widget Text
    text_widget.insert(tk.END, matrice_text)

    # Désactiver l'édition dans le widget Text
    text_widget.config(state=tk.DISABLED)

"""Dans le menus affichage la chaine eulerien et hamiltonien du graphe non_orientée"""

# Fonction pour trouver une chaîne eulérienne
def chaine_eulerienne():
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]
    
    # Créer un defaultdict avec une valeur par défaut de liste vide
    graph = defaultdict(list)
    # Ajouter des éléments sans se soucier de vérifier si la clé existe déjà
    for s1, s2, _ in aretes:
        graph[s1].append(s2)
        graph[s2].append(s1)

    # Vérifier les degrés des sommets
    odd_vertices = [v for v in graph if len(graph[v]) % 2 == 1]
    if len(odd_vertices) not in [0, 2]:
        nouvelle_fenetre = Toplevel()
        nouvelle_fenetre.title("Résultat")
        text_widget = Text(nouvelle_fenetre, wrap="word", height=5, width=50)
        text_widget.insert(END, "Pas de chaîne eulérienne : car plus de deux sommets ont un degré impair.")
        text_widget.pack(padx=10, pady=10)
        text_widget.config(state="disabled")
        return
    
    # Trouver la chaîne eulérienne (Fleury's Algorithm)
    def find_eulerian_path(start):
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            if graph[current]:
                next_sommet = graph[current].pop()
                graph[next_sommet].remove(current)  # Enlever l'arête
                stack.append(next_sommet)
            else:
                path.append(stack.pop())
        return path

    # Déterminer le point de départ
    start = odd_vertices[0] if odd_vertices else list(graph.keys())[0]
    eulerian_path = find_eulerian_path(start)
    
    # Affichage du résultat
    chaine = " -> ".join(str(s + 1) for s in eulerian_path[::-1])
    nouvelle_fenetre = Toplevel()
    nouvelle_fenetre.title("Chaîne Eulérienne")
    text_widget = Text(nouvelle_fenetre, wrap="word", height=10, width=50)
    text_widget.insert(END, f"Chaîne eulérienne trouvée :\n{chaine}")
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state="disabled")


from tkinter import Toplevel, Text, END

# Fonction pour trouver une chaîne hamiltonienne
def chaine_hamiltonienne():
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]
    
#ce fonction permet de trouver un chemin dans un graphe qui couvre tous les sommets une seule fois
    def backtrack(path, visited):
        # Si tous les sommets ont été visités (la taille du chemin est égale au nombre de sommets)
        if len(path) == len(sommets):  # Si tous les sommets sont visités
            return path
        
        # Récupérer le dernier sommet du chemin actuel
        current = path[-1]
        # Parcourir toutes les arêtes du graphe
        for s1, s2, _ in aretes:
            next_sommet = None
            if s1 == current and s2 not in visited:
                next_sommet = s2
            elif s2 == current and s1 not in visited:
                next_sommet = s1
            
            if next_sommet is not None:
                result = backtrack(path + [next_sommet], visited | {next_sommet})
                if result:  # Si une solution est trouvée
                    return result
        return None

    # Rechercher une chaîne hamiltonienne
    for start in range(len(sommets)):
        result = backtrack([start], {start})
        if result:
            chaine = " -> ".join(str(s + 1) for s in result)
            
            # Affichage dans une nouvelle fenêtre
            nouvelle_fenetre = Toplevel()
            nouvelle_fenetre.title("Chaîne Hamiltonienne")
            text_widget = Text(nouvelle_fenetre, wrap="word", height=10, width=50)
            text_widget.insert(END, f"Chaîne hamiltonienne trouvée :\n{chaine}")
            text_widget.pack(padx=10, pady=10)
            text_widget.config(state="disabled")  # Rendre le texte non modifiable
            return
    
    # Si aucune chaîne n'est trouvée, afficher une autre fenêtre avec le message
    nouvelle_fenetre = Toplevel()
    nouvelle_fenetre.title("Résultat")
    text_widget = Text(nouvelle_fenetre, wrap="word", height=5, width=50)
    text_widget.insert(END, "Pas de chaîne hamiltonienne trouvée.")
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state="disabled")  # Rendre le texte non modifiable
    

"""Dans le menus affichage La matrice d'ajacence et incidence du graphe orientée"""

def matrice_adjacence_orientee():
    # Récupérer les données du graphe actuel
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]

    # Nombre de sommets dans le graphe
    n = len(sommets)

    # Initialiser un dictionnaire pour stocker les voisins (arêtes orientées)
    voisins = {i: [] for i in range(n)}
    for s1, s2, orientee in aretes:
        if orientee:  # Si l'arête est orientée
            voisins[s1].append(s2)
        else:  # Si l'arête est non orientée
            voisins[s1].append(s2)
            voisins[s2].append(s1)

    # Créer une matrice d'adjacence
    matrice = []
    for sommet_dep in range(n):
        adjacence = []
        for sommet_arr in range(n):
            # Vérifie si sommet_dep a une arête vers sommet_arr
            adjacence.append(1 if sommet_arr in voisins[sommet_dep] else 0)
        matrice.append(adjacence)

    # Créer une nouvelle fenêtre pour afficher la matrice
    fenetre_matrice = tk.Toplevel(root)
    fenetre_matrice.title("Matrice d'Adjacence Orientée")

    # Créer un widget Text pour afficher la matrice
    text_widget = tk.Text(fenetre_matrice, wrap=tk.WORD, width=70, height=45)
    text_widget.pack(padx=45, pady=45)

    # Ajouter les noms des sommets dans la première ligne
    matrice_text = "     "  # Espaces avant les indices des colonnes
    for i in range(n):
        matrice_text += f"  {i+1} "  # Ajouter les indices des colonnes pour les sommets
    matrice_text += "\n"

    # Ajouter les lignes de la matrice avec les indices des sommets
    for i in range(n):
        matrice_text += f" {i+1} "  # Ajouter le numéro du sommet pour chaque ligne
        for j in range(n):
            matrice_text += f"  {matrice[i][j]} "  # Ajouter les valeurs de la matrice
        matrice_text += "\n"

    # Insérer la matrice dans le widget Text
    text_widget.insert(tk.END, matrice_text)

    # Désactiver l'édition dans le widget Text
    text_widget.config(state=tk.DISABLED)
    

def matrice_incidence_orientee():
    # Récupérer les données du graphe actuel
    tab = notebook.nametowidget(notebook.select())
    sommets = modifications[tab]["sommets"]
    aretes = modifications[tab]["aretes"]

    # Vérifier qu'il y a des sommets et des arêtes
    if not sommets:
        messagebox.showinfo("Info", "Aucun sommet n'est défini dans ce graphe.")
        return
    if not aretes:
        messagebox.showinfo("Info", "Aucune arête n'est définie dans ce graphe.")
        return

    # Nombre de sommets et d'arêtes
    n = len(sommets)
    m = len(aretes)

    # Créer une matrice d'incidence initialisée à 0
    matrice = [[0 for _ in range(m)] for _ in range(n)]

    # Remplir la matrice d'incidence selon les conditions
    for j, (s1, s2, orientee) in enumerate(aretes):
        if orientee:  # Si l'arête est orientée
            if s1 == s2:
                matrice[s1][j] = 0  # Boucle
            else:
                matrice[s1][j] = -1  # Arête sortante
                matrice[s2][j] = 1   # Arête entrante

    # Créer une nouvelle fenêtre pour afficher la matrice
    fenetre_matrice = tk.Toplevel(root)
    fenetre_matrice.title("Matrice d'Incidence Orientée")

    # Créer un widget Text pour afficher la matrice
    text_widget = tk.Text(fenetre_matrice, wrap=tk.WORD, width=70, height=25)
    text_widget.pack(padx=45, pady=45)

    # Ajouter les noms des arêtes en haut (A, B, C...)
    matrice_text = "     "  # Espaces avant les indices des colonnes
    for j in range(m):
        matrice_text += f"  {chr(65 + j)} "  # Utiliser des lettres pour les arêtes
    matrice_text += "\n"

    # Ajouter les lignes de la matrice avec les indices des sommets
    for i in range(n):
        matrice_text += f" {i+1} "  # Ajouter le numéro du sommet pour chaque ligne
        for j in range(m):
            matrice_text += f"  {matrice[i][j]} "  # Ajouter les valeurs de la matrice
        matrice_text += "\n"

    # Insérer la matrice dans le widget Text
    text_widget.insert(tk.END, matrice_text)

    # Désactiver l'édition dans le widget Text
    text_widget.config(state=tk.DISABLED)
    





# Interface principale
root = tk.Tk()
root.title("Création de graphes")
# Agrandir la fenêtre principale
root.geometry("600x400")  # Largeur: 1000px, Hauteur: 600px

# Création de l'onglet principal
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Barre de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
      
# Menu Fichier
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_fichier.add_command(label="Nouveau", command=nouveau_fichier)
menu_fichier.add_command(label="Ouvrir", command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", command=enregistrer_fichier)
menu_fichier.add_command(label="Fermer", command=fermer_onglet)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=quitter_application)

# Menu "Création" avec sous-menu "Graphe"
menu_creation = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Création", menu=menu_creation)

graphe = tk.Menu(menu_creation, tearoff=0)
menu_creation.add_cascade(label="graphe", menu=graphe)
# Associer les commandes des chaînes aux options de menu

# Ajout des options pour le menu 'Création'
graphe.add_command(label="Sommet", command=creer_sommet)

arete = tk.Menu(graphe, tearoff=0)
graphe.add_cascade(label="Arete", menu=arete)
arete.add_command(label="Orientée", command=creer_arete_orientee)
arete.add_command(label="Non Orientée", command=creer_arete_non_orientee)

# Ajout du menu 'Affichage'
menu_affichage = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)


# Associer les commandes aux options de menu
graphe = tk.Menu(menu_affichage, tearoff=0)
menu_affichage.add_cascade(label="graphe", menu=graphe)

Orientée = tk.Menu(graphe, tearoff=0)
graphe.add_cascade(label="Orientée", menu=Orientée)

Non_Orientée = tk.Menu(graphe, tearoff=0)
graphe.add_cascade(label="Non_Orientée", menu=Non_Orientée)


Orientée.add_command(label="Matrice d'adjacence", command=matrice_adjacence_orientee)
Orientée.add_command(label="Matrice d'incidence ", command=matrice_incidence_orientee)
Non_Orientée.add_command(label="Matrice d'adjacence ", command=matrice_adjacence_non_orientée)
Non_Orientée.add_command(label="Matrice d'incidence ", command=matrice_incidence_non_orientée)

chaine= tk.Menu(Non_Orientée, tearoff=0)
Non_Orientée.add_cascade(label="chaine", menu=chaine)
chaine.add_command(label="Chaîne eulérienne", command=chaine_eulerienne)
chaine.add_command(label="Chaîne hamiltonienne", command=chaine_hamiltonienne)

# Menus Affichage, Exécution et Édition
menu_bar.add_cascade(label="Exécution", menu=tk.Menu(menu_bar, tearoff=0))
menu_bar.add_cascade(label="Édition", menu=tk.Menu(menu_bar, tearoff=0))

# Démarrer l'application
root.mainloop()