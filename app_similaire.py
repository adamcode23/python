nbr_vies = 7
mot_a_deviner = "python"
mot_public = "_" * len(mot_a_deviner)
while nbr_vies > 0 and mot_public != mot_a_deviner:
        try:
            print(mot_public)
            lettre = input("devine le mot caché ecrit une lettre : ")
        except ValueError:
            print("Veuillez entrer une seule lettre.")
            print(mot_public)
            continue
        if lettre in mot_a_deviner:
            for i in range(len(mot_a_deviner)):
                if mot_a_deviner[i] == lettre:
                    mot_public = mot_public[:i] + lettre + mot_public[i+1:]
        else:
            nbr_vies -= 1
            print("mauvaise lettre il te reste", nbr_vies, "vies")
            print(mot_public)
        if mot_public == mot_a_deviner:
            print("Bravo, le mot a deviner est", mot_a_deviner)
        elif nbr_vies == 0:
            print("Perdu, le mot a deviner etait", mot_a_deviner)