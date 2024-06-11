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
   

   # placement des super pacgommes
   super_pacgommes_positions = [(1, 1), (1, HAUTEUR-2), (LARGEUR-2, 1), (LARGEUR-2, HAUTEUR-2)]

   for (x, y) in super_pacgommes_positions:
      GUM[x][y] = 2
   return GUM
            
GUM = PlacementsGUM()   


PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"   ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange" ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"   ,random.choice(Direction)]  )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"    ,random.choice(Direction)]  )         


# variable pour le score, mode de chasse et durée de chasse
score = 0  
mode_chasse = False
chasse_tour = 0


### 3.IA PACMAN

G = 900  # Valeur pour les murs d'une valeur très grande
M = LARGEUR * HAUTEUR  # Valeur des cases du parcours initialisées à une valeur M correspondant à la surface totale labyrinthe 
DISTANCES = np.zeros(TBL.shape, dtype=np.int32) # distances des cases


# initialisation de la carte des distances 
def carte_init():
   global G, M, DISTANCES

   for x in range(LARGEUR):
      for y in range(HAUTEUR):

         if TBL[x][y] == 1 :
            DISTANCES[x][y] = G
         elif GUM[x][y] == 1 or GUM[x][y] == 2:
            DISTANCES[x][y] = 0
         else:
            DISTANCES[x][y] = M

   return DISTANCES

DISTANCES = carte_init()


# recalcule de la carte des distances 

def recalcul_de_la_carte():
   global DISTANCES, Direction, G, M

   Maj = True
   # Continue tant qu'il y a des mises à jour
   while Maj:
      Maj = False
      
      # Parcourt le tableau en évitant les bords, qui sont des murs
      for y in range(1, HAUTEUR - 1):
         for x in range(1, LARGEUR - 1):
               # Si la case n'est pas un mur
               if DISTANCES[x][y] != G:
                  # Calcule les coordonnées des voisins valides
                  voisins = [(x + dx, y + dy) for dx, dy in Direction 
                              if 0 <= x + dx < LARGEUR and 0 <= y + dy < HAUTEUR]

                  # Calcule la valeur minimale parmi les voisins
                  valeur_min = min(DISTANCES[nx][ny] for nx, ny in voisins)

                  # Si la distance actuelle est plus grande que la distance minimale + 1
                  if DISTANCES[x][y] > valeur_min + 1:
                     # Met à jour la distance de la case
                     DISTANCES[x][y] = valeur_min + 1
                     # Indique qu'il y a eu une mise à jour
                     Maj = True

# Initialisation des tableaux pour la position des fantômes et les distances aux fantômes
GHOST = np.zeros(TBL.shape, dtype=np.int32)
DISTANCES_GHOST = np.zeros(TBL.shape, dtype=np.int32)

def carte_init_fantomes():
   global DISTANCES_GHOST, GHOST

   # Réinitialise le tableau des positions des fantômes
   GHOST = np.zeros(TBL.shape, dtype=np.int32)

   # Marque les positions des fantômes dans le tableau GHOST
   for F in Ghosts:
      if TBL[F[0]][F[1]] != 2:  # fantôme pas présent dans la maison
         GHOST[F[0]][F[1]] = 1

   # Initialisation de la carte des distances aux fantômes
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if TBL[x][y] == 1:  # Mur
               DISTANCES_GHOST[x][y] = G
         elif GHOST[x][y] == 1:  # Fantôme
               DISTANCES_GHOST[x][y] = 0
         else:  # Autre
               DISTANCES_GHOST[x][y] = M

   return DISTANCES_GHOST

def recalcule_de_la_carte_des_fantomes():
   global DISTANCES_GHOST, GHOST

   anyUpdate = True

   # Boucle jusqu'à ce qu'il n'y ait plus de mise à jour
   while anyUpdate:
      anyUpdate = False
      # Parcourt le tableau en évitant les bords, qui sont des murs
      for y in range(1, HAUTEUR - 1):
         for x in range(1, LARGEUR - 1):
               # Si la case n'est pas un mur
               if DISTANCES_GHOST[x][y] != G:
                  # Calcule les coordonnées des voisins valides
                  voisins = [(x + dx, y + dy) for dx, dy in Direction 
                              if 0 <= x + dx < LARGEUR and 0 <= y + dy < HAUTEUR]

                  # Calcule la valeur minimale parmi les voisins
                  valeur_min = min(DISTANCES_GHOST[nx][ny] for nx, ny in voisins)

                  # Si la distance actuelle est plus grande que la distance minimale + 1
                  if DISTANCES_GHOST[x][y] > valeur_min + 1:
                     # Met à jour la distance de la case
                     DISTANCES_GHOST[x][y] = valeur_min + 1
                     # Indique qu'il y a eu une mise à jour
                     anyUpdate = True




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


