while True:
    try:
        note = float(input("quel est ta note au brevet ? "))
    except ValueError:
        print(" Entre un nombre valide (utilise un point pour les décimales)😡😡.")
        continue
    if note > 20 or note < 0:
        print("la note doit être comprise entre 0 et 20😡😡")
        continue
    break
if note >= 18:
    print("tu as réussi ton brevet !, avec mention très bien et félicitation du jury😂😂")
elif note >= 16:
    print("tu as réussi ton brevet !, avec mention très bien😃😃")
elif note >= 14:
    print("tu as réussi ton brevet !, avec mention bien😉😉")
elif note >= 12:
    print("tu as réussi ton brevet !, avec mention assez bien🙂🙂")
elif note >= 10:
    print("tu as réussi ton brevet !, sans mention")
else:
    print("tu as échoué ton brevet😱😱 !")