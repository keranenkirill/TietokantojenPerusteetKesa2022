import testi_1_tuotteet
tuotteet = testi_1_tuotteet

tulos = tuotteet.tarkista_tietokannan_olemassaolo()
print("* ",tulos," *")
print()



print("1 - Lisää uusi tuote")
print("2 - Hae tuotteen hinta")
print("3 - Tulosta Tuotteet-lista")
print("4 - Tulosta Tuotteet-listan kallein tuote")
print("5 - Sulje ohjelma")
print()
print()

while True:
    print()
    komento = input("Anna komento: ")

    if komento == "1":
        nimi = input("Tuotteen nimi: ")
        hinta = input("Tuotteen hinta: ")
        tuotteet.lisaa_tuote(nimi, hinta)

    if komento == "2":
        nimi = input("Tuotteen nimi: ")
        hinta = tuotteet.hae_hinta(nimi)
        if hinta:
            print("Hinta on", hinta)
        else:
            print("Ei löytynyt")

    if komento == "3":
       lista = tuotteet.tulosta_tuote_lista()
       print()
       print("Tuotteet-listalla:")
       for l in lista:
          print(l)
    
    if komento == "4":
        kallein_tuote = tuotteet.tulosta_kallein_tuote()
        print("kallein tuote:",kallein_tuote[0][0], "|",kallein_tuote[0][1]  )

    if komento == "5":
        print("Ohjelma lopetettu.")
        break