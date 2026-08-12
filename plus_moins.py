import random
nbr_random = random.randint(1, 100)
while True:
    try:
        nbr_player = int(input("donne un nbr entre 1 et 100  "))
    except ValueError:
        print("Mettre un nombre entier.")
        continue
    if nbr_player > 100 or nbr_player < 1:
        print("Le nombre doit être compris entre 1 et 100 .")
        continue
    if nbr_player < nbr_random:
        print("mettre un nombre plus grand !")
    elif nbr_player > nbr_random:
        print("mec met un nbr plus petit stp ")
    else:
        print ("GG's ta win la game ")