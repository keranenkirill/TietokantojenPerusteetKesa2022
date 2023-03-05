import sqlite3
import random

db = sqlite3.connect("sandbox_L7/kauppa.db")
db.isolation_level = None




db.execute("BEGIN")
for i in range(1,10+1):
    db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES (?,?)", ["tuote"+str(i), 1])
db.execute("COMMIT")

tulos = random.randint(1900, 2000)
print(tulos)