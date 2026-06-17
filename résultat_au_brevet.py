note = int(input("quel est ta note au brevet ? "))

if note >= 18:
    print("tu as réussi ton brevet !, avec mention très bien et félicitation du jury")
elif note >= 16:
    print("tu as réussi ton brevet !, avec mention très bien")
elif note >= 14:
    print("tu as réussi ton brevet !, avec mention bien")
elif note >= 12:
    print("tu as réussi ton brevet !, avec mention assez bien")
elif note >= 10:
    print("tu as réussi ton brevet !, sans mention")
else:
    print("tu as échoué ton brevet !")