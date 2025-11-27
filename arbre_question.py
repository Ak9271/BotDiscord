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
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    c = random.randint(1, 20)
    question = f"2. Calculer : ({a} - {b}) * {c}"
    reponse = (a - b) * c
    return question, reponse

def generer_calcul_3():
    a = random.randint(1, 1000)
    b = random.randint(1, 10)
    question = f"3. Calculer : {a} / {b} (arrondir à l'entier le plus proche)"
    reponse = round(a / b)
    return question, reponse

def generer_calcul_4():
    pourcentage = random.choice([10,15,20,25,30])
    nombre = random.choice([50,100,150,200,250,500])
    question = f"4. Calculer : {pourcentage}% de {nombre}"
    reponse = (pourcentage / 100) * nombre
    return question, reponse

def generer_calcul_5():
    nbr_virgule = random.choice([0.1,0.2,0.5,1.5,2.5,3.5,4.5,5.5])
    nombre = random.randint(1, 1000)
    question = f"5. Calculer : {nombre} * {nbr_virgule}"
    reponse = nombre * nbr_virgule
    return question, reponse

def generer_calcul_6():
    a = random.randint(1,20)
    puissance = random.randint(1,5)
    b = random.randint(1,2000)
    question = f"6. Calculer : {a}^{puissance} - {b}"
    reponse = (a ** puissance) - b
    return question, reponse

def generer_calcul_7():
    x = random.randint(5, 10)
    a = random.randint(2, 4)
    b = random.randint(1, 5)
    c = a * x - b
    question = f"7. Résoudre pour x : {a}x - {b} = {c}. Trouver la valeur de x."
    reponse = x
    return question, reponse

def generer_calcul_8():
    r1 = random.randint(1,5)
    r2 = r1 + random.randint(1,3)
    somme = r1 + r2
    produit = r1 * r2
    question = f"8. x² - {somme}x + {produit} = 0. Trouver les solutions x1 et x2."
    bonne_reponse = sorted([r1, r2])
    reponse_esperee = f"{bonne_reponse[0]} et {bonne_reponse[1]}"
    return question, reponse_esperee

ArbreQuestion = {
    "start": {
        "generateur": generer_calcul_1,
        "suivant": "calcul_2",
        "erreur_max": 2
    },
    "calcul_2": {
        "generateur": generer_calcul_2,
        "suivant": "calcul_3",
        "erreur_max": 2
    },
    "calcul_3": {
        "generateur": generer_calcul_3,
        "suivant": "calcul_4",
        "erreur_max": 2
    },
    "calcul_4": {
        "generateur": generer_calcul_4,
        "suivant": "calcul_5",
        "erreur_max": 3
    },
    "calcul_5": {
        "generateur": generer_calcul_5,
        "suivant": "calcul_6",
        "erreur_max": 3
    },
    "calcul_6": {
        "generateur": generer_calcul_6,
        "suivant": "calcul_7",
        "erreur_max": 3
    },
    "calcul_7": {
        "generateur": generer_calcul_7,
        "suivant": "calcul_8",
        "erreur_max": 4
    },
    "calcul_8": {
        "generateur": generer_calcul_8,
        "suivant": "Note Finale",
        "erreur_max": 5
    },
    "conclusion_finale": {
        "conclusion": "Tu as fini tous les calculs. Bravo !"
    },
    "echec": {
        "conclusion": "Tu as dépassé le nombre maximum d'erreurs autorisées. Fin du test."
    }
}