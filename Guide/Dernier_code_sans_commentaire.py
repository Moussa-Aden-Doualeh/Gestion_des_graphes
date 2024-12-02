
import tkinter as tk
from tkinter import Menu, filedialog, messagebox
from tkinter import ttk
import math
from tkinter import * # pour importer le bibliotheque de l'interface graphique .
from tkinter import simpledialog  as zone_dialogue # Pour les boîtes de dialogue de saisie
from tkinter import messagebox as boite_message # Pour les gestions de messages d'erreur et notifications
from tkinter import filedialog as dialogue_fichier  # Pour la boîte de dialogue "Ouvrir un fichier"

from PIL import Image, ImageTk  # Importer Pillow pour la gestion des images

import networkx as nx
import matplotlib.pyplot as plt

# Dictionnaire pour stocker les sommets et arretes de chaque onglet
tab_data = {}
modifications= {}

# Variables globales pour la creation
creation_sommet = False
creation_arete = False
arete_orientee = False
retirer_mode = False
sommet_selectionne = None  # Sommet selectionnee pour ajouter une arrete
current_file = None  # Fichier en cours pour chaque onglet

graphe_orientee = None  # None signifie que le type n'est pas encore defini

# Creer la fenetre principale
fenetre = tk.Tk()
fenetre.title("Interface Graphique")
fenetre.geometry("800x600")

# Creer un widget Notebook pour les onglets
notebook = ttk.Notebook(fenetre)
notebook.pack(expand=1, fill='both')

# Variable globale pour compter les fichiers
fichier_count = 1

# Fonction pour gerer le clic sur "Nouveau" (ajouter un nouvel onglet)
def nouveau():
    global graphe_orientee, fichier_count
    graphe_orientee = None  # Réinitialiser pour un nouveau graphe
    
    # Créer un nouvel onglet
    new_tab = tk.Frame(notebook)
    canvas = tk.Canvas(new_tab, bg='white')
    canvas.pack(expand=1, fill='both')
    canvas.bind("<Button-1>", lambda event: canvas_click(event, canvas))
    
    # Ajouter un nouvel onglet avec un nom incrémenté
    notebook.add(new_tab, text=f"Fichier {fichier_count}")
    notebook.select(new_tab)
    
    # Mettre à jour le compteur pour le prochain fichier
    fichier_count += 1
    
    # Stocker les données de cet onglet
    tab_data[new_tab] = {'sommets': [], 'aretes': [], 'file_path': None}

# Fonction pour ouvrir un fichier existantt
def ouvrir_fichier():
    global graphe_orientee
    graphe_orientee=None # Reatialiser , le typz sera determiner par le conten du fichier
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers Python", "*.py")])
    if file_path:
        new_tab = tk.Frame(notebook)
        canvas = tk.Canvas(new_tab, bg='white')
        canvas.pack(expand=1, fill='both')
        canvas.bind("<Button-1>", lambda event: canvas_click(event, canvas))
        notebook.add(new_tab, text=file_path.split('/')[-1])
        notebook.select(new_tab)

        with open(file_path, 'r') as file:
            contenu = file.read()

        tab_data[new_tab] = {'sommets': [], 'aretes': [], 'file_path': file_path}
        charger_graphe(contenu, canvas, new_tab)


def enregistrer_fichier():
    # Récupérer l'onglet sélectionné
    current_tab = notebook.nametowidget(notebook.select())  # Onglet sélectionné
    
    # Vérifier si l'onglet existe dans tab_data
    if current_tab not in tab_data:
        messagebox.showerror("Erreur", "Onglet non trouvé dans les données")
        return
    
    # Récupérer le chemin du fichier à partir des données de l'onglet
    file_path = tab_data[current_tab].get('file_path')  # Chemin du fichier
    
    # Vérifier si le canvas est vide (pas de sommets ni d'arêtes)
    if not tab_data[current_tab]['sommets'] and not tab_data[current_tab]['aretes']:
        # Si le canvas est vide, afficher un message demandant de créer un graphe
        messagebox.showinfo("Attention", "Veuillez créer un graphe avant d'enregistrer.")
    else:
        if not file_path:  # Si pas encore enregistré, utiliser 'Enregistrer sous'
            enregistrer_sous()  # Appel à la fonction "Enregistrer sous"
        else:
            # Si le fichier existe déjà, on l'enregistre
            with open(file_path, 'w') as file:
                # Sauvegarder les données du graphe dans le fichier
                file.write(sauvegarder_graphe(current_tab))


