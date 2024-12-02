from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import json
import csv
import os

oldx=0
oldy=0
iter=0
l=[]

class  application():

   def __init__(self,window):
      self.window=window
      self.savefile={1:""}
      self.file=None
      self.list_top=[]

   def personalise(self):
       self.window.geometry("400x400")
       self.window.title("Interface")

   def nouveau(self):
      self.fram = Toplevel(self.window)
      self.list_top.append(self.fram)
      self.fram.protocol("WM_DELETE_WINDOW",self.fermer)
      self.fram.transient(self.window)
      self.fram.focus_set()
      """self.fram.iconbitmap("ga2.ico")"""
      self.fram.geometry("550x300")
      self.fram.title("Untitled.py")
      self.canvas= Canvas(self.fram, background="white")
      self.canvas.pack(side=TOP, fill=BOTH, expand=1)
      self.indice_sommet=0
      self.indice_arete=0
      self.list_sommet=[]
      self.list_arete=[]

   def get_sommet(self):
      l=[]
      A = self.list_sommet
      for i in A:
         l.append(int(i[0]))
      return l

   def get_arete(self):
      l=[]
      B = self.list_arete
      j=0
      for i in B:
         j+=1
         l.append(int(j))
      return l

   def voisin(self):
      B = self.list_arete
      voisin = []
      for i in B:
         l =[i[1][0], i[2][0]]
         voisin.append(l)
      return voisin

   def creer_matrice_ad(self):
      A = self.list_sommet
      C = self.voisin()
      matrice={}
      for i in A:
         adjacence= []
         for j in A:
            l1=[i[0], j[0]]
            l2=[j[0], i[0]]
            if (l1 in C) or (l2 in C):
               adja=1
            else:
               adja=0
            adjacence.append(adja)
         matrice[int(i[0])]= tuple(adjacence)
      return matrice

   def matrice_ad(self):
      popup = Toplevel(self.fram)
      popup.title("Matrice d'adjacence")
      """popup.iconbitmap("ga2.ico")"""
      popup.transient(self.fram)
      matrice = self.creer_matrice_ad()
      list_sommet = self.get_sommet()
      for i in range(len(list_sommet)):
         list_sommet[i] = str(list_sommet[i])
      mat= ttk.Treeview(master=popup)
      mat['columns'] = tuple(list_sommet)
      mat.column("#0",width=30,minwidth=20)
      for i in list_sommet:
         mat.column(i,width=30,minwidth=20)
      mat.heading("#0",text="  ")
      for i in list_sommet:
         mat.heading(i,text=str(i))
      list_sommet = self.get_sommet()
      for i in list_sommet:
         mat.insert(parent="",index="end",iid = i,text=str(i)+" ",values=matrice[i])
      mat.pack()


   def creer_matrice_in(self):
      A = self.list_sommet
      B = self.list_arete
      matrice={}
      for i in A:
         incidence= []
         for j in B:
            if i[0]==j[1][0] or i[0]==j[2][0]:
               if i[1]==j[1][1] and i[2]==j[2][2]:
                  incid=2
               else:

                  incid=1
            else:
               incid=0
            incidence.append(incid)
         matrice[int(i[0])]= tuple(incidence)
      return matrice

   def matrice_in(self):
      popup = Toplevel(self.fram)
      popup.title("Matrice d'incidence")
      """popup.iconbitmap("ga2.ico")"""
      popup.transient(self.fram)
      matrice = self.creer_matrice_in()
      list_arete = self.get_arete()
      list_sommet = self.get_sommet()
      for i in range(len(list_sommet)):
         list_sommet[i] = str(list_sommet[i])

      mat= ttk.Treeview(master=popup)
      mat['columns'] = tuple(list_arete)
      mat.column("#0",width=30,minwidth=20)
      for i in list_sommet:
         mat.column(i,width=30,minwidth=20)
      mat.heading("#0",text="  ")
      for i in list_arete:
         mat.heading(i,text="e"+str(i))
      list_sommet = self.get_sommet()
      for i in list_sommet:
         mat.insert(parent="",index="end",iid = i,text=str(i)+" ",values=matrice[i])
      mat.pack()


   def vide(event):
      pass

   def ouvrir(self):
      self.file = filedialog.askopenfilename( title="Ouvrir un fichier",
                                           filetypes=[("Python files","*.py")])
      if self.file!="":
         self.savefile[1] = self.file
         self.fram = Toplevel(self.window)
         self.fram.protocol("WM_DELETE_WINDOW",self.fermer)
         self.fram.title(os.path.basename(self.file))
         self.list_top.append(self.fram)
         self.fram.transient(self.window)
         self.fram.focus_set()
         """self.fram.iconbitmap("ga2.ico")"""
         self.fram.geometry("550x300")
         self.canvas= Canvas(self.fram, background="white")
         self.canvas.pack(side=TOP, fill=BOTH, expand=1)
         self.indice_sommet=0
         self.indice_arete=0
         self.list_sommet=[]
         self.list_arete=[]


         dic = {}
         with open(self.file, 'r') as f:
            dic = json.load(f)

         self.list_sommet = dic['ls']
         self.list_arete = dic['la']


         for j in self.list_arete:
            if j[1][1]==j[2][1] and j[1][2]==j[2][2]:
               self.canvas.create_oval(j[1][1], j[1][2],j[1][1]-30, j[1][2]-30)
               center_x, center_y = (j[1][1]-30, j[1][2]-30)
            else:
               self.canvas.create_line(j[1][1],j[1][2], j[2][1], j[2][2])
               center_x, center_y = ((j[1][1]) + (j[2][1])) / 2, ((j[1][2] + 15) + (j[2][2] + 15)) / 2
            self.indice_arete+=1
            self.canvas.create_text(center_x, center_y, text=j[0])

         for i in self.list_sommet:
            self.canvas.create_oval(i[1]-10, i[2]-10, i[1]+10, i[2]+10, fill="white")
            self.indice_sommet+=1
            self.canvas.create_text(i[1],i[2], text=i[0], fill="black")


   def enregistrer(self):
      dic = {}
      dic['ls']=self.list_sommet
      dic['la']=self.list_arete
      if self.file==None:
         self.enregistrer_sous()
      else:
         with open(self.file, 'w+') as f:
               json.dump(dic, f)

   def enregistrer_sous(self):

      self.file = filedialog.asksaveasfilename(initialfile='Untitled.py',
                                            filetypes=[("Python files","*.py")])
      if self.file!="":
         self.fram.title(os.path.basename(self.file))
         dic = {}
         dic['ls']=self.list_sommet
         dic['la']=self.list_arete

         with open(self.file, 'w+') as f:
            json.dump(dic, f)

   def fermer(self):
      if len(self.list_top)==0 :
         self.window.quit()
      else:
            n=len(self.list_top)
            self.list_top[n-1].destroy()
            self.list_top.remove(self.list_top[n-1])

   def ajoute_point(self,event):
      self.canvas.focus_set()
      x = event.x
      y = event.y
      vide=True
      for i in range(len(self.list_sommet)):
         sx=self.list_sommet[i][1]
         sy=self.list_sommet[i][2]
         if (x > sx-15) and (x < sx+15) and (y > sy-15)  and (y < sy+15):
            vide=False

      if vide:
         self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='white')
         self.indice_sommet+=1
         self.canvas.create_text(x,y, text=str(self.indice_sommet), fill='black')
         l=[str(self.indice_sommet),x,y,0]
         self.list_sommet.append(l)

   def sommet(self):
      self.canvas.bind("<Button-1>", self.ajoute_point)

   def tracer(self, event):
      global iter, l
      global oldx,oldy
      if iter==0:
         oldx,oldy = event.x,event.y
         for i in range(len(self.list_sommet)):
            osx=self.list_sommet[i][1]
            osy=self.list_sommet[i][2]
            if (oldx > osx-10) and (oldx < osx+10) and (oldy > osy-10) and (oldy < osy+10):
               oldx, oldy=self.list_sommet[i][1], self.list_sommet[i][2]
               l=self.list_sommet[i]
               iter+=1
      else:
         x,y = event.x,event.y
         for i in range(len(self.list_sommet)):
            sx=self.list_sommet[i][1]
            sy=self.list_sommet[i][2]
            if (x > sx-10) and (x < sx+10) and (y > sy-10) and (y < sy+10):
               x,y=self.list_sommet[i][1], self.list_sommet[i][2]
               if x==oldx and y==oldy:
                  self.canvas.create_oval(x, y, x-30, y-30)
                  center_x, center_y = (x-30, y-30)
               else:
                  self.canvas.create_line(oldx, oldy, x, y)
                  self.canvas.create_oval(oldx-10, oldy-10, oldx+10, oldy+10, fill='white')
                  self.canvas.create_text(oldx, oldy, text=l[0], fill='black')
                  self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='white')
                  self.canvas.create_text(x,y, text=self.list_sommet[i][0], fill='black')
                  center_x, center_y = ((oldx) + (x)) / 2, ((oldy + 15) + (y + 15)) / 2

               self.indice_arete+=1
               self.canvas.create_text(center_x, center_y, text="e"+str(self.indice_arete))
               list=["e"+str(self.indice_arete),l, self.list_sommet[i] ]
               self.list_arete.append(list)
               iter=0
               oldx=0
               oldy=0
               l=[]

   def arete(self):
      self.canvas.bind("<Button-1>", self.tracer)

   """def degree(self):
      voisin=self.voisin()
      for i in range(len(self.list_sommet)):
         degre=0
         for j in voisin:
            if self.list_sommet[i][0] in j:
               degre+=1
         self.list_sommet[i][3]=degre
      max_degre= self.list_sommet[0][3]
      for i in range(len(self.list_sommet)):
         if max_degre < self.list_sommet[i][3]:
            max_degre = self.list_sommet[i][3]
            sommet=self.list_sommet[i][0]
      print("sommet ",sommet,"=",max_degre)"""

   def coloration(self):
      dic_voisin={}
      B = self.list_arete
      voisin = []
      for i in B:
         l =[i[1], i[2]]
         voisin.append(l)

      for i in range(len(self.list_sommet)):
         l=[]
         for j in voisin:
            if self.list_sommet[i][0]==j[0][0]:
               l.append(j[1][0])
            elif self.list_sommet[i][0]==j[1][0]:
               l.append(j[0][0])
         dic_voisin[self.list_sommet[i][0]]=l

      self.dic_color={1:'blue',2:'red',3:'green',4:'yellow',5:'purple'}
      for i in range(len(self.list_sommet)):
         lst=dic_voisin[self.list_sommet[i][0]]
         ls=[]
         for j in lst:
            for e in self.list_sommet:
               if e[0]==j:
                  ls.append(e[3])
         k=1
         while k in ls:
            k+=1
         self.list_sommet[i][3]=k

      self.color = Toplevel(self.window)
      self.color.transient(self.fram)
      """self.color.iconbitmap("ga2.ico")"""
      self.color.geometry("550x300")
      self.color_can= Canvas(self.color, background="white")
      self.color_can.pack(side=TOP, fill=BOTH, expand=1)


      for j in self.list_arete:
         if j[1][1]==j[2][1] and j[1][2]==j[2][2]:
            self.color_can.create_oval(j[1][1], j[1][2],j[1][1]-30, j[1][2]-30)
            center_x, center_y = (j[1][1]-30, j[1][2]-30)
         else:
            self.color_can.create_line(j[1][1],j[1][2], j[2][1], j[2][2])
            center_x, center_y = ((j[1][1]) + (j[2][1])) / 2, ((j[1][2] + 15) + (j[2][2] + 15)) / 2
         self.color_can.create_text(center_x, center_y, text=j[0])

      for i in self.list_sommet:
            self.color_can.create_oval(i[1]-10, i[2]-10, i[1]+10, i[2]+10, fill=self.dic_color[i[3]])
            self.color_can.create_text(i[1],i[2], text=i[0], fill="white")


   def add_menu(self):
      menu = Menu(self.window)
      fichier = Menu (menu, tearoff=0)
      fichier.add_command(label="Nouveau", command=self.nouveau)
      fichier.add_command(label="Ouvrir...", command=self.ouvrir)
      fichier.add_command(label="Enregistrer", command=self.enregistrer)
      fichier.add_command(label="Enregistrer sous...", command=self.enregistrer_sous)
      fichier.add_separator()                                        #ligne de separation
      fichier.add_command(label="Fermer", command=self.fermer)
      creation = Menu (menu, tearoff=0)
      creation.add_command(label="Sommet", command=self.sommet)
      creation.add_command(label="Arete",command=self.arete)
      affichage = Menu (menu, tearoff=0)
      affichage.add_command(label="Graphe", command=self.vide)
      affichage.add_command(label="Chaines", command=self.vide)

      matrice = Menu(affichage, tearoff=0)
      matrice.add_command(label="Matrice d'incidence", command=self.matrice_in)
      matrice.add_command(label="Matrice d'adjacence", command=self.matrice_ad)

      affichage.add_cascade(label="Matrice", menu=matrice)
      execution = Menu (menu, tearoff=0)
      execution.add_command(label="Plus court chemin", command=self.vide)

      coloration = Menu(execution, tearoff=0)
      coloration.add_command(label="Algorithme de glouton", command=self.coloration)
      execution.add_cascade(label="Coloration", menu=coloration)
      edition = Menu(menu, tearoff=0)
      edition.add_command(label="Graphe")

      menu.add_cascade(label="Fichier", menu=fichier)
      menu.add_cascade(label="Création", menu=creation)
      menu.add_cascade(label="Affichage", menu=affichage)
      menu.add_cascade(label="Exécution", menu=execution)
      menu.add_cascade(label="Edition", menu=edition)
      self.window.config(menu = menu)

   def affiche(self):
      self.window.mainloop()
if __name__ == '__main__':
       window = Tk()
inter= application(window)
iter=0
inter.personalise()
inter.add_menu()
inter.affiche()