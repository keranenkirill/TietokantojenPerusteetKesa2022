import sqlite3

db = sqlite3.connect("sandbox_L5/testi.db")
db.isolation_level = None

# tietokantakomennot

try:
    db.execute("CREATE TABLE Tuotteet (id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
except:
    # KOMENNON TULISI TULOSTAA VIRHEVIESTI, SILLÄ TAULU ON JO OLEMASSA
    print()
    print("Taulua ei voitu luoda")
    print()
