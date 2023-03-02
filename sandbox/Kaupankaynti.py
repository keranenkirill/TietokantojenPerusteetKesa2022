import sqlite3

db = sqlite3.connect("sandbox/Kaupankayntidb.db")
db.isolation_level = None

Maijan_ostoslista = db.execute("SELECT Tuotteet.nimi, Tuotteet.hinta FROM Tuotteet, Asiakkaat, Ostokset WHERE Asiakkaat.id = Ostokset.asiakas_id AND Tuotteet.id = Ostokset.tuote_id AND Asiakkaat.nimi = 'Maija';").fetchall()
print(Maijan_ostoslista)