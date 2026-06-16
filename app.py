mot_de_passe = input("quel est le mot de passe ? ")

if len(mot_de_passe) < 4:
    if len(mot_de_passe) == 0:
        print("lécrire autre chose")
    else:
        print("mot de passe trop court !")
print("Le programme est terminé !")