def enregistrer_sous():
    # Récupérer l'onglet sélectionné
    current_tab = notebook.nametowidget(notebook.select())  # Onglet sélectionné
    
    # Vérifier si l'onglet existe dans tab_data
    if current_tab not in tab_data:
        messagebox.showerror("Erreur", "Onglet non trouvé dans les données")
        return
    
    # Vérifier si le canvas est vide (pas de sommets ni d'arêtes)
    if not tab_data[current_tab]['sommets'] and not tab_data[current_tab]['aretes']:
        # Si le canvas est vide, afficher un message demandant de créer un graphe
        messagebox.showinfo("Attention", "Veuillez créer un graphe avant d'enregistrer.")
    else:
        # Demander à l'utilisateur où enregistrer le fichier
        fichier = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Fichiers Python", "*.py")])
        
        if fichier:
            # Enregistrer le chemin du fichier dans les données de l'onglet
            tab_data[current_tab]['file_path'] = fichier
            
            # Mettre à jour le nom de l'onglet avec le nom du fichier
            notebook.tab(current_tab, text=fichier.split('/')[-1])
            
            # Sauvegarder le graphe dans le fichier
            with open(fichier, 'w') as file:
                file.write(sauvegarder_graphe(current_tab))

# Fonction pour fermer l'onglet actuel
def fermer_fichier():
    # Vérifier s'il y a des onglets ouverts
    if notebook.index("end") == 0:
        # Aucun onglet n'est ouvert
        messagebox.showinfo("Attention", "Impossible de Fermer, Aucun Onglet est ouvert")
    else:
        # Obtenir l'onglet courant
        current_tab = notebook.select()
        
        # Fermer l'onglet
        notebook.forget(current_tab)
        
        # Vérifier et supprimer les données associées à l'onglet, si elles existent
        if current_tab in tab_data:
            del tab_data[current_tab]

# Fonction pour quitter l'application
def quitter_application():
    confirmation = messagebox.askyesno("Quitter", "etes-vous sur de vouloir quitter?")
    if confirmation:
        fenetre.quit()

# Fonctions pour creer des sommets et des arretes
def creer_sommet():
    global creation_sommet, creation_arete
    creation_sommet = True
    creation_arete = False


def creer_arete_oriente():
    global creation_sommet, creation_arete, arete_orientee, graphe_orientee
    if graphe_orientee is None or graphe_orientee is True:
        creation_sommet = False
        creation_arete = True
        arete_orientee = True
        graphe_orientee = True  # Definir le type de graphe comme orientee
    else:
        messagebox.showerror("Erreur", "Ce graphe est defini comme non orientee. Veuillez continuer avec des arretes non orientees.")


def creer_arete_non_oriente():
    global creation_sommet, creation_arete, arete_orientee, graphe_orientee
    if graphe_orientee is None or graphe_orientee is False:
        creation_sommet = False
        creation_arete = True
        arete_orientee = False
        graphe_orientee = False  # Definir le type de graphe comme non orientee
    else:
        messagebox.showerror("Erreur", "Ce graphe est defini comme orientee. Veuillez continuer avec des arretes orientees.")



# Fonction pour retirer un sommet par clic
def retirer_sommet_par_clic(event, canvas):
    global sommet_selectionne
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    x, y = event.x, event.y

    # Identifier le sommet cliqué
    sommet_clique = None
    for i, (sx, sy, nom_sommet) in enumerate(sommets):
        if math.sqrt((sx - x) ** 2 + (sy - y) ** 2) <= 10:  # Rayon de 10 pour détecter le clic
            sommet_clique = i
            break

    if sommet_clique is None:
        messagebox.showinfo("Retirer sommet", "Aucun sommet sélectionné.")
        return

    # Supprimer les arêtes associées au sommet
    data['aretes'] = [arete for arete in aretes if sommet_clique not in (arete[0], arete[1])]

    # Supprimer le sommet
    data['sommets'].pop(sommet_clique)

    # Ré-indexer les arêtes après suppression
    data['aretes'] = [
        (s1 - (1 if s1 > sommet_clique else 0), s2 - (1 if s2 > sommet_clique else 0), orientee, nom_arete)
        for s1, s2, orientee, nom_arete in data['aretes']
    ]

    # Redessiner le graphe
    dessiner_graphe(canvas, current_tab)
