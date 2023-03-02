import sqlite3

db = sqlite3.connect("sandbox_L5/testi.db")
db.isolation_level = None

#ohjelman alussa tarkistetaan, että taulu on olemassa
try:
    db.execute("CREATE TABLE Tuotteet (id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
except:
    print("Taulua ei voitu luoda, sillä se on olemassa")
    print()


print("1 - Lisää uusi tuote")
print("2 - Hae tuotteen hinta")
print("3 - Tulosta Tuotteet-lista")
print("4 - Sulje ohjelma")

while True:
    komento = input("Anna komento: ")

    if komento == "1":
        nimi = input("Tuotteen nimi: ")
        hinta = input("Tuotteen hinta: ")
        db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES (?,?)", [nimi, hinta])

    if komento == "2":
        nimi = input("Tuotteen nimi: ")
        hinta = db.execute("SELECT hinta FROM Tuotteet WHERE nimi=?", [nimi]).fetchone()
        if hinta:
            print("Hinta on", hinta[0])
        else:
            print("Ei löytynyt")
    
    if komento == "3":
       tuotteet = db.execute("SELECT nimi, hinta FROM Tuotteet").fetchall()
       print()
       print("Tuotteet-listalla:")
       for tuote in tuotteet:
         print(tuote) 
       print()

    if komento == "4":
        break