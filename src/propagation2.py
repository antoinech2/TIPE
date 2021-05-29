''' modélisation avec utilisation de plotly '''
'''Le code est expliqué dans l'article sur machinelearnia.com, lien dans le readme'''
#Modules externes
import random as rd
import time
import math as m
import numpy as np
import matplotlib.pyplot as plt

#Modules internes
from constants import *

def distance_e(x, y):  # distance entre 2 points du plan cartésien
    return m.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2))

def chance_infecte(p):  # return True si il devient infecté avec une proba p
    proba = int(p * 100)
    return rd.randint(0, 100) <= proba

def immuniser(l, l2, p):  # l: infectés; l2: immunisés précédents
    drop = 0
    for i in range(len(l)):
        if chance_infecte(p):
            l2.append(l[i-drop])
            l.remove(l[i-drop])
            drop+=1
    return l, l2

def deces(l, l2, l3, p):  # l: infectés; l2: décès précédents; l3: immunisés
    l_p = l[:]  # création d'une copie pour éviter erreur d'indice
    for i in range(len(l_p)):
        if l_p[i] not in l3 and chance_infecte(p):
            l2.append(l_p[i])
            l.remove(l_p[i])
    return l, l2

def StartSimulation():

    print('Début de la simulation ... \n')
    start = time.time()

    #Variables
    variance_pop = 1  # recommandé : 1
    rayon_contamination = 0.5  # recommandé : 0.5
    infectiosite = 0.17  # recommandé : 10%
    p = 0.1  # recommandé : 10%
    d = 0.05  # recommandé : 5%

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'


    """Condition pour éviter erreur, non nécessaire si on utilise le ficheir pour les TIPE
    if nb_population < 10 or rayon_contamination <= 0:
        return 'error, nb_population and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]' """

    # dataset
    x = []
    y = []
    for i in range (nb_population):
            x.append(rd.gauss(0, variance_pop))
            y.append(rd.gauss(0, variance_pop))
    data = {courbe_sains = [],courbe_infectes = [],courbe_immunises = [],courbe_deces = [],courbe_removed = [],coord=[],abscisse_jour=[]}

    id_patient_0 = rd.randint(0, nb_population - 1)  # on choisit le premier individu infecté au hasard
    Infect(id_patient_0)
    coord_1er_infecte = [x[id_patient_0], y[id_patient_0]]  # coordonnées du 1er infecté

    # Remplissage des listes
    data['coord'].append(0)
    for k in range(nb_population):
        if k==id_patient_0 :
            data['coord'].append(coord_1er_infecte)
        else:
            data['coord'].append(x[k], x[k]])

    data['courbe_sains'].append(nb_population-1)
    data['courbe_infectes'].append(1)
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)


        jour = 2
        # Jours 2 à n
    data['abscisse_jour'].append(jour)

while GetNombreEtatInfection(INFECTE) > 0.08 * nb_population or GetNombreEtatInfection(NEUTRE) > 10: #condition d'arrêt
    print("Jour {}...".format(jour))
    for id_individu, etat, duree_etat in GetListDureeEtat():
        if duree_etat != 0:
            ReduceDureeEtat(id_individu)
        else:
            if etat == INFECTE:
                if ChanceMort(id_individu):
                    Mort(id_individu)
                elif ChanceImmunite(id_individu):
                    Immunite(id_individu)
                else:
                    Neutre(id_individu)
            elif etat == IMMUNISE:
                Neutre(id_individu)

    for id_infecte in GetListEtatInfection(INFECTE):
        non_sains = 0
        for id_sain in GetListEtatInfection(SAIN):
            if distance_e(data['coord'][id_infecte],data['coord'][id_sain]) < rayon_contamination :
                if GetEtatInfection(id_sain) in SAIN and ChanceInfection(id_sain):
                    Infect(id_sain)
    pop_db.commit()
    jour += 1

    # pour les courbes finales
    data['courbe_sains'].append(GetNombreEtatInfection(SAIN))
    data['courbe_infectes'].append(GetNombreEtatInfection(INFECTE))
    data['courbe_immunises'].append(GetNombreEtatInfection(IMMUNISE))
    data['courbe_deces'].append(GetNombreEtatInfection(MORT))
    data['courbe_removed'].append(GetNombreEtatInfection(REMOVED))
    data['abscisse_jour'].append(jour)

plt.plot(data['abscisse_jour'], data['courbe_sains'])
plt.plot(data['abscisse_jour'], data['courbe_infectes'])
plt.plot(data['abscisse_jour'], data['courbe_immunises'])
plt.plot(data['abscisse_jour'], data['courbe_deces'])
plt.plot(data['abscisse_jour'], data['courbe_removed'])
