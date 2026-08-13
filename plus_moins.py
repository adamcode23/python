import random
nbr_random = random.randint(1, 100)
nbr_vies = 7
nbr_player = None
while nbr_vies > 0 and nbr_player != nbr_random:
    try:
        nbr_player = int(input("donne un nbr entre 1 et 100  "))
    except ValueError:
        print("Mettre un nombre entier.")
        continue
    print(f"il ne te reste plus que {nbr_vies} vies")
    if nbr_player > 100 or nbr_player < 1:
        print("Le nombre doit être compris entre 1 et 100 .")
        continue
    if nbr_player < nbr_random:
        print("mettre un nombre plus grand !")
        nbr_vies -= 1
    elif nbr_player > nbr_random:
        print("mec met un nbr plus petit stp ")
        nbr_vies -= 1
    else:
        print ("GG's ta win la game ")
else:
    if nbr_vies == 0:
        print("Perdu le nombre etait", nbr_random)