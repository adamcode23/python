nb_vies = 7
mot_a_deviner = "python"
mot_public = "_" * len(mot_a_deviner)
while nb_vies > 0 and mot_public != mot_a_deviner:
    lettre = input("Entrez une lettre : ")
    if lettre in mot_a_deviner:
        for i in range(len(mot_a_deviner)): 
            if mot_a_deviner[i] == lettre:
                mot_public = mot_public[:i] + lettre + mot_public[i+1:]