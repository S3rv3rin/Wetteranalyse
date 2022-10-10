CREATE USER 'weatheradm'@'localhost' IDENTIFIED BY 'geheim123';
CREATE DATABASE doit_projekt;
GRANT DELETE, INSERT, SELECT, UPDATE ON doit_projekt . * TO 'weatheradm'@'localhost';

create table doit_projekt.stationen (
    stations_id int primary key,
    plz varchar(5),
    ort varchar(40),     
    landkreis varchar(40),
    bundesland varchar(30),
    land varchar(20),
    breitengrad float,
    laengengrad float,
    stationshoehe int
);
create table doit_projekt.stationkennung_messung_kennung(
	id int primary key,
    kennung_Id varchar(6) not null,
	stationskennung varchar(5) not null ,
    datum_beginn date, 
    datum_ende date
);
create table doit_projekt.stationskennung (
	stationskennung varchar(6) primary key,
    stations_id varchar(5)
);
create table city.cities_germany (
	osm_id int primary key,
    ags varchar(11),
    ort varchar(50),
    plz varchar(11),
    landkreis varchar(50) ,
    bundesland varchar(50)
);
create table doit_projekt.messwerte_kennung (
	kennung_id varchar(6) primary key,
    beschreibung varchar(400)
);
create table doit_projekt.rskf (
	niederschlagsform int1 primary key,
    beschreibung varchar(400)
);
create table doit_projekt.ftp_dateien 
	(dateinamen varchar(50) primary key not null);
create table doit_projekt.messungen (
    MESSUNG_ID varchar(16) primary key NOT null,
    STATIONS_ID int not null,
    MESS_DATUM date NOT null,
    QN_3 int(4) ,
    FX float(8),
    FM float(8),
    QN_4 int(4),
    RSK float(8),
    RSKF int(4),
    SDK float(8),
    SHK_TAG int(4),
    NM float(8),
    VPM float(8),
    PM float(8),
    TMK float(8),
    UPM float(8),
    TXK float(8),
    TNK float(8),
    TGK float(8)
);

insert into doit_projekt.rskf
		(niederschlagsform, beschreibung)
		value
		(0,'kein Niederschlag (konventionelleoder automatische Messung),entspricht WMO Code-Zahl 10'),
        (1,'nur Regen (in historischen Datenvor 1979)'),
        (4,'Form nicht bekannt, obwohlNiederschlag gemeldet'),
        (6,'nur Regen; flüssiger Niederschlagbei automatischen Stationen,entspricht WMO Code-Zahl 11'),
		(7,'nur Schnee; fester Niederschlagbei automatischen Stationen,entspricht WMO Code-Zahl 12'),
        (8,'Regen und Schnee (und/oder Schneeregen); flüssigerund fester Niederschlag beiautomatischen Stationen,entspricht WMO Code-Zahl 13'),
        (9,'fehlender Wert oderNiederschlagsform nichtfeststellbar bei automatischerMessung, entspricht WMO Code-Zahl 15');

insert into doit_projekt.messwerte_kennung
		(kennung_id, beschreibung)
		value
        ('AE','Stationen mit aerologischen Beobachtungen'),
        ('EB','Stationen mit täglichen Daten der Erdbodentemperaturmessungen'),
        ('FF','Stationen mit stündlichen Winddaten'),
        ('KL','Stationen mit Klimadaten'),
        ('MI','Stationen mit automatischen Messungen(10-Minuten-Auflösung)'),
        ('MM','Stationen mit automatischen Messungen(10-Minuten-Auflösung)'),
        ('PE','Stationen mit phänologischen Beobachtungen'),
        ('PS','Stationen mit phänologischen Beobachtungen'),
        ('RR','Stationen mit täglichen Niederschlagsdaten'),
        ('SO','Stationen mit stündlichen Daten der Sonnenscheindauer'),
        ('SY','Stationen mit stündlichen, automatischen Messungen (teilw. ergänzt mit Augenbeobachtungen, vor Einführung der Automaten nur Augenbeobachtungen)'),
        ('TU','Stationen mit stündlichen Daten der Temperatur undder relativen Feuchte');