# Greer les clics sur le canevas
def canvas_click(event, canvas):
    global sommet_selectionne, creation_sommet, creation_arete, retirer_mode
    if retirer_mode:
        retirer_sommet_par_clic(event, canvas)
        return

    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    x, y = event.x, event.y
    if creation_sommet:
        # Ajouter un sommet avec un nom unique
        nom_sommet = f"S{len(sommets) + 1}"
        sommets.append((x, y, nom_sommet))
        dessiner_graphe(canvas, current_tab)
    elif creation_arete:
        for i, (sx, sy, nom_sommet) in enumerate(sommets):
            if math.sqrt((sx - x) ** 2 + (sy - y) ** 2) <= 30:
                if sommet_selectionne is None:
                    sommet_selectionne = i
                else:
                    # Ajouter une arrete avec un nom unique
                    nom_arete = f"A{len(aretes) + 1}"
                    aretes.append((sommet_selectionne, i, arete_orientee, nom_arete))
                    sommet_selectionne = None
                    dessiner_graphe(canvas, current_tab)
                    break



def dessiner_graphe(canvas, current_tab):
    canvas.delete("all")  # Nettoyer le canevas
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    # Fonction pour vérifier si la distance entre deux sommets est inférieure à 60 pixels
    def est_trop_proche(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) < 60

    # Dessiner les sommets
    for i, (x, y, nom_sommet) in enumerate(sommets):
        # Vérifier si le sommet est trop proche des autres
        for j, (other_x, other_y, _) in enumerate(sommets):
            if i != j and est_trop_proche(x, y, other_x, other_y):
                # Afficher un message d'erreur si les sommets sont trop proches
                messagebox.showerror("Erreur", "Impossible de placer des sommets très proches")
                return  # Sortir de la fonction et ne pas dessiner de nouveaux sommets

        # Dessiner le sommet
        canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue")
        canvas.create_text(x, y, text=nom_sommet, fill="white")

    # Dessiner les arêtes
    for s1, s2, orientee, nom_arete in aretes:
        x1, y1, _ = sommets[s1]
        x2, y2, _ = sommets[s2]
        if orientee:
            draw_arrow(canvas, x1, y1, x2, y2)
        else:
            canvas.create_line(x1, y1, x2, y2)
        # Afficher le nom de l'arête au milieu
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_text(xm, ym, text=nom_arete, fill="red")



def draw_arrow(canvas, x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1)
    x_arrow = x2 - 15 * math.cos(angle)
    y_arrow = y2 - 15 * math.sin(angle)
    canvas.create_line(x1, y1, x_arrow, y_arrow, arrow=tk.LAST)


# Greer les clics sur le canevas
def canvas_click(event, canvas):
    global sommet_selectionne, creation_sommet, creation_arete
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    x, y = event.x, event.y
    if creation_sommet:
        # Ajouter un sommet avec un nom unique
        nom_sommet = f"S{len(sommets) + 1}"
        sommets.append((x, y, nom_sommet))
        dessiner_graphe(canvas, current_tab)
    elif creation_arete:
        for i, (sx, sy, nom_sommet) in enumerate(sommets):
            if math.sqrt((sx - x) ** 2 + (sy - y) ** 2) <= 30:
                if sommet_selectionne is None:
                    sommet_selectionne = i
                else:
                    # Ajouter une arrete avec un nom unique
                    nom_arete = f"A{len(aretes) + 1}"
                    aretes.append((sommet_selectionne, i, arete_orientee, nom_arete))
                    sommet_selectionne = None
                    dessiner_graphe(canvas, current_tab)
                    break

def sauvegarder_graphe(current_tab):
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    contenu = f"sommets = {sommets}\naretes = {aretes}\n"
    return contenu

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
        messagebox.showerror("Erreur", f"Erreur lors du chargement : {e}")


