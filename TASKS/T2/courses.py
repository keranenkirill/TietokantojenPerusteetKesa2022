import os
import sqlite3

try:
   # poistaa tietokannan alussa (kätevä moduulin testailussa)
   os.remove("TASKS/T2/courses.db")
   print("TIETOKANTA POISTETTU ONNISTUNEESTI")
except:
   # mikäli tietokantaa ei ollut vielä olemassa, niin exceptionilla virheviesti
   print("TIETOKANTAA EI VOITU POISTAA, SILLÄ SE EI OLE OLEMASSA")

try:
   db = sqlite3.connect("TASKS/T2/courses.db")
   db.isolation_level = None  
   print("TIETOKANTA LUOTU ONNISTUNEESTI")
except:
   print("TIETOKANNAN UUDELLEENLUOMISESSA ONGELMIA")


# luo tietokantaan tarvittavat taulut
def create_tables():
   db.execute("CREATE TABLE Opettajat (id INTEGER PRIMARY KEY, nimi TEX);")
   
   db.execute("CREATE TABLE Kurssit (id INTEGER PRIMARY KEY, nimi TEXT, opintopisteet INTEGER);")
   
   db.execute("CREATE TABLE KurssinOpettajat (kurssi_id INTEGER REFERENCES Kurssit, opettaja_id INTEGER REFERENCES Opettaja);")
   
   db.execute("CREATE TABLE Opiskelijat (id INTEGER PRIMARY KEY, nimi TEX);")
   
   db.execute("CREATE TABLE Suoritukset (id INTEGER PRIMARY KEY, oppilas_id INTEGER REFERENCES Opiskelijat, kurssi_id INTEGER REFERENCES Kurssit, paiva TEXT, arvosana INTEGER);")
   
   db.execute("CREATE TABLE Ryhmat (id INTEGER PRIMARY KEY, nimi TEXT)")
   db.execute("CREATE TABLE Ryhmat_opettaja_jasen (ryhma_id REFERENCES Ryhmat, opettaja_id INTEGER REFERENCES Opettajat)")
   db.execute("CREATE TABLE Ryhmat_oppilas_jasen (ryhma_id REFERENCES Ryhmat, oppilas_id INTEGER REFERENCES Opiskelijat)")
   
   


# lisää opettajan tietokantaan
def create_teacher(name):
   try:
      db.execute("INSERT INTO Opettajat (nimi) VALUES (?)", [name])
      opettajan_id = db.execute("SELECT Opettajat.id FROM Opettajat WHERE Opettajat.nimi =?", [name]).fetchone()
      print("LISÄTTY ONNISTUNEESTI OPETTAJA:", name, " id:", opettajan_id[0])
      return opettajan_id[0]
   except:
      print("OPETTAJAN LISÄÄMISESSÄ TAULUUN ILMENNYT ONGELMA")
        
        
# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
   print( "lisättävän opettajan/opettajien id:t ", teacher_ids)
   
   db.execute("INSERT INTO Kurssit (nimi, opintopisteet) VALUES (?,?)", [name, credits])
   print("lisätty kurssi:", name," sen opintopisteet:", credits )
   
   lisatyn_kurssin_id = db.execute("SELECT Kurssit.id FROM Kurssit WHERE Kurssit.nimi =?", [name]).fetchone()
   print("lisätyn kurssin id: ",lisatyn_kurssin_id)
   print()
   for opettaja_id in teacher_ids:
      db.execute("INSERT INTO KurssinOpettajat (kurssi_id, opettaja_id) VALUES (?, ?)", [lisatyn_kurssin_id[0], opettaja_id])
   
   return lisatyn_kurssin_id[0]
  
           
# lisää opiskelijan tietokantaan
def create_student(name):
   print("lisättävän opiskelijan nimi:", name)
   db.execute("INSERT INTO Opiskelijat (nimi) VALUES (?)", [name])
   print()
    
   lisatyn_opiskelijan_id = db.execute("SELECT Opiskelijat.id FROM Opiskelijat WHERE Opiskelijat.nimi =?", [name]).fetchone()
   return lisatyn_opiskelijan_id[0]


# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
   #print(student_id, course_id,  date,grade)
   db.execute("INSERT INTO Suoritukset (oppilas_id, kurssi_id, paiva, arvosana) VALUES (?, ?, ?, ?)", [student_id, course_id, date, grade])
   print("lisätty suoritus opiskelijalle (id):", student_id, " kurssina (id):", course_id, " päiväyksenä:", date, " arvosanalla:", grade)
   print()


# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):    
    #print(name, teacher_ids, student_ids)
    db.execute("INSERT INTO Ryhmat (nimi) VALUES (?)", [name])
    ryhman_id = db.execute("SELECT id FROM Ryhmat WHERE Ryhmat.nimi =?", [name]).fetchone()
    ryhman_id = ryhman_id[0]
    #print(ryhman_id)
    for student_id in student_ids:
      db.execute("INSERT INTO Ryhmat_oppilas_jasen (ryhma_id, oppilas_id) VALUES (?,?)", [ryhman_id, student_id])
   
    for teacher_id in teacher_ids:
      db.execute("INSERT INTO Ryhmat_opettaja_jasen (ryhma_id, opettaja_id) VALUES (?,?)", [ryhman_id, teacher_id])


# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    kurssilista = db.execute("SELECT Kurssit.nimi FROM Kurssit, Opettajat, KurssinOpettajat WHERE Kurssit.id = KurssinOpettajat.kurssi_id AND Opettajat.id = KurssinOpettajat.opettaja_id AND Opettajat.nimi =? ;", [teacher_name]).fetchall()
    tulos_lista =[]
    for kurssi in kurssilista:
       tulos_lista.append(kurssi[0])
   
    return tulos_lista


# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    kurssien_maara = db.execute("SELECT COUNT(Suoritukset.kurssi_id) FROM Suoritukset, KurssinOpettajat, Opettajat WHERE Suoritukset.kurssi_id = KurssinOpettajat.kurssi_id AND KurssinOpettajat.opettaja_id  = Opettajat.id AND Opettajat.nimi =?;", [teacher_name]).fetchone()
    kurssipisteiden_maara = kurssien_maara[0] * 5
    return kurssipisteiden_maara


# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    kurssit_arvosanoineen = db.execute("SELECT Kurssit.nimi, Suoritukset.arvosana FROM Kurssit, Suoritukset, Opiskelijat WHERE Kurssit.id = Suoritukset.kurssi_id AND Opiskelijat.id = Suoritukset.oppilas_id AND Opiskelijat.nimi =?;", [student_name]).fetchall()
    return kurssit_arvosanoineen 
 
 
# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    #tässä oli dotettu olevan monta eri tapaa toeuttaa %%-kohdassa
    #opintopisteiden_maara = db.execute("SELECT Suoritukset.kurssi_id, Suoritukset.paiva FROM Suoritukset;").fetchall()
    opintopisteiden_maara = db.execute("SELECT COUNT(Suoritukset.kurssi_id) FROM Suoritukset WHERE Suoritukset.paiva LIKE '%' || ? || '%';", [year]).fetchone()
    #print (opintopisteiden_maara[0])
    opintopisteiden_maara = opintopisteiden_maara[0]*5
    return opintopisteiden_maara
    
    
# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    arvosana_parit = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    #print(arvosana_parit)

    tulos_lista = db.execute("SELECT Suoritukset.arvosana, COUNT(*) as 'saatujen arvosanojen maara' FROM Suoritukset, Kurssit WHERE Suoritukset.kurssi_id = Kurssit.id AND Kurssit.nimi = ? GROUP BY arvosana;", [course_name]).fetchall()
    #print(tulos_lista)
    
    for i in tulos_lista:       
       arvosana_parit[i[0]] = i[1]
       
    return arvosana_parit

             
# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    tulos_taulu = db.execute("SELECT Kurssit.nimi, COUNT(DISTINCT KurssinOpettajat.opettaja_id), COUNT(DISTINCT Suoritukset.oppilas_id) FROM Opettajat, Opiskelijat, Kurssit LEFT JOIN KurssinOpettajat ON  Kurssit.id = KurssinOpettajat.kurssi_id LEFT JOIN Suoritukset ON Kurssit.id = Suoritukset.kurssi_id GROUP BY Kurssit.id;").fetchall()
    
    return tulos_taulu
 
 
# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
   opettajien_nimi_taulu = db.execute("SELECT nimi FROM Opettajat ORDER BY nimi;").fetchall()
   ope_kurssi_list = []
   for nimi in opettajien_nimi_taulu:
      opetuple =()
      #print(nimi[0])
      tupl = list(opetuple)
      tupl.append(nimi[0])
      opetuple = tuple(tupl)

      
      kurssi_list = []
      tulos_taulu = db.execute("SELECT Kurssit.nimi FROM Opettajat, Kurssit, KurssinOpettajat WHERE Opettajat.id = KurssinOpettajat.opettaja_id AND Kurssit.id = KurssinOpettajat.kurssi_id AND Opettajat.nimi = ?;", [nimi[0]]).fetchall()
      for tulos in tulos_taulu:
         #print(tulos[0])
         kurssi_list.append(tulos[0])
         
      tupl = list(opetuple)
      tupl.append(kurssi_list)
      opetuple = tuple(tupl)

      ope_kurssi_list.append(opetuple)
      
      
   return ope_kurssi_list
   

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    #haetaan ryhman opiskelijat
    ryhman_jasenet = []
    
    ryhman_opiskelijat = db.execute("SELECT Opiskelijat.nimi FROM Ryhmat_oppilas_jasen, Opiskelijat, Ryhmat WHERE Opiskelijat.id = Ryhmat_oppilas_jasen.oppilas_id AND Ryhmat.id = Ryhmat_oppilas_jasen.ryhma_id AND Ryhmat.nimi = ?;", [group_name]).fetchall()
    for opiskelija in ryhman_opiskelijat:
       #print(opiskelija[0])
       ryhman_jasenet.append(opiskelija[0])
    
    ryhman_opettajat = db.execute("SELECT Opettajat.nimi FROM Ryhmat_opettaja_jasen, Opettajat, Ryhmat WHERE Opettajat.id = Ryhmat_opettaja_jasen.opettaja_id AND Ryhmat.id = Ryhmat_opettaja_jasen.ryhma_id AND Ryhmat.nimi = ?;", [group_name]).fetchall()
    for opettaja in ryhman_opettajat:
       #print(opettaja[0])    
       ryhman_jasenet.append(opettaja[0])

    ryhman_jasenet.sort()
    return ryhman_jasenet

# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    tulos_lista =[]
    ryhma_nimet = db.execute("SELECT nimi FROM Ryhmat GROUP BY nimi;")
    for ryhma in ryhma_nimet:
       #print(ryhma[0])
       ryhma_tuple = ()
       tupl = list(ryhma_tuple)
       tupl.append(ryhma[0])
       ryhma_tuple = tuple(tupl)
       
       op_pisteet = db.execute("SELECT 5 * COUNT(Suoritukset.oppilas_id) FROM Suoritukset, Opiskelijat, Kurssit, Ryhmat_oppilas_jasen, Ryhmat WHERE Opiskelijat.id = Suoritukset.oppilas_id AND Ryhmat_oppilas_jasen.oppilas_id = Opiskelijat.id AND Ryhmat_oppilas_jasen.ryhma_id = Ryhmat.id AND Suoritukset.kurssi_id = Kurssit.id AND Ryhmat.nimi =?;", [ryhma[0]]).fetchone()
       #print(op_pisteet[0])
       tupl = list(ryhma_tuple)
       tupl.append(op_pisteet[0])
       ryhma_tuple = tuple(tupl)
       
       tulos_lista.append(ryhma_tuple)
      
    return tulos_lista

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    pass