nb_vies = 7
mot_a_deviner = "python"
mot_public = "_" * len(mot_a_deviner)
while nb_vies > 0 and mot_public != mot_a_deviner:
    print(mot_public)
    lettre = input("Entrez une lettre : ")
    if lettre in mot_a_deviner:
        for i in range(len(mot_a_deviner)): 
            if mot_a_deviner[i] == lettre:
                mot_public = mot_public[:i] + lettre + mot_public[i+1:]
    else:
        nb_vies -= 1
        print("Mauvaise lettre, il te reste", nb_vies, "vies")
    print(mot_public)
    if mot_public == mot_a_deviner:
        print("Bravo, le mot à deviner est", mot_a_deviner)
    elif nb_vies == 0:
        print("Perdu, le mot à deviner était", mot_a_deviner)