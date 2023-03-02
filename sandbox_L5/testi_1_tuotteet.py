import sqlite3

db = sqlite3.connect("sandbox_L5/testi.db")
db.isolation_level = None

def tarkista_tietokannan_olemassaolo():
   try:
    db.execute("CREATE TABLE Tuotteet (id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
    return "Taulu on nyt luotu"
   except:
    return "Taulu on jo olemassa"
 

def lisaa_tuote(nimi, hinta):
    db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES (?,?)", [nimi, hinta])

def hae_hinta(nimi):
    hinta = db.execute("SELECT hinta FROM Tuotteet WHERE nimi=?", [nimi]).fetchone()
    if hinta:
        return hinta[0]
    else:
        return None
     
def tulosta_tuote_lista():
   tuotteet = db.execute("SELECT nimi, hinta FROM Tuotteet").fetchall()
   return tuotteet

def tulosta_kallein_tuote():
    kallein = db.execute("SELECT nimi, MAX(hinta) FROM Tuotteet").fetchall()
    return kallein