# Fonction pour afficher la matrice d'adjacence
def afficher_matrice_adjacente():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    n = len(sommets)
    matrice = [[0] * n for _ in range(n)]
    
    for s1, s2, orientee,nom_arete in aretes:
        matrice[s1][s2] = 1
        if not orientee:
            matrice[s2][s1] = 1

    afficher_matrice(matrice, "Matrice d'adjacence")

# Fonction pour afficher la matrice d'incidence

def afficher_matrice_incidence():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    aretes = data['aretes']
    sommets = data['sommets']

    # Initialisation de la matrice d'incidence
    n_sommets = len(sommets)
    n_aretes = len(aretes)
    matrice_incidence = [[0] * n_aretes for _ in range(n_sommets)]

    # Remplir la matrice d'incidence
    for j, (s1, s2, orientee, nom_arete) in enumerate(aretes):
        matrice_incidence[s1][j] = 1
        matrice_incidence[s2][j] = -1
        if orientee:
            matrice_incidence[s1][j] = 1
            matrice_incidence[s2][j] = 0
        else:
            matrice_incidence[s1][j] = 1
            matrice_incidence[s2][j] = 1

    # Appeler la fonction pour afficher la matrice avec les noms des arretes
    afficher_matrice(matrice_incidence, "Matrice d'incidence", [nom_arete for _, _, _, nom_arete in aretes])

# Fonction pour afficher la cha?ne eulerienne (simplifiee)

def afficher_chaine_eulerienne():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    # Construire une representation du graphe
    graphe = {i: [] for i in range(len(sommets))}
    for s1, s2, orientee, nom_arete in aretes:
        graphe[s1].append((s2, nom_arete))
        if not orientee:
            graphe[s2].append((s1, nom_arete))

    # Verifier les sommets de degre impair
    odd_vertices = [v for v in graphe if len(graphe[v]) % 2 != 0]
    if len(odd_vertices) not in [0, 2]:
        messagebox.showinfo("Chaine eulerienne", "Aucune chaine eulerienne n'existe.")
        return

    # Trouver une cha?ne eulerienne
    def find_eulerian_path(v, path):
        while graphe[v]:
            next_vertex, edge_name = graphe[v].pop()
            graphe[next_vertex].remove((v, edge_name))  # Enlever l'arrete
            find_eulerian_path(next_vertex, path)
        path.append(v)

    start_vertex = odd_vertices[0] if odd_vertices else 0
    path = []
    find_eulerian_path(start_vertex, path)

    chaine = " -> ".join(f"S{i + 1}" for i in path[::-1])
    messagebox.showinfo("Chaine eulerienne", f"Chaine eulerienne trouvee : {chaine}")


# Fonction pour afficher la cha?ne hamiltonienne (simplifiee)
def afficher_chaine_hamiltonienne():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    # Construire une representation du graphe
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

    for start_vertex in range(n):
        visited = {start_vertex}
        path = [start_vertex]
        result = hamiltonian_path(start_vertex, visited, path)
        if result:
            chaine = " -> ".join(f"S{i + 1}" for i in result)
            messagebox.showinfo("Chaine hamiltonienne", f"Chaine hamiltonienne trouvee : {chaine}")
            return

    messagebox.showinfo("Chaine hamiltonienne", "Aucune chaine hamiltonienne n'existe.")

# Fonction pour afficher une matrice dans une nouvelle fenetre
def afficher_matrice(matrice, titre,en_tetes_aretes=None):
    fenetre_matrice = tk.Toplevel(fenetre)
    fenetre_matrice.title(titre)
    
    # Ajouter les en-tetes pour les noms des sommets
    for i in range(len(matrice)):
        label = tk.Label(fenetre_matrice, text=f"S{i+1}", borderwidth=1, relief="solid", width=5, bg="lightgray")
        label.grid(row=0, column=i+1)
        label = tk.Label(fenetre_matrice, text=f"S{i+1}", borderwidth=1, relief="solid", width=5, bg="lightgray")
        label.grid(row=i+1, column=0)
    # Afficher les noms des aretes en en-tete si fourni
    if en_tetes_aretes:
        for j, nom in enumerate(en_tetes_aretes):
            label=tk.Label(fenetre_matrice, text=nom, borderwidth=1, relief="solid", width=5, bg="lightgray")
            label.grid(row=0, column=j+1)
    
    # Afficher les valeurs de la matrice
    for i, ligne in enumerate(matrice):
        for j, valeur in enumerate(ligne):
            label = tk.Label(fenetre_matrice, text=valeur, borderwidth=1, relief="solid", width=5)
            label.grid(row=i+1, column=j+1)

