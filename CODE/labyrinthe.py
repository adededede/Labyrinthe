from asyncio.windows_events import NULL


class Case:

    #attributs de la classe
    mur_haut = False
    mur_bas = False
    mur_gauche = False
    mur_droite = False
    #index
    index = 0

    #constructeur
    def __init__(self,haut,bas,gauche,droite,index):
        #est-ce techniquement juste?
        #peut-on simplement ne pas les definir ci-dessus?
        #mais dans ce cas comment etre sur que l'on a bien des booleens?
        self.mur_haut=haut
        self.mur_bas=bas
        self.mur_gauche=gauche
        self.mur_droite=droite
        self.index = index
   

class Labyrinthe:

    #attributs de la classe
    #on pourrait par la suite imaginer des labyrinthe de forme ronde, triangulaire...
    cases = []


    #constructeur
    def __init__(self,largeur,hauteur):
        self.largeur=largeur
        self.hauteur=hauteur
        self.remplissage_aleatoire()
        # techniquement la création des bordures fait
        # aussi les coins du coup pas vraiment utile
        # self.creation_coins()
        self.creation_bordures()


    #methode de la classe
    def remplissage_aleatoire(self):
        index = 0
        for c in range(self.largeur*self.hauteur) :
            self.cases.append(Case(False,False,False,False,index))
            index+=1

    def creation_coins(self):
        #coin en haut à gauche
        self.cases[0].mur_haut = True
        self.cases[0].mur_gauche = True
        #coin en haut à droite
        self.cases[(self.largeur)-1].mur_haut = True
        self.cases[(self.largeur)-1].mur_droite = True
        #coin en bas à gauche
        self.cases[(self.largeur*self.hauteur)-self.largeur].mur_bas = True
        self.cases[(self.largeur*self.hauteur)-self.largeur].mur_gauche = True
        #coin en bas à droite
        self.cases[(self.largeur*self.hauteur)-1].mur_bas =True
        self.cases[(self.largeur*self.hauteur)-1].mur_droite =True

    def creation_bordures(self):
        #parcours de notre liste de cases
        for c in self.cases :
            #toute la bordure haute
            if (c.index >= 0 and c.index <= self.largeur-1):
                c.mur_haut = True                 
            #toute la bordure basse          
            if(c.index >= (self.largeur*self.hauteur)-self.largeur and c.index <= (self.largeur*self.hauteur)-1):
                c.mur_bas = True
            #toute la bordure gauche
            if(c.index % self.largeur == 0) :
                c.mur_gauche = True
            #toute la bordure droite
            if(c.index % self.largeur == (self.largeur-1)) :
                c.mur_droite = True
    
    def affichage(self):
        for c in self.cases : 
            print(f'index : {c.index}')
            if c.index % self.largeur == (self.largeur-1) :
                print(f'{c.mur_haut} {c.mur_bas} {c.mur_gauche} {c.mur_droite} \n')
            else :
                print(f'{c.mur_haut} {c.mur_bas} {c.mur_gauche} {c.mur_droite}, ')

    #permet de verifier la presence de mur autour d'un case voulu, en y indiquant l'index de celle-ci
    def presence_mur(self,index,droit,bas,haut,gauche):
        #si l'index correspond à une case de la premiere ligne
        if (index >= 0 and index <= self.largeur-1):
            #on regarde la case à sa gauche
            if index != 0 :
                gauche = self.cases[index - 1].mur_droite
            #on regarde la case à sa droite
            if index != self.largeur - 1 :
                droit = self.cases[index + 1].mur_gauche
            bas = self.cases[index]
            haut = NULL

        #si l'index correspond à une case de la dernière ligne
        elif(index % self.largeur == (self.largeur-1)) :
            #on regarde la case à sa gauche
            if index != (self.largeur*self.hauteur)-self.largeur :
                gauche = self.cases[index - 1].mur_droite
            #on regarde la case à sa droite
            if index != (self.largeur*self.hauteur)-1 :
                droit = self.cases[index + 1].mur_gauche
            bas = NULL
            haut = self.cases[index]

        #si l'index correspond à une case de la colonne toute à gauche          
        elif(index >= (self.largeur*self.hauteur)-self.largeur and index <= (self.largeur*self.hauteur)-1):
            gauche = NULL
            #on regarde la case au dessus
            haut = self.cases[index]
            #on regarde la case au dessous
            bas = self.cases[index]
            #on regarde la case à sa droite
            droit = self.cases[index + 1].mur_gauche                
            
        #si l'index correspond à une case de la colonne toute à droite
        elif(index % self.largeur == 0) :
            droit = NULL
            #on regarde la case au dessus
            haut = self.cases[index]
            #on regarde la case au dessous
            bas = self.cases[index]
            #on regarde la case à sa gauche
            gauche = self.cases[index - 1].mur_droite              
                        
                   

#test du code
labyrinthe_test = Labyrinthe(4,3)
labyrinthe_test.affichage()
            
            
                





