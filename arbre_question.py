import random
import operator

def generer_calcul_1():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    question = f"1. Calculer : {a} + {b} * {c}"
    reponse = a + b * c
    return question, reponse

def generer_calcul_2():
    a = random.randint(1, 1000)
    b = random.randint(1, 10)
    question = f"2. Calculer : {a} / {b} (arrondir à l'entier le plus proche)"
    reponse = round(a / b)
    return question, reponse

def generer_calcul_2_Final():
    pourcentage = random.choice([10,15,20,25,30])
    nombre = random.choice([50,100,150,200,250,500])
    question = f"3. Calculer : {pourcentage}% de {nombre}, (Noter la decimale meme si 0)"
    reponse = (pourcentage / 100) * nombre
    return question, reponse

def generer_calcul_3():
    pourcentage = random.choice([10,15,20,25,30])
    nombre = random.choice([50,100,150,200,250,500])
    question = f"2. Calculer : {pourcentage}% de {nombre}, (Noter la decimale meme si 0)"
    reponse = (pourcentage / 100) * nombre
    return question, reponse

def generer_calcul_4():
    a = random.randint(1,9)
    puissance = random.randint(1,5)
    b = random.randint(1,2000)
    question = f"3. Calculer : {a}^{puissance} - {b}"
    reponse = (a ** puissance) - b
    return question, reponse

def generer_calcul_5():
    x = random.randint(5, 10)
    a = random.randint(2, 4)
    b = random.randint(1, 5)
    c = a * x - b
    question = f"3. Résoudre pour x : {a}x - {b} = {c}. Trouver la valeur de x."
    reponse = x
    return question, reponse

def generer_calcul_6():
    r1 = random.randint(1,9)
    r2 = r1 + random.randint(1,5)
    somme = r1 + r2
    produit = r1 * r2
    question = f"3. x² - {somme}x + {produit} = 0. Trouver les solutions x1 et x2."
    bonne_reponse = sorted([r1, r2])
    reponse_esperee = f"{bonne_reponse[0]} et {bonne_reponse[1]}"
    return question, reponse_esperee

ArbreQuestion = {
    "start": {
        "generateur": generer_calcul_1,
        "reussite": "calcul_3",
        "echec_progression": "calcul_2",
        "erreur_max": 2
    },
    "calcul_2": {
        "generateur": generer_calcul_2,
        "reussite": "calcul_5",
        "echec_progression": "calcul_2_Final",
        "erreur_max": 2
    },
    "calcul_2_Final": {
        "generateur": generer_calcul_2_Final,
        "suivant": "conclusion_finale",
        "erreur_max": 2
    },
    "calcul_3": {
        "generateur": generer_calcul_3,
        "suivant": "calcul_6",
        "echec_progression": "calcul_4",
        "erreur_max": 2
    },
    "calcul_4": {
        "generateur": generer_calcul_4,
        "suivant": "conclusion_finale",
        "erreur_max": 3
    },
    "calcul_5": {
        "generateur": generer_calcul_5,
        "suivant": "conclusion_finale",
        "erreur_max": 3
    },
    "calcul_6": {
        "generateur": generer_calcul_6,
        "suivant": "conclusion_finale",
        "erreur_max": 3
    },
    "conclusion_finale": {
        "conclusion": "Tu as fini tous les calculs. Bravo !"
    },
    "echec": {
        "conclusion": "Tu as dépassé le nombre maximum d'erreurs autorisées. Fin du test."
    }
}