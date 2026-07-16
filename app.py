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

if len(str(int(mot_de_passe))) < 4:
    print("Mot de passe trop court !")
elif int(mot_de_passe) == 1234:
    print("Mot de passe correct !")
    print("Mais il n'est pas très sécurisé, je te conseille de le changer !")
else:
    print("Mot de passe incorrect !")

print("Le programme est terminé !")