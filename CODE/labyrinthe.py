from asyncio.windows_events import NULL
import random

class Case:

    #attributs de la classe
    mur_haut = False
    mur_bas = False
    mur_gauche = False
    mur_droite = False
    #index de la case
    index = 0
    #index de la modélisation
    index_modelisation = 0

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
        self.index_modelisation = self.index
   

class Labyrinthe:

    #attributs de la classe
    #on pourrait par la suite imaginer des labyrinthe de forme ronde, triangulaire...
    #ainsi que des labyrinthe impossible (insolvable) ainsi que des labyrinthe imparfaits
    cases = []


    #constructeur
    def __init__(self,largeur,hauteur):
        self.largeur=largeur
        self.hauteur=hauteur
        index = 0
        for c in range(self.largeur*self.hauteur) :
            #idée de basee remplir juste le contour
            #causee des problèmes lors de la modélisation des chemins dans le labyrinthe
            #self.cases.append(Case(False,False,False,False,index))
            self.cases.append(Case(True,True,True,True,index))
            index+=1
        # techniquement la création des bordures fait
        # aussi les coins du coup pas vraiment utile
        # self.creation_coins()

        # Du coup les bordures sont faites lorsque l'on rempli & crée la grille du labyrinthe
        # self.creation_bordures()

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

    #créer les contours du labybrinthe
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
    
    #permet d'afficher de manière brut le labyrinthe
    def affichage(self):
        for c in self.cases : 
            print(f'index : {c.index}\tmodelisation : {c.index_modelisation}')
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

        #si l'index correspond à une case de la colonne toute à droite  
        elif(index % self.largeur == (self.largeur-1)) :
            #on regarde la case à sa gauche
            if index != (self.largeur*self.hauteur)-self.largeur :
                gauche = self.cases[index - 1].mur_droite
            #on regarde la case à sa droite
            if index != (self.largeur*self.hauteur)-1 :
                droit = self.cases[index + 1].mur_gauche
            bas = NULL
            haut = self.cases[index]

        #si l'index correspond à une case de la dernière ligne          
        elif(index >= (self.largeur*self.hauteur)-self.largeur and index <= (self.largeur*self.hauteur)-1):
            gauche = NULL
            #on regarde la case au dessus
            haut = self.cases[index]
            #on regarde la case au dessous
            bas = self.cases[index]
            #on regarde la case à sa droite
            droit = self.cases[index + 1].mur_gauche                
            
        #si l'index correspond à une case de la colonne toute à gauche
        elif(index % self.largeur == 0) :
            droit = NULL
            #on regarde la case au dessus
            haut = self.cases[index]
            #on regarde la case au dessous
            bas = self.cases[index]
            #on regarde la case à sa gauche
            gauche = self.cases[index - 1].mur_droite              
                        
    #modélise l'interieur du labyrinthe de manière aléatoire
    def remplissage(self):
        iteration = 0
        while (iteration < self.largeur*self.hauteur):
            case_aleatoire = random.randint(0, (self.largeur*self.hauteur)-1)
            mur_aleatoire = random.randint(0,3)
            #mur haut
            if mur_aleatoire == 0:
                #SI la case n'est pas sur la ligne une
                if self.cases[case_aleatoire].index > self.largeur-1 :
                    #si la case au dessus de celle tiré n'a pas le même index de modélisation
                    if self.cases[case_aleatoire].index_modelisation != self.cases[case_aleatoire-self.largeur].index_modelisation :
                        #on enleve le mur en haut
                        #de la case pioché
                        self.cases[case_aleatoire].mur_haut = False
                        #et de la case au dessus
                        self.cases[case_aleatoire-self.largeur].mur_bas = False
                        #on donne le même index de modelisation aux deux cases
                        self.cases[case_aleatoire-self.largeur].index_modelisation = self.cases[case_aleatoire].index_modelisation
                        #ainsi qu'a toutes les cases qu'elles a deja "infecté" 
                        for c in self.cases:
                            if c.index_modelisation == self.cases[case_aleatoire-self.largeur].index :
                                c.index_modelisation = self.cases[case_aleatoire-self.largeur].index_modelisation
                        iteration += 1

            #mur bas
            elif mur_aleatoire == 1:
                #SI la case n'est pas sur la dernière ligne
                if self.cases[case_aleatoire].index < (self.largeur*self.hauteur)-self.largeur :
                    #si la case au dessous de celle tiré n'a pas le même index de modélisation
                    if self.cases[case_aleatoire].index_modelisation != self.cases[case_aleatoire+self.largeur].index_modelisation :
                        #on enleve le mur en bas
                        #de la case pioché
                        self.cases[case_aleatoire].mur_bas = False
                        #et de la case au dessous
                        self.cases[case_aleatoire+self.largeur].mur_haut = False
                        #on donne le même index de modelisation aux deux cases
                        self.cases[case_aleatoire+self.largeur].index_modelisation = self.cases[case_aleatoire].index_modelisation
                        #ainsi qu'a toutes les cases qu'elles a deja "infecté" 
                        for c in self.cases:
                            if c.index_modelisation == self.cases[case_aleatoire+self.largeur].index :
                                c.index_modelisation = self.cases[case_aleatoire+self.largeur].index_modelisation
                        iteration += 1

            #mur droit
            elif mur_aleatoire == 2:
                #SI la case n'est pas sur la ligne la plus à droite
                if self.cases[case_aleatoire].index % self.largeur != (self.largeur-1):
                    #si la case à droite de celle tiré n'a pas le même index de modélisation
                    if self.cases[case_aleatoire].index_modelisation != self.cases[case_aleatoire+1].index_modelisation :
                        #on enlève le mur à droite
                        #de la case pioché
                        self.cases[case_aleatoire].mur_droite = False
                        #et de la case à sa droite
                        self.cases[case_aleatoire+1].mur_gauche = False
                        #on donne le même index de modelisation aux deux cases
                        self.cases[case_aleatoire+1].index_modelisation = self.cases[case_aleatoire].index_modelisation
                        #ainsi qu'a toutes les cases qu'elles a deja "infecté" 
                        for c in self.cases:
                            if c.index_modelisation == self.cases[case_aleatoire+1].index :
                                c.index_modelisation = self.cases[case_aleatoire+1].index_modelisation
                        iteration += 1

            #mur gauche
            elif mur_aleatoire == 3:
                #SI la case n'est pas sur la ligne la plus à gauche
                if self.cases[case_aleatoire].index % self.largeur != 0:
                    #si la case à gauche de celle tiré n'a pas le même index de modélisation
                    if self.cases[case_aleatoire].index_modelisation != self.cases[case_aleatoire-1].index_modelisation :
                        #on enlève le mur à gauche
                        #de la case pioché
                        self.cases[case_aleatoire].mur_gauche = False
                        #et de la case à sa gauche
                        self.cases[case_aleatoire-1].mur_droite = False
                        #on donne le même index de modelisation aux deux cases
                        self.cases[case_aleatoire-1].index_modelisation = self.cases[case_aleatoire].index_modelisation
                        #ainsi qu'a toutes les cases qu'elles a deja "infecté" 
                        for c in self.cases:
                            if c.index_modelisation == self.cases[case_aleatoire-1].index :
                                c.index_modelisation = self.cases[case_aleatoire-1].index_modelisation
                        iteration += 1
        
    #creation des portes d'entrée et de sortie du labyrinthe
    def creation_portes(self):
        index_porte1 = -1
        index_porte2 = -1
        while not ((index_porte1>=0 and index_porte1< self.largeur) or (index_porte1>= self.largeur*(self.hauteur-1) and index_porte1<self.largeur*self.hauteur) or (index_porte1%self.largeur==0) or (index_porte1%self.largeur==self.largeur-1)) :
            index_porte1 = random.randint(0,(self.largeur*self.hauteur)-1)
            
        index_porte2 = index_porte1
        while index_porte1 == index_porte2 :
            while not ((index_porte2>=0 and index_porte2< self.largeur) or (index_porte2>= self.largeur*(self.hauteur-1) and index_porte2<self.largeur*self.hauteur) or (index_porte2%self.largeur==0) or (index_porte2%self.largeur==self.largeur-1)) :
                index_porte2 = random.randint(0,(self.largeur*self.hauteur)-1)
        
        #switch self.cases[index_porte1].etat :
        #    case COIN_0_0 :
        #    case COIN_0_D :
        #    case COIN_G_0 :
        #    case COIN_D_D :
        #    case L_0 :
        #    case L_G :
        #    case L_D :
        #    case L_Fin :

    
                   

#test du code
labyrinthe_test = Labyrinthe(4,3)
labyrinthe_test.affichage()
labyrinthe_test.remplissage()
labyrinthe_test.affichage()
            
            
                





