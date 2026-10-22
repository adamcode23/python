print("calculateur de moyenne au brevet")
moyenne = float(input("Entrez votre moyenne au brevet : "))
if moyenne < 10:
    print("ta pas ton brevet")
if moyenne >= 10 and moyenne < 12:
    print("tu as ton brevet sans mention")
elif moyenne >= 12 and moyenne < 14:
    print("tu as ton brevet avec mention assez bien")
elif moyenne >= 14 and moyenne < 16:
    print("tu as ton brevet avec mention bien")
elif moyenne >= 16 and moyenne < 20:
    print("tu as ton brevet avec mention très bien")
elif moyenne >= 20:
    print("tu as ton brevet avec mention très bien")

