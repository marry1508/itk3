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

# Einen neuen Kunden in der Datenbank anlegen
def neuerKunde(vorname,nachname):
    c.execute(f'insert into kunde (vorname,nachname) values ("{vorname}","{nachname}");')
    conn.commit()

# Einen neuen Escooter in der Datenbank anlegen
def neuerEscooter(standort,mietpreis_strecke,mietpreis_zeit):
    c.execute(f'insert into escooter (standort,mietpreis_strecke,mietpreis_zeit) values ("{standort}",{mietpreis_strecke},{mietpreis_zeit});')
    conn.commit()

# Alle Kundeneinträge aus der Datenbank ausgeben
def kundenAusgeben():
    select_query = 'SELECT * FROM kunde'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(f"KundenID: {row[0]}  Name: {row[1]} {row[2]}")
    print()

# Alle Escootereinträge aus der Datenbank ausgeben
def escooterAusgeben():
    select_query = 'SELECT * FROM escooter'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(f"ScooterID: {row[0]}  Standort: {row[1]}  Preis pro Minute: {row[2]}€  Preis pro km: {row[3]}€")
    print()

# Alle Mietvorgänge aus der Datenbank ausgeben
def mietvorgängeAusgeben():
    select_query = 'SELECT * FROM mietvorgang'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(f"ID: {row[0]}  ScooterID: {row[1]}  KundenID: {row[2]} Startzeit: {row[3]}  Endzeit: {row[4]}  Strecke: {row[5]}km  Preis: {row[6]}€")

# Einen neuen Kunden mit Eingaben aus der Konsole anlegen
def neuerKundeKonsole():
    vorname = input("Wie lautet der Vorname?")
    nachname = input("Wie lautet der Nachname?")
    neuerKunde(vorname,nachname)

# Einen neuen Escooter mit Eingaben aus der Konsole anlegen
def neuerEscooterKonsole():
    standort = input("Wo ist der Escooter?")
    mietpreis_strecke = input("Wie teuer pro Kilometer?")
    mietpreis_zeit = input("Wie teuer pro Minute?")
    neuerEscooter(standort,mietpreis_strecke,mietpreis_zeit)

# Einen neuen Mietvorgang in der Datenbank anlegen
def neuerMietvorgang():
    scooterID = input("Welche Scooter ID?")
    kundenID = input("Wie lautet deine KundenID?")
    # Aktuelles Datum + Uhrzeit in Variable speichern und für Datenbank passend formatieren
    startzeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while True:
        bezahlart = input("Möchtest du pro Kilometer oder pro Minute bezahlen?")
        # Je nach gewünschter Bezahlart den entsprechenden Preis berechnen und Mietvorgang in die Datenbank eintragen
        if bezahlart == "km":
            strecke = Decimal(input("Wie weit fährst du?"))
            c.execute(f"select mietpreis_strecke from escooter where scooter_ID = {scooterID}")
            preis = c.fetchone()
            endpreis = round(preis[0] * strecke,2)
            c.execute(f'insert into mietvorgang(scooter_ID,kunden_ID,strecke,preis,startzeit) values ({scooterID},{kundenID},{strecke},{endpreis},"{startzeit}")')
            conn.commit()
            break
        elif bezahlart == "min":
            c.execute(f"select mietpreis_zeit from escooter where scooter_ID = {scooterID}")
            preis = c.fetchone()
            zeit = Decimal(input("Wie lange möchtest du den Scooter mieten?"))
            endpreis = round(preis[0] * zeit,2)
            c.execute(f'insert into mietvorgang(scooter_ID,kunden_ID,preis,startzeit) values ({scooterID},{kundenID},{endpreis},"{startzeit}")')
            conn.commit()
            break
        else:
            print("Falsche Eingabe")


# Schleife zum abfragen aller vom User gewünschten Eingaben
while True:
    print('''Was möchtest du machen?
              Neuen Kunden anlegen - 1
              Neuen Escooter anlegen - 2
              Neuen Mietvorgang anlegen - 3
              Beenden - 4''')
    x = input()
    if x == "1":
        neuerEscooterKonsole()
    elif x == "2":
        neuerEscooterKonsole()
    elif x == "3":
        neuerMietvorgang()
    elif x == "4":
        break
    elif x == "5":
        mietvorgängeAusgeben()
    elif x == "6":
        kundenAusgeben()
        escooterAusgeben()
    else:
        print("Ungueltige Eingabe")

# Ab hier random Befehle zum Testen von Dingen, nicht direkt relevant

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    

#neuerMietvorgang()
#mietvorgängeAusgeben()
#neuerEscooterKonsole()
#neuerKundeKonsole()
#neuerEscooter("Altona",0.30,4.50)
#neuerKunde("Luigi","Mario")
#escooterAusgeben()
#kundenAusgeben()

# Verbindung zur Datenbank schließen
conn.close()