#Fonction pour le parcours en profondeur

def trouver_sommet_depart(sommets, aretes, orientee):
    if orientee:
        # Compter les arretes entrantes pour chaque sommet
        entrees = {i: 0 for i in range(len(sommets))}
        for s1, s2, _, _ in aretes:
            entrees[s2] += 1
        # Trouver le sommet sans arretes entrantes
        for sommet, nb_entrees in entrees.items():
            if nb_entrees == 0:
                return sommet
    # Si aucun sommet sans arretes entrantes ou graphe non oriente
    return min(range(len(sommets)))  # Le sommet avec le plus petit indice


    
def dfs(sommet, visited, aretes, orientee, chemin):
    visited.add(sommet)
    chemin.append(sommet)
    for s1, s2, _, _ in aretes:
        if s1 == sommet and s2 not in visited:
            dfs(s2, visited, aretes, orientee, chemin)



def effectuer_parcours_profondeur():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']
    
    if not sommets:
        messagebox.showinfo("Parcours en profondeur", "Aucun sommet dans le graphe.")
        return
    
    orientee = any(a[2] for a in aretes)  # Determiner si le graphe est oriente
    sommet_depart = trouver_sommet_depart(sommets, aretes, orientee)
    
    visited = set()
    chemin = []
    dfs(sommet_depart, visited, aretes, orientee, chemin)
    
    # Afficher le chemin parcouru
    chemin_noms = [sommets[s][2] for s in chemin]  # Recuperer les noms des sommets
    messagebox.showinfo("Parcours en profondeur", f"Chemin : {' -> '.join(chemin_noms)}")



def afficher_parcours_dfs():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]
    sommets = data['sommets']
    aretes = data['aretes']

    if not sommets:
        messagebox.showinfo("DFS", "Aucun sommet dans le graphe.")
        return

    orientee = any(a[2] for a in aretes)
    sommet_depart = trouver_sommet_depart(sommets, aretes, orientee)
    parcours = dfs(sommets, aretes, sommet_depart, orientee)

    # Afficher le parcours
    noms_parcours = [sommets[i][2] for i in parcours]
    messagebox.showinfo("DFS", f"Parcours DFS : {' -> '.join(noms_parcours)}")


# Fonction pour retirer une arête orientée
def retirer_arrete_orientee():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]

    if not data['aretes']:
        messagebox.showinfo("Retirer arête orientée", "Aucune arête orientée à retirer.")
        return

    for i, (s1, s2, orientee, nom) in enumerate(data['aretes']):
        if orientee:
            del data['aretes'][i]
            messagebox.showinfo("Retirer arête orientée", f"Arête orientée '{nom}' supprimée.")
            return

    messagebox.showinfo("Retirer arête orientée", "Aucune arête orientée trouvée.")

   # Fonction pour retirer une arête non orientée
def retirer_arrete_non_orientee():
    current_tab = notebook.nametowidget(notebook.select())
    data = tab_data[current_tab]

    if not data['aretes']:
        messagebox.showinfo("Retirer arête non orientée", "Aucune arête non orientée à retirer.")
        return

    for i, (s1, s2, orientee, nom) in enumerate(data['aretes']):
        if not orientee:
            del data['aretes'][i]
            messagebox.showinfo("Retirer arête non orientée", f"Arête non orientée '{nom}' supprimée.")
            return

    messagebox.showinfo("Retirer arête non orientée", "Aucune arête non orientée trouvée.")
 
#pour le chemin 
# Initialiser les variables globales
nom_sommet_courant = None
liste_sommets = []
cercles = []
textes_sommets = []
etiquettes_arretes = []
arcs = []
chemin_fichier = None

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


# Créer une barre de menus
menu_bar = Menu(fenetre)

# Créer les sous-menus
menu_fichier = Menu(menu_bar, tearoff=0)  # Sous-menu Fichier
menu_creation = Menu(menu_bar, tearoff=0)  # Sous-menu Création
menu_affichage = Menu(menu_bar, tearoff=0)  # Sous-menu Affichage
menu_exe = Menu(menu_bar, tearoff=0)  # Sous-menu Exécution
menu_edition = Menu(menu_bar, tearoff=0)  # Sous-menu Édition

