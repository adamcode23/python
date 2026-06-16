mot_de_passe = input("quel est le mot de passe ? ")

if len(mot_de_passe) < 4:
    if len(mot_de_passe) == 0:
        print("écris autre chose")
    else:
        print("mot de passe trop court !")
elif mot_de_passe == "1234":
    print("mot de passe correct !")
    print("mais il n'ai pas très sécurisé, je te conseille de le changer !")
else:
    print("mot de passe incorrect !")

print("Le programme est terminé !")