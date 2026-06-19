while True:
    try:
        mot_de_passe = float(input("quel est le mot de passe ? "))
    except ValueError:
        print("Mettre un nombre entier ou décimal (pour les décimal avec des points).")
        continue

    if mot_de_passe > 20 or mot_de_passe < 0:
        print("Le mot de passe doit être compris entre 0 et 20 .")
        continue  

        


    break





if len(str(mot_de_passe)) < 4:
    if len(str(mot_de_passe)) == 0:
        print("écris autre chose")
    else:
        print("mot de passe trop court !")
elif mot_de_passe == 1234:
    print("mot de passe correct !")
    print("mais il n'ai pas très sécurisé, je te conseille de le changer !")
else:
    print("mot de passe incorrect !")

print("Le programme est terminé !")