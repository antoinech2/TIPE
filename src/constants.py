#Constantes raccourci

#phase_infection :
MORT = -1
NEUTRE = 0
INFECTE = 1
IMMUNISE = 2
SAIN = [NEUTRE, IMMUNISE]
REMOVED = [IMMUNISE, MORT]


NAME = {
MORT : "décédé",
NEUTRE : "neutre",
INFECTE : "infecté",
#SAIN : "sain",
IMMUNISE : "immunisé"
}

COLOR = {
MORT : ['#AB63FA', '#AB63FA'],
NEUTRE : ['#636EFA', '#636EFA'],
INFECTE : ['#EF553B', '#EF553B'],
#SAIN : [],
IMMUNISE : ['#00CC96', '#00CC96']
}

DUREE = {
INFECTE : 10 
}
