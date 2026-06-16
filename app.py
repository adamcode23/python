mot_de_passe = input("quel est le mot de passe ? ")

if len(mot_de_passe) < 4:
    print("le mot de passe est trop court !")
if len(mot_de_passe) > 4:
    print("le mot de passe est trop long !")
if len(mot_de_passe) == 0:
    print("le mot de passe est vide !")
    print("relancer le programme !")

if mot_de_passe == "1234":
    print("mot de passe correct !")
else: 
    print("mot de passe incorrect !")
print("Le programme est terminé !")