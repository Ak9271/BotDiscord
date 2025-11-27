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


ArbreQuestion = {

}