# Menu Fichier
menu_fichier.add_command(label="Nouveau", command=nouveau,compound=LEFT)
menu_fichier.add_command(label="Ouvrir", compound=LEFT,command=ouvrir_fichier)
menu_fichier.add_command(label="Enregistrer", compound=LEFT,command=enregistrer_fichier)
menu_fichier.add_command(label="Enregistrer sous",command= enregistrer_sous,compound=LEFT)
menu_fichier.add_command(label="Fermer",compound=LEFT,command=fermer_fichier)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter",command=quitter_application,compound=LEFT)
# Menu Création
sous_menu_sommet = Menu(menu_creation, tearoff=0)
sous_menu_sommet.add_command(label="Ajouter Un Sommet",command=creer_sommet,compound=LEFT)
sous_menu_sommet.add_command(label="Retirer Un Sommet", command=retirer_sommet_par_clic,compound=LEFT)
menu_creation.add_cascade(label="Sommet", compound=LEFT, menu=sous_menu_sommet)

# Sous-menu Arête
sous_menu_arret = Menu(menu_creation, tearoff=0)

# Sous-menu pour les arêtes orientées
sous_menu_arret_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_orientee.add_command(label="Ajouter une arête orientée",command=creer_arete_oriente,compound=LEFT)
sous_menu_arret_orientee.add_command(label="Retirer une arête orientée",command=retirer_arrete_orientee,compound=LEFT)

# Sous-menu pour les arêtes non orientées
sous_menu_arret_non_orientee = Menu(sous_menu_arret, tearoff=0)
sous_menu_arret_non_orientee.add_command(label="Ajouter une arête non orientée",command=creer_arete_non_oriente,compound=LEFT)
sous_menu_arret_non_orientee.add_command(label="Retirer une arête non orientée",command=retirer_arrete_non_orientee,compound=LEFT)

# Ajouter les options des arêtes au menu principal
sous_menu_arret.add_cascade(label="Arête Orientée", menu=sous_menu_arret_orientee)
sous_menu_arret.add_cascade(label="Arête Non Orientée", menu=sous_menu_arret_non_orientee)
menu_creation.add_cascade(label="Arête", menu=sous_menu_arret)

# Menu Affichage
menu_affichage.add_command(label="Graphe", compound=LEFT)
sous_menu_chaine = Menu(menu_affichage, tearoff=0)
sous_menu_chaine.add_command(label="Chaine eulerienne",command=afficher_chaine_eulerienne,compound=LEFT)
sous_menu_chaine.add_command(label="Chaine hamiltonienne",command=afficher_chaine_hamiltonienne,compound=LEFT)
sous_menu_chaine.add_command(label="Chemins entre deux sommets",command=chemin_entre_deux_sommets,compound=LEFT)

menu_affichage.add_cascade(label="Chaines", compound=LEFT, menu=sous_menu_chaine)

sous_menu_matrice_ma = Menu(menu_affichage, tearoff=0)
sous_menu_matrice_ma.add_command(label="Matrice adjacents",command=afficher_matrice_adjacente,compound=LEFT)
sous_menu_matrice_ma.add_command(label="Matrice incidence",command=afficher_matrice_incidence,compound=LEFT)
menu_affichage.add_cascade(label="Matrices", compound=LEFT, menu=sous_menu_matrice_ma)

# Menu Exécution 
menu_exe.add_command(label="Parours en profondeur ",command=effectuer_parcours_profondeur)
menu_exe.add_command(label="Plus court chemin")
menu_exe.add_command(label="Coloration")

# Ajouter la barre de menu à la fenêtre principale
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)
menu_bar.add_cascade(label="Création", menu=menu_creation)
menu_bar.add_cascade(label="Affichage", menu=menu_affichage)
menu_bar.add_cascade(label="Exécution", menu=menu_exe)
menu_bar.add_cascade(label="Édition", menu=menu_edition)

# Appliquer la barre de menu à la fenêtre
fenetre.config(menu=menu_bar)

# Demarrer la boucle principale de l'interface
fenetre.mainloop()