import mysql.connector 
from datetime import datetime
from decimal import *

# Variablen definieren
MYSQL_ROOT_PASSWORD="passwort"
MYSQL_DATABASE="scootech"
MYSQL_USER="root"
HOST='localhost'

# Verbindung zur Datenbank herstellen
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                              host=HOST, database=MYSQL_DATABASE)
c = conn.cursor()

def neuerKunde(vorname,nachname):
    c.execute(f'insert into kunde (vorname,nachname) values ("{vorname}","{nachname}");')
    conn.commit()

def neuerEscooter(standort,mietpreis_strecke,mietpreis_zeit):
    c.execute(f'insert into escooter (standort,mietpreis_strecke,mietpreis_zeit) values ("{standort}",{mietpreis_strecke},{mietpreis_zeit});')
    conn.commit()

def kundenAusgeben():
    select_query = 'SELECT * FROM kunde'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(row)

def escooterAusgeben():
    select_query = 'SELECT * FROM escooter'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(row)

def mietvorgängeAusgeben():
    select_query = 'SELECT * FROM mietvorgang'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(row)


def neuerKundeKonsole():
    vorname = input("Wie lautet der Vorname?")
    nachname = input("Wie lautet der Nachname?")
    neuerKunde(vorname,nachname)

def neuerEscooterKonsole():
    standort = input("Wo ist der Escooter?")
    mietpreis_strecke = input("Wie teuer pro Kilometer?")
    mietpreis_zeit = input("Wie teuer pro Minute?")
    neuerEscooter(standort,mietpreis_strecke,mietpreis_zeit)

def neuerMietvorgang():
    scooterID = input("Welche Scooter ID?")
    kundenname = input("Wie heißt du?")
    kundenID = 1
    bezahlart = input("Möchtest du pro Kilometer oder pro Minute bezahlen?")
    if bezahlart == "km":
        strecke = Decimal(input("Wie weit fährst du?"))
        startzeit = datetime.now()
        c.execute(f"select mietpreis_strecke from escooter where scooter_ID = {scooterID}")
        preis = c.fetchone()
        endpreis = round(preis[0] * strecke,2)
        c.execute(f'insert into mietvorgang(scooter_ID,kunden_ID,strecke,preis) values ({scooterID},{kundenID},{strecke},{endpreis})')
        conn.commit()
        


neuerMietvorgang()
mietvorgängeAusgeben()
#neuerEscooterKonsole()
#neuerKundeKonsole()
#neuerEscooter("Altona",0.30,4.50)
#neuerKunde("Luigi","Mario")
#escooterAusgeben()
#kundenAusgeben()
conn.close()