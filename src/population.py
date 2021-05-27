#Fichier pour générer la population
#Objectif : recréer une population représentative de la France par rapport à différents critères.
import sqlite3
import numpy as np

from constants import *

DESTROY_TABLE = True
nb_population = 1000
database_loc_data = "../data/population_data.db"
database_loc_pop = "../data/population.db"

data_db = sqlite3.connect(database_loc_data)
pop_db = sqlite3.connect(database_loc_pop)
data_cur = data_db.cursor()
pop_cur = pop_db.cursor()

def GeneratePopulation():
    print("Génération de la population...")
    if DESTROY_TABLE:
        try:
            pop_cur.execute("DROP TABLE population")
            pop_cur.execute("DROP TABLE etat")
        except:
            pass
    pop_cur.execute('CREATE TABLE IF NOT EXISTS "population" (	"id_individu"	INTEGER NOT NULL, "age"	INTEGER NOT NULL,	"maladie_chronique"	INTEGER NOT NULL DEFAULT 0,	PRIMARY KEY("id_individu" AUTOINCREMENT))')
    pop_cur.execute('CREATE TABLE IF NOT EXISTS "etat" ("id_individu" INTEGER NOT NULL, "etat" INTEGER NOT NULL DEFAULT {} , "duree_etat" INTEGER DEFAULT NULL, "phase_vaccin" INTEGER NOT NULL DEFAULT 0, "id_vaccin" INTEGER DEFAULT NULL, PRIMARY KEY("id_individu" AUTOINCREMENT))'.format(NEUTRE))
    pop_db.commit()

    print("Attribution de l'âge...")
    #AGE
    nb_age = data_cur.execute("SELECT COUNT(age) FROM age").fetchall()[0][0]
    for age in range(nb_age): #Chaque année
        nb_individu_age = round(data_cur.execute("SELECT proportion FROM age WHERE age = ?", (age,)).fetchall()[0][0] * nb_population)
        for individu in range(nb_individu_age): #On créer le bon nombre d'individu de cet age
            pop_cur.execute("INSERT INTO population (age) VALUES (?)", (age,))
            pop_cur.execute("INSERT INTO etat DEFAULT VALUES")
    pop_db.commit()

    print("Attribution de la présence de maladies chroniques...")
    #MALADIES CHRONIQUES
    for (age_min, age_max, proportion) in data_cur.execute("SELECT * FROM maladie_chronique").fetchall():
        pop_cur.execute("UPDATE population SET maladie_chronique = True WHERE id_individu IN (SELECT id_individu FROM population WHERE age >= ? AND age <= ? ORDER BY RANDOM() LIMIT ROUND ((SELECT COUNT(id_individu) FROM population WHERE age >= ? AND age <= ?) * ?))", (age_min, age_max, age_min, age_max, proportion))
    pop_db.commit()

    print("Population générée !")

def CloseDB():
    pop_cur.close()
    pop_db.close()
    data_cur.close()
    data_db.close()


#Getter

def GetAllEtat():
    request = np.array(pop_cur.execute("SELECT id_individu, etat FROM etat").fetchall())
    return request#[(r[k][0], r[k][1]) for k in request]

def GetNombreEtatInfection(etat):
    if type(etat) != list:
        etat = [etat]
    return pop_cur.execute("SELECT COUNT(id_individu) FROM etat WHERE etat IN ({})".format(str(etat)[1:len(str(etat))-1])).fetchall()[0][0]

def GetListEtatInfection(etat):
    if type(etat) != list:
        etat = [etat]
    return np.array(pop_cur.execute("SELECT id_individu FROM etat WHERE etat IN ({})".format(str(etat)[1:len(str(etat))-1])).fetchall())[:, 0]

def GetEtatInfection(id_individu):
    request = pop_cur.execute("SELECT etat FROM etat WHERE id_individu = ?", (int(id_individu),)).fetchall()[0][0]
    return request

def GetListDureeEtat():
    request = np.array(pop_cur.execute("SELECT id_individu, etat, duree_etat FROM etat WHERE duree_etat NOT NULL").fetchall())
    return request#request[:, 0], request[:, 1], request[:, 2]

#Setter

def Infect(id_individu):
    ChangeEtat(id_individu, INFECTE)
    pop_cur.execute("UPDATE etat SET duree_etat = ? WHERE id_individu = ?", (DUREE[INFECTE], id_individu))

def ReduceDureeEtat(id_individu):
    pop_cur.execute("UPDATE etat SET duree_etat = duree_etat - 1 WHERE id_individu = ?", (id_individu, ))

def ChangeEtat(id_individu, new_etat):
    print(id_individu, new_etat)
    pop_cur.execute("UPDATE etat SET etat = ?,  duree_etat = NULL WHERE id_individu = ?", (new_etat, id_individu))

def Mort(id_individu):
    ChangeEtat(id_individu, MORT)

def Immunite(id_individu):
    ChangeEtat(id_individu, IMMUNISE)

def Neutre(id_individu):
    ChangeEtat(id_individu, NEUTRE)
