vies = 7
mot_mystere = "python"
mot_public = "_" * len(mot_mystere)
while vies > 0 and mot_mystere != mot_public:
    lettre = input("donne une lettre : ")
    if lettre in mot_mystere:
        for i in range(len(mot_mystere)): #en mode ca fait regarde chaque lettre est fait une place pour chaque lettre du mot mystere
            if mot_mystere[i] == lettre: #si une place du mot mystere grace a la variable i = la lettre donner par le joueur alors on remplace le _ par la lettre donner par le joueur
                mot_public = mot_public[:i] + lettre + mot_public[i + 1:]
    else:
        vies -= 1
    print(mot_public)
    print("il te reste ", vies," vies")     

if mot_public == mot_mystere:
    print("bravo tu a trouver : ", mot_public)
elif vies == 0:
    print("tu est mort")



