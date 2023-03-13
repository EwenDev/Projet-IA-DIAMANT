##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random


class IA_Diamant():

  def __init__(self, match: str):
    """génère l'objet de la classe IA_Diamant

      Args:
          match (str): decriptif de la partie
      """
    self.historique = [] #historique des cartes tirées
    self.nbjoueurs_plateau = 0 #nombre de joueurs encore en jeu
    self.nbjoueurs_restant = 0 #nombre de joueurs restant
    self.tour = 0 #tour actuel
    self.tresor_sol = 0 #nombre de diamants sur le plateau
    self.tresor_partage = 0 #nombre de diamants partagés
    self.liste_pieges = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0} #nombre de pièges de chaque type
    self.pieges_sortie = {'P1': 3, 'P2': 3, 'P3': 3, 'P4': 3, 'P5': 3} #nombre de pièges de chaque type qui peuvent encore sortir
    self.valeurs_reliques = [5, 5, 5, 10, 10] #valeurs des reliques
    self.nbreliquesdecouvertes = 0 #nombre de reliques découvertes
    self.valreliquesol = 0 #valeur des reliques sur le plateau
    self.joueurs = [] #liste des joueurs
    self.facteurdesortie = 0  #Pourcentage de chances de sortir
    self.donnees_manche = None #Données de la manche
    self.nbsorties = 0 #nombre de sorties
    self.relique_en_jeu = 1 #relique en jeu
    self.carte_dans_le_deck = 31 #nombre de cartes dans la pioche (31 au début de la partie)
    self.classement_diamants = [] #classement des joueurs en fonction du nombre de diamants
    self.ecart = [0,0] #la premiere valeur donne les diamants d'avance et la deuxieme les diamants de retard
    self.indice_ia = 0 #indice de l'ia
  

    for i in range(len(match)): #Repère le caractère "|" et récupère le nombre de joueurs situé après le premier "|"
      if match[i] == '|':
        self.nbjoueurs = int(match[i + 1])
        self.nbjoueurs_plateau = self.nbjoueurs
        break

    self.id_mon_ia = int(match[-1]) #Prend l'id de l'IA à partir du dernier caractère de la chaîne

    for i in range(self.nbjoueurs): #Crée la liste des objets joueurs en mettant en paramètre True si le joueur concerné est l'IA
      if i == self.id_mon_ia:
        self.joueurs.append(Joueur(True))
      else:
        self.joueurs.append(Joueur(False))

  def risque_piege(self):
    """
    Fonction permettant de calculer le risque de tomber sur un piège lors du prochain tour.

    Args : /

    Returns : /
    """
    piege_probable = 0
    for k in self.pieges_sortie.keys(): #Parcourt le dictionnaire pour vérifier la présence de pièges probables dans la liste des pièges
      piege_probable += (self.pieges_sortie[k] - 1) * self.liste_pieges[k]
    
    self.facteurdesortie = (piege_probable / self.carte_dans_le_deck) * 100 #Calcul du risque de tomber sur un piège
  
  
  def ecart_diamants(self):
    """
    Calcule l'écart de l'IA dans le classement par rapport à ses adversaires et met à jour la liste ecart composée de deux valeurs :
    - la première valeur donne l'écart entre l'IA et celui qui est derrière elle dans le classement
    - la première valeur donne l'écart entre l'IA et celui qui est devant elle dans le classement

    Args : /

    Returns : /
    """
    if self.indice_ia == 0:
      self.ecart[0] = 0 #s'il n'y a personne apres il n'y a pas de diamants d'avance
      self.ecart[1] = self.classement_diamants[self.indice_ia][0] - self.classement_diamants[self.indice_ia+1][0]
    elif self.indice_ia == 3:
      self.ecart[0] = self.classement_diamants[self.indice_ia][0] - self.classement_diamants[self.indice_ia-1][0]
      self.ecart[1] = 0 #s'il n'y a personne avant il n'y a pas de diamants de retard
    else:
      self.ecart[0] = self.classement_diamants[self.indice_ia][0] - self.classement_diamants[self.indice_ia-1][0]
      self.ecart[1] = self.classement_diamants[self.indice_ia][0] - self.classement_diamants[self.indice_ia+1][0]
      
  def set_coeffs(self):
    """
    Exécute la fonction ecart_diamants() et crée une variable plus qui va calculer un facteur de modification du facteur de sortie pour l'ajouter à celui-ci

    Args : /

    Returns : /
    """
    self.ecart_diamants()
    plus = self.indice_ia*10 + self.ecart[1] + (self.tresor_sol/self.nbjoueurs_plateau) - self.ecart[0] 
    self.facteurdesortie += plus
    

  def doit_continuer(self):
    """
    Exécute les fonctions risque_piege() et set_coeffs() puis génère un nombre qui, si est inférieur au facteur de sortie, retourne True

    Args: /

    Returns : 
      False (bool) : Si jamais l'IA n'a pas de diamants, ou que le tour actuel est le premier.
      True (bool) : Si jamais le facteur de sortie est inférieur au nombre généré aléatoirement.
    """
    self.risque_piege()
    self.set_coeffs()
    r = random.randint(0,100)
    if self.joueurs[self.id_mon_ia].diamant_poche == 0 or self.tour == 0:
      return False
    return r <= self.facteurdesortie
    
  def comptabilise_carte(self, carte):
    """
      Va contabiliser la carte tirée pour savoir si celle-ci est un trésor, un piège, ou une relique, et va agir en conséquence.

      Args:
        carte (str): Carte tirée (dernier(s) caractère(s) de tour après le symbole '|')

      Returns:
        //
      """
    self.historique.append(carte)
    if carte[0] == 'P': #Si la carte est un piège
      self.liste_pieges[carte] += 1 #On ajoute 1 au nombre de pièges de ce type

      if self.liste_pieges[carte] == 2: #Si le nombre de pièges de ce type est égal à 2
        self.pieges_sortie[carte] -= 1 #On enlève 1 au nombre de pièges de ce type qui seront dans la pioche à la prochaine manche

        
    elif carte == 'R': #Si la carte est une relique
      self.nbreliquesdecouvertes += 1 #On ajoute 1 au nombre de reliques découvertes
      self.valreliquesol += self.valeurs_reliques[self.nbreliquesdecouvertes-1] #On ajoute la valeur de la relique à la valeur totale des reliques découvertes
      self.relique_en_jeu -= 1 #On enlève 1 au nombre de reliques en jeu (elle ne sera plus dans la pioche à la prochaine manche)

    elif carte == 'N': #Si la carte est "Néant", on ne fait rien
      return
    
    else: #Si la carte est un trésor
      self.tresor_partage = int(carte) // self.nbjoueurs_plateau #On calcule le nombre de diamants que chaque joueur va recevoir
      self.tresor_sol += int(carte) % self.nbjoueurs_plateau  #On calcule le nombre de diamants qui restent sur le sol
      self.partage_diamants() #On partage les diamants aux joueurs
      
    
  def action(self, tour: str) -> str:
    """Appelé à chaque décision du joueur IA

      Args:
          tour (str): descriptif du dernier tour de jeu

      Returns:
          str: 'X' ou 'R'
      """
    self.donnees_manche = tour #On stocke les données du tour dans une variable
    self.tour += 1 #On incrémente le tour actuel
    self.carte_dans_le_deck -=1 #On enlève 1 au nombre de cartes dans le deck (utile pour le calcul de la probabilité de tirer un piège)
    for i in range(len(self.donnees_manche)):  #On parcourt les données du tour
      if self.donnees_manche[i] == '|': #On cherche le symbole '|' qui sépare les données du tour
        
        self.choix_joueurs = self.donnees_manche[:i].split(',') #On sépare les choix des joueurs
        self.lecture_choix_joueurs(self.choix_joueurs) #On lit les choix des joueurs
        self.partage_diamants_fin() #On partage les diamants aux joueurs
        
        self.classement_joueurs() #On classe les joueurs par ordre de score
        
        self.nbjoueurs_plateau = self.nbjoueurs_restant #On met à jour le nombre de joueurs sur le plateau

        self.comptabilise_carte(self.donnees_manche[i + 1:]) #On récupère le dernier caractère de la chaîne de caractères, qui est la carte tirée
        

    if not self.doit_continuer(): #On retourne 'X' doit_continuer() retourne False, et 'R' si doit_continuer() retourne True
      return 'X'
    else:
      return 'R'

  def lecture_choix_joueurs(self, choix):
    """
    Va lire les choix des joueurs et mettre à jour les variables des joueurs
    
    Args:
      choix (str): Liste des choix des joueurs
      
    Returns: /
    """
    self.nbjoueurs_restant = 0
    self.nbsorties = 0
    for i in range(len(choix)): #On parcourt la liste des choix des joueurs
      self.choix = self.donnees_manche[i + 1:] #On récupère le dernier caractère de la chaîne de caractères, qui est la carte tirée
      if choix[i] == 'R': #Si le joueur a choisi de rentrer
        self.joueurs[i].etat = 'R'
        self.nbsorties += 1 #On incrémente le nombre de joueurs qui ont choisi de rentrer
      elif choix[i] == 'N': #Si l'état du joueur est 'Néant'
        self.joueurs[i].etat = 'N'
      elif choix[i] == 'X': #Si le joueuru a choisi d'explorer
        self.joueurs[i].etat = 'X' 
    for i in range(len(self.joueurs)): #On parcourt la liste des joueurs
      if self.joueurs[i].etat == 'X': #Si le joueur est encore sur le plateau
        self.nbjoueurs_restant += 1 #On incrémente le nombre de joueurs restants sur le plateau
    return

  def partage_diamants(self):
    """
    Partage les diamants aux joueurs qui sont encore sur le plateau
    
    Args: /
    
    Returns: /
    """
    for i in range(len(self.joueurs)): #On parcourt la liste des joueurs
      if self.joueurs[i].etat == 'X': #Si le joueur est encore sur le plateau
        self.joueurs[i].diamant_poche += self.tresor_partage #On ajoute les diamants au joueur

  def partage_diamants_fin(self):
    """
    Partage les diamants aux joueurs qui quittent le plateau
    
    Args: /
    
    Returns: /"""
    if self.nbsorties >= 1:
      diamants_partage = self.tresor_sol // self.nbsorties
      for i in range(len(self.joueurs)):
        if self.joueurs[i].etat == 'R':
          self.joueurs[i].diamant_poche += diamants_partage
          self.joueurs[i].diamant_campement += self.joueurs[i].diamant_poche
          self.joueurs[i].diamant_poche = 0
      self.tresor_sol = self.tresor_sol % self.nbsorties
    if self.nbsorties == 1 and self.valreliquesol > 0:
      for i in range(len(self.joueurs)):
        if self.joueurs[i].etat == 'R':
          self.joueurs[i].diamant_campement += self.valreliquesol
          self.valreliquesol = 0
          self.nbrelique = 0

  def fin_de_manche(self, raison: str, dernier_tour: str) -> None:
    """Appelé à chaque fin de manche

      Args:
          raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
          dernier_tour (str): descriptif du dernier tour de la manche

      Returns: /
      """
    
    if not raison == 'R': #Si la manche se termine à cause d'un piège
      self.pieges_sortie[raison] -= 1  #On décrémente le nombre de pièges de ce type qui pourront encore être tirés
      
    for i in range(len(dernier_tour)): #On réalise la même chose que dans la fonction action mais pour le dernier tour
      if dernier_tour[i] == '|':
        
        self.choix_joueurs = dernier_tour[:i].split(',')
        self.lecture_choix_joueurs(self.choix_joueurs)
        self.partage_diamants_fin()
        
        self.classement_joueurs()
        
        self.nbjoueurs_plateau = self.nbjoueurs_restant
  
        self.comptabilise_carte(dernier_tour[i + 1:])
 
    self.historique = [] #On vide l'historique des cartes
    self.tour = 0
    self.tresor_sol = 0
    self.tresor_partage = 0
    self.liste_pieges = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0}
    self.nbrelique = 0
    self.valreliquesol = 0
    self.nbjoueurs_plateau = self.nbjoueurs
    self.nbjoueurs_restant = 0
    self.nbsorties = 0
    self.relique_en_jeu += 1
    self.carte_dans_le_deck = 15 + self.relique_en_jeu
    for j in range(len(self.joueurs)): #On vide les poches des joueurs
      self.joueurs[j].diamant_poche = 0
    
    for x in self.pieges_sortie.keys(): #On remet les pièges dans le deck en fonction des pièges qui ont été tirés pendant la manche
      self.carte_dans_le_deck += self.pieges_sortie[x]
    

    
  def game_over(self, scores: str) -> None:
    #print(self.classement_diamants)
    """Appelé à la fin du jeu ; sert à ce que vous voulez

      Args:
          scores (str): descriptif des scores de fin de jeu
      """

  
  def classement_joueurs(self): 
    """
    Classe les joueurs en fonction de leur nombre de diamants en ajoutant un booléen pour savoir si le joueur est notre IA
    
    Args: /
    
    Returns: /
    """
    self.classement_diamants = []
  
    for i in range(len(self.joueurs)) :
      self.classement_diamants.append([self.joueurs[i].diamant_campement,self.joueurs[i].est_ia,self.joueurs[i].etat]) #On ajoute le nombre de diamants du joueur et un booléen pour savoir si c'est notre IA et son état
      self.classement_diamants.sort() #On trie la liste
      
    cpt = 0 
    while not self.classement_diamants[cpt][1]: #On cherche l'indice de notre IA dans la liste
      
      if self.classement_diamants[cpt][1]: #Si on trouve notre IA on arrâte la boucle
        break 
      cpt += 1
    self.indice_ia = cpt #On stocke l'indice de notre IA dans la variable indice_ia
      

class Joueur:
  def __init__(self, est_ia): #On ajoute un booléen pour savoir si le joueur est notre IA
    """
    Initialisation du joueur
      
    Args:
      est_ia (bool): True si le joueur est notre IA, False sinon

    Returns: /
    """
    self.etat = 'X' #X = Explore, R = Rentre, N = Hors jeu
    self.diamant_poche = 0 #Diamants dans la poche du joueur
    self.diamant_campement = 0 #Diamants dans le campement du joueur
    self.est_ia = est_ia #Booléen pour savoir si le joueur est notre IA

