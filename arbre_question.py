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
    b = random.randint(1, 9)
    question = f"3. Calculer : {a} / {b} (arrondir à l'entier le plus proche)"
    reponse = round(a / b)
    return question, reponse

ArbreQuestion = {

}