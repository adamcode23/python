
print("Bienvenue dans le programme météo !")
celciucs = float(input("quel est la température en celciucs ? "))
if celciucs > 25:
    print("waa i fait super chau")
if celciucs < 15:
    print("waa i fait super froid")
farenheit = celciucs * 9 / 5 + 32
kelvin = celciucs + 273.15
print(("la température en farenheit est de ") + str(farenheit) + (" °F !") + (" et en kelvin de ") + str(kelvin) + (" K ! (paye ton café stp le gooooooaaaaaat kakoukakou)") )