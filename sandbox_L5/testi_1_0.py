import sqlite3

db = sqlite3.connect("sandbox_L5/testi.db")
db.isolation_level = None

# tietokantakomennot

try:
    db.execute("CREATE TABLE Tuotteet (id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
except:
    print("Taulua ei voitu luoda")

nimi = input("Lisättävän tuotteen nimi: ")
hinta = input("Lisättävän tuotteen hinta: ")
lisatty_tuote = db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES (?, ?)", [nimi, hinta])
print()
print("Lisätty Tuotteet-listalle:",nimi, hinta, "ja tuotteen id:", lisatty_tuote.lastrowid)
print()

nimi = input("Etsittävän tuotteen nimi: ")
hinta = db.execute("SELECT hinta FROM Tuotteet WHERE nimi=?", [nimi]).fetchone()
if hinta:
    print("Tuotteen", nimi, "hinta on", hinta[0])
else:
    print("Ei löytynyt")


tuotteet = db.execute("SELECT nimi, hinta FROM Tuotteet").fetchall()
print()
print("Tuotteet-listalla:")
for tuote in tuotteet:
   print(tuote) 
print()



