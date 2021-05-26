#Fichier pour générer la population
#Objectif : recréer une population représentative de la France par rapport à différents critères.
import  sqlite3

DESTROY_TABLE = True
nb_population = 1000000
database_loc_data = "../data/population_data.db"
database_loc_pop = "../data/population.db"

def GeneratePopulation():
    print("Génération de la population...")
    data_db = sqlite3.connect(database_loc_data)
    pop_db = sqlite3.connect(database_loc_pop)
    data_cur = data_db.cursor()
    pop_cur = pop_db.cursor()
    if DESTROY_TABLE:
        pop_cur.execute("DROP TABLE population")
    pop_cur.execute('CREATE TABLE "population" (	"id_individu"	INTEGER NOT NULL, "age"	INTEGER NOT NULL,	"maladie_chronique"	INTEGER NOT NULL DEFAULT 0,	PRIMARY KEY("id_individu" AUTOINCREMENT))')
    pop_db.commit()

    print("Attribution de l'âge...")
    #AGE
    nb_age = data_cur.execute("SELECT COUNT(age) FROM age").fetchall()[0][0]
    for age in range(nb_age): #Chaque année
        nb_individu_age = round(data_cur.execute("SELECT proportion FROM age WHERE age = ?", (age,)).fetchall()[0][0] * nb_population)
        for individu in range(nb_individu_age): #On créer le bon nombre d'individu de cet age
            pop_cur.execute("INSERT INTO population (age) VALUES (?)", (age,))
    pop_db.commit()

    print("Attribution de la présence de maladies chroniques...")
    #MALADIES CHRONIQUES
    for (age_min, age_max, proportion) in data_cur.execute("SELECT * FROM maladie_chronique").fetchall():
        pop_cur.execute("UPDATE population SET maladie_chronique = True WHERE id_individu IN (SELECT id_individu FROM population WHERE age >= ? AND age <= ? ORDER BY RANDOM() LIMIT ROUND ((SELECT COUNT(id_individu) FROM population WHERE age >= ? AND age <= ?) * ?))", (age_min, age_max, age_min, age_max, proportion))
    pop_db.commit()

    print("Population générée !")
    pop_cur.close()
    pop_db.close()
    data_cur.close()
    data_db.close()

GeneratePopulation()
