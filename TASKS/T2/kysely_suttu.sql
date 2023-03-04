-- SQLite


.schema

-- SELECT * FROM KurssinOpettajat;
-- SELECT * FROM Kurssit;
--SELECT * FROM Opettajat;
--SELECT * FROM Opiskelijat;

--SELECT * FROM Ryhmat;
--SELECT * FROM Ryhmat_opettaja_jasen;
--SELECT * FROM Ryhmat_oppilas_jasen;

-- SELECT * FROM Suoritukset;

--SELECT Opiskelijat.nimi, Ryhmat.nimi
--FROM Opiskelijat, Ryhmat, Ryhmat_oppilas_jasen
--WHERE Opiskelijat.id = Ryhmat_oppilas_jasen.oppilas_id AND Ryhmat.id = Ryhmat_oppilas_jasen.ryhma_id;


--SELECT Opettajat.nimi, Ryhmat.nimi
--FROM Opettajat, Ryhmat, Ryhmat_opettaja_jasen
--WHERE Opettajat.id = Ryhmat_opettaja_jasen.opettaja_id AND Ryhmat.id = Ryhmat_opettaja_jasen.ryhma_id;


-- hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
--SELECT * FROM Opettajat;
--SELECT * FROM KurssinOpettajat;

--SELECT * FROM Opettajat;
--SELECT * FROM Kurssit;
--SELECT * FROM KurssinOpettajat;
--SELECT * FROM Suoritukset;

--SELECT KurssinOpettajat.kurssi_id FROM KurssinOpettajat, Opettajat WHERE Opettajat.id = KurssinOpettajat.opettaja_id AND Opettajat.nimi ="Erkki Kaila";


--SELECT COUNT(Suoritukset.kurssi_id)
--FROM Suoritukset, KurssinOpettajat, Opettajat
--WHERE Suoritukset.kurssi_id = KurssinOpettajat.kurssi_id AND KurssinOpettajat.opettaja_id  = Opettajat.id AND Opettajat.nimi = "Leena Salmela";


--SELECT Kurssit.nimi, Suoritukset.arvosana
--FROM Kurssit, Suoritukset, Opiskelijat
--WHERE Kurssit.id = Suoritukset.kurssi_id AND Opiskelijat.id = Suoritukset.oppilas_id AND Opiskelijat.nimi = "Esko Ukkonen";


--SELECT COUNT(Suoritukset.kurssi_id) FROM Suoritukset WHERE Suoritukset.paiva LIKE '%2020%';
--SELECT COUNT(Suoritukset.kurssi_id) FROM Suoritukset WHERE Suoritukset.paiva LIKE '2020-%';


--SELECT Suoritukset.arvosana, COUNT(*) as "saatujen arvosanojen maara" 
--FROM Suoritukset, Kurssit
--WHERE Suoritukset.kurssi_id = Kurssit.id AND Kurssit.nimi = "Ohjelmoinnin perusteet"
--GROUP BY arvosana;



SELECT Kurssit.nimi, 
      COUNT(DISTINCT KurssinOpettajat.opettaja_id), 
      COUNT(DISTINCT Suoritukset.oppilas_id)
FROM Opettajat, Opiskelijat, Kurssit 
      LEFT JOIN KurssinOpettajat 
            ON  Kurssit.id = KurssinOpettajat.kurssi_id 
      LEFT JOIN Suoritukset 
            ON Kurssit.id = Suoritukset.kurssi_id
GROUP BY Kurssit.id;


--SELECT Opettajat.id
--FROM Opettajat;


--SELECT Opettajat.nimi, Kurssit.nimi
--FROM Opettajat, Kurssit, KurssinOpettajat
--WHERE Opettajat.id = KurssinOpettajat.opettaja_id AND Kurssit.id = KurssinOpettajat.kurssi_id AND Opettajat.id =1 ;

SELECT * FROM Ryhmat_oppilas_jasen;
SELECT * FROM Suoritukset ;
SELECT * FROM Opiskelijat ;
SELECT * FROM Kurssit ;


SELECT nimi FROM Ryhmat GROUP BY nimi;
SELECT Suoritukset.oppilas_id
FROM Suoritukset, Opiskelijat, Kurssit, Ryhmat_oppilas_jasen, Ryhmat
WHERE Opiskelijat.id = Suoritukset.oppilas_id 
      AND Ryhmat_oppilas_jasen.oppilas_id = Opiskelijat.id 
      AND Ryhmat_oppilas_jasen.ryhma_id = Ryhmat.id 
      AND Suoritukset.kurssi_id = Kurssit.id 
      AND Ryhmat.nimi ="Basic-koodarit";







--#hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
--# "Antti Laaksonen", "Otto Nurmi"

--SELECT Ryhmat.nimi
--FROM Ryhmat, Ryhmat_opettaja_jasen, Ryhmat_oppilas_jasen, Opettajat, Opiskelijat
--WHERE Opiskelijat.id = Ryhmat_oppilas_jasen.oppilas_id AND Ryhmat.id = Ryhmat_oppilas_jasen.ryhma_id
--      AND Opettajat.id = Ryhmat_opettaja_jasen.opettaja_id AND Ryhmat.id = Ryhmat_opettaja_jasen.ryhma_id
--      AND Opettajat.nimi = "Antti Laaksonen" AND Opiskelijat.nimi = "Otto Nurmi";


