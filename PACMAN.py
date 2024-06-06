import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

# labyrinthe de jeu
TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# Liste des déplacements possibles [(0,-1), (0,1), (1,0), (-1,0)]
Direction = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   


PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"   ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange" ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"   ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"    ,random.choice(Direction)]  )         


# variable pour le score
score = 0  


### 3.IA PACMAN

G = 900  # Valeur pour les murs d'une valeur très grande
M = LARGEUR * HAUTEUR  # Valeur des cases du parcours initialisées à une valeur M correspondant à la surface totale labyrinthe 
Distances = np.zeros(TBL.shape, dtype=np.int32) # distances des cases


# initialisation de la carte des distances 
def carte_init():
   #global G, M, Distances

   for x in range(LARGEUR):
      for y in range(HAUTEUR):

         if TBL[x][y] == 1:
            Distances[x][y] = G
         elif GUM[x][y] == 1:
            Distances[x][y] = 0
         else:
            Distances[x][y] = M

   return Distances

Distances = carte_init()


# recalcule de la carte des distances 


def recalcul_de_la_carte():
   # global Distances, Direction, G, M

   Maj = True
   # Continue tant qu'il y a des mises à jour
   while Maj:
      Maj = False
      
      # Parcourt le tableau en évitant les bords, qui sont des murs
      for y in range(1, HAUTEUR - 1):
         for x in range(1, LARGEUR - 1):
               # Si la case n'est pas un mur
               if Distances[x][y] != G:
                  # Calcule les coordonnées des voisins valides
                  voisins = [(x + dx, y + dy) for dx, dy in Direction 
                              if 0 <= x + dx < LARGEUR and 0 <= y + dy < HAUTEUR]

                  # Calcule la valeur minimale parmi les voisins
                  valeur_min = min(Distances[nx][ny] for nx, ny in voisins)

                  # Si la distance actuelle est plus grande que la distance minimale + 1
                  if Distances[x][y] > valeur_min + 1:
                     # Met à jour la distance de la case
                     Distances[x][y] = valeur_min + 1
                     # Indique qu'il y a eu une mise à jour
                     Maj = True



##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info


print(Distances)



##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche, score
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)

   # Affichage du score
   canvas.create_text(screeenWidth // 7, screenHeight- 40, text=f"Score: {score}", fill="white", font=PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove():
   global Direction 
   moves = []
   
   # Calculer les positions adjacentes en fonction de la position actuelle et des déplacements possibles
   for dx, dy in Direction:
      nx = PacManPos[0] + dx
      ny = PacManPos[1] + dy
      if TBL[nx][ny] == 0:  # Verifier si le mouvement est possible (pas un mur)
         moves.append((dx, dy))

   return moves

   
def GhostsPossibleMove(x, y, directionActuelle):
   #global TBL

   # Calculer les coordonnées de la prochaine case dans la direction actuelle pour un couloir
   nx = x + directionActuelle[0]
   ny = y + directionActuelle[1]

   # Liste des directions disponibles
   directionsDisponible = []

   # Si la case suivante est un mur, ajouter la direction opposée à la liste des directions disponibles
   if TBL[nx][ny] == 1:
      directionsDisponible.append((-directionActuelle[0], -directionActuelle[1]))

   # Si le fantôme se déplace verticalement
   if directionActuelle[0] == 0:
      if TBL[x + 1][y] != 1:
         directionsDisponible.append((1, 0))
      if TBL[x - 1][y] != 1:
         directionsDisponible.append((-1, 0))
   # Si le fantôme se déplace horizontalement
   elif directionActuelle[1] == 0:
      if TBL[x][y + 1] != 1:
         directionsDisponible.append((0, 1))
      if TBL[x][y - 1] != 1:
         directionsDisponible.append((0, -1))

   # Si au moins une direction est disponible, en choisir une au hasard 
   # Sinon continuer dans la direction actuelle
   if directionsDisponible:
      return random.choice(directionsDisponible)
   else:
      return directionActuelle


   
def IAPacman():
   global PacManPos, Ghosts, score, Distances

   # Deplacement Pacman
   possible_moves = PacManPossibleMove()
   
   # Selectionne le mouvement avec la distance minimale
   min_distance = float('inf')
   best_move = None

   for move in possible_moves:
      nx, ny = PacManPos[0] + move[0], PacManPos[1] + move[1]
      if Distances[nx][ny] < min_distance:
         min_distance = Distances[nx][ny]
         best_move = move

   if best_move:
      PacManPos[0] += best_move[0]
      PacManPos[1] += best_move[1]

   # Si Pac-Man se trouve sur une case avec une Pac-gomme, la retire
   # Ajoute +100 pour chaque Pac-gomme mangée
   if GUM[PacManPos[0]][PacManPos[1]] == 1:
      GUM[PacManPos[0]][PacManPos[1]] = 0
      score += 100 
      Distances = carte_init()
      recalcul_de_la_carte()

   # Juste pour montrer comment on se sert de la fonction SetInfo1
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         SetInfo1(x, y, Distances[x][y])

   
def IAGhosts():
   #global Direction

   for F in Ghosts:
      # Calculer le prochain mouvement possible pour le fantôme actuel
      move = GhostsPossibleMove(F[0], F[1], F[3])
      
      # Mettre à jour la position du fantôme avec le mouvement calculé
      F[0] += move[0]
      F[1] += move[1]
      
      # Mettre à jour la direction actuelle du fantôme avec le nouveau mouvement
      F[3] = move

   # Vérification de la collision avec les fantômes
   for F in Ghosts:
      if [F[0], F[1]] == PacManPos:
         print("Collision avec un fantôme!")
         global PAUSE_FLAG
         PAUSE_FLAG = True
      

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration
   
   if not PAUSE_FLAG : 
      iteration += 1
      if iteration % 2 == 0 :   
         IAPacman()
      else:                     
         IAGhosts()
   
   Affiche(PacmanColor = "yellow", message = "message")  




###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()