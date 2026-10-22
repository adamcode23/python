vies = 7
mot_caché = "python"
lettres_trouvées = [lettre for lettre in mot_caché]
while vies > 0:
    lettre = input("devine une lettre : ")
    if len(lettre) != 1:        
            print("tu dois entrer une seule lettre")
            continue
    if lettre in mot_caché:
        print("bien joué ! conitue à deviner")
        lettres_trouvées.append(lettre)
    if all(caractere in lettres_trouvées for caractere in mot_caché):
            print("Bravo ! Tu as trouvé le mot caché.")
            break
    else:
        vies -= 1
        print("mauvaise lettre ! il te reste", vies, "vies")
    if vies == 0:
        print("tu as perdu ! le mot caché était :", mot_caché)
        break
print("le mot caché était :", mot_caché)