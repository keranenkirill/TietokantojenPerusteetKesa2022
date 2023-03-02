import sqlite3
db = sqlite3.connect("TASKS/T1/bikes.db")
db.isolation_level = None


def distance_of_user(user):
   kokonaismatka_metreina = db.execute("SELECT SUM(Trips.distance) FROM Users, Trips WHERE Trips.user_id = Users.id AND Users.name = ?", [user]).fetchone()
   return kokonaismatka_metreina[0] 


def speed_of_user(user):
   kokmatk = distance_of_user(user) / 1000
   
   kokonaismatkan_aika = db.execute("SELECT SUM(Trips.duration) FROM Users, Trips WHERE Trips.user_id = Users.id AND Users.name = ?", [user]).fetchone()
   kokmatk_aik = kokonaismatkan_aika[0]/60
   
   return round((kokmatk) / kokmatk_aik, 2)      
    
   
def duration_in_each_city(day):
   #lista == lista kokonaisajasta pyörien päällä kaupunkikohtaisesti tiettynä päivänä
   # SQL-kyselyssä yhdistävänä tekijänä on Bikes taulun tiedot, sillä Bikes tiedoilla viitataan Cities-tauluun ja Trips-taulussa viitataan Bikes-tauluun
   lista = db.execute("SELECT Cities.name, SUM(Trips.duration) FROM Bikes, Cities, Trips WHERE Trips.bike_id = Bikes.id AND Bikes.city_id = Cities.id AND Trips.day = ? GROUP BY Cities.name", [day]).fetchall()
   return lista
   
   
def users_in_city(city):
   #eri_kavijoiden_maar == kertoo montako eri useria on käynyt tietysä kaupungissa
   #SQL-kyselyssä emme käytä Users-taulua, sillä user_id on löydettävissä Trips-taulusta,
   #  joten riittänee kyselyä rajoittaa taas yhdistävään tekijään kuten yllä *((def duration_in_each_city(day)))*  eli Bikes-taulun mukaan
   eri_kavijoiden_maar = db.execute("SELECT COUNT(DISTINCT Trips.user_id) FROM Bikes, Cities, Trips WHERE Bikes.id = Trips.bike_id AND Bikes.city_id = Cities.id AND Cities.name = ?", [city]).fetchone()
   return eri_kavijoiden_maar[0]
   
   
   
def trips_on_each_day(city):
   #matkoja_paivassa == lista kaikista tietokannassa olevista päivistä, jolloin tehtiin ainakin yksi matka
   #Tässä aika selväää on, että käytämme yhdistävänä tauluna todettua Bikes-taulua,
   #  lisäksi Trips-taulu on tärkeä, sillä saadaan ryhmiteltyä päivien mukaan 
   matkoja_paivassa = db.execute("SELECT Trips.day, COUNT(Trips.duration) FROM Bikes, Trips, Cities WHERE Bikes.id = Trips.bike_id AND Cities.id = Bikes.city_id AND Cities.name =? GROUP BY Trips.day", [city]).fetchall()
   return matkoja_paivassa
   
   
   
def most_popular_start(city):
   enitenlahtoja_pys = db.execute("SELECT Stops.name, COUNT(Trips.id) AS lahtojen_maara FROM Stops, Cities, Trips WHERE Cities.id = Stops.city_id  AND Stops.id = Trips.from_id AND Cities.name =? GROUP BY Trips.from_id ORDER BY lahtojen_maara DESC", [city]).fetchall()
   return enitenlahtoja_pys[0]
   