print(DISTANCES)



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
         if ( GUM[x][y] == 2):
            xx = To(x) 
            yy = To(y)
            e = 7
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="green")
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
   global TBL

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
   global PacManPos, Ghosts, score, DISTANCES,DISTANCES_GHOST, mode_chasse, chasse_tour

   # Deplacement Pacman
   possible_moves = PacManPossibleMove()
   
   # Vérifier la distance aux fantômes
   distance_fantome_min = min(DISTANCES_GHOST[PacManPos[0] + move[0], PacManPos[1] + move[1]] for move in possible_moves)

   if distance_fantome_min > 3:
      # Mode recherche de Pac-gommes
      min_distance = float('inf')
      best_move = None

      for move in possible_moves:
         nx, ny = PacManPos[0] + move[0], PacManPos[1] + move[1]
         if DISTANCES[nx][ny] < min_distance:
               min_distance = DISTANCES[nx][ny]
               best_move = move

      if best_move:
         PacManPos[0] += best_move[0]
         PacManPos[1] += best_move[1]
      else:
         # Si aucun mouvement trouvé, choisir un mouvement aléatoire parmi les mouvements possibles
         random_move = random.choice(possible_moves)
         PacManPos[0] += random_move[0]
         PacManPos[1] += random_move[1]

   elif mode_chasse:
      # Mode chasse - Pac-Man doit se diriger vers le fantôme le plus proche
      min_distance_ghost = float('inf')
      best_move = None

      for move in possible_moves:
         nx, ny = PacManPos[0] + move[0], PacManPos[1] + move[1]
         if DISTANCES_GHOST[nx][ny] < min_distance_ghost:
               min_distance_ghost = DISTANCES_GHOST[nx][ny]
               best_move = move

      if best_move:
         PacManPos[0] += best_move[0]
         PacManPos[1] += best_move[1]  
      else:
         # Si aucun mouvement trouvé, choisir un mouvement aléatoire parmi les mouvements possibles
         random_move = random.choice(possible_moves)
         PacManPos[0] += random_move[0]
         PacManPos[1] += random_move[1]
          
   
   else:
      # Mode fuite
      max_distance = -1
      best_move = None

      for move in possible_moves:
         nx, ny = PacManPos[0] + move[0], PacManPos[1] + move[1]
         if DISTANCES_GHOST[nx][ny] > max_distance:
               max_distance = DISTANCES_GHOST[nx][ny]
               best_move = move

      if best_move:
         PacManPos[0] += best_move[0]
         PacManPos[1] += best_move[1]
      else:
         # Si aucun mouvement trouvé, choisir un mouvement aléatoire parmi les mouvements possibles
         random_move = random.choice(possible_moves)
         PacManPos[0] += random_move[0]
         PacManPos[1] += random_move[1]

   # Si Pac-Man se trouve sur une case avec une Pac-gomme, la retire
   # Ajoute +100 pour chaque Pac-gomme mangée
   if GUM[PacManPos[0]][PacManPos[1]] == 1:
      GUM[PacManPos[0]][PacManPos[1]] = 0
      score += 100 
      DISTANCES = carte_init()

   # Si Pac-Man se trouve sur une case avec une super Pac-gomme,la retire
   # Activer le mode chasse

   if GUM[PacManPos[0]][PacManPos[1]] == 2:
      GUM[PacManPos[0]][PacManPos[1]] = 0
      score += 500 
      mode_chasse = True
      chasse_tour = 16
      DISTANCES = carte_init()

   if chasse_tour > 0:
        chasse_tour = chasse_tour - 1
   else:
        mode_chasse = False

   recalcul_de_la_carte()
   # Juste pour montrer comment on se sert de la fonction SetInfo1
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         SetInfo1(x, y, DISTANCES[x][y])
         SetInfo2(x, y, DISTANCES_GHOST[x][y])

   
def IAGhosts():
   global Direction, score

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
      if [F[0], F[1]] == PacManPos and not mode_chasse:
         print("Collision avec un fantôme!")
         global PAUSE_FLAG
         PAUSE_FLAG = True
      elif [F[0], F[1]] == PacManPos and mode_chasse :
         F[0], F[1], F[3] = LARGEUR // 2, HAUTEUR // 2, (0, 1)
         score += 2000
   
   carte_init_fantomes()
   recalcule_de_la_carte_des_fantomes()
      

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration
   
   if not PAUSE_FLAG: 
      iteration += 1
      if iteration % 2 == 0:   
         IAPacman()
      else:                     
         IAGhosts()
   
   pacman_color = "green" if mode_chasse else "yellow"
   Affiche(PacmanColor=pacman_color, message="message") 




###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()