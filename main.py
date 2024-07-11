import mysql.connector 
from datetime import datetime
from decimal import *
from getpass import getpass

# Variablen definieren
MYSQL_ROOT_PASSWORD="passwort" ########PASS ÄNDERN
MYSQL_DATABASE="scootech"
MYSQL_USER="root"
HOST='localhost'
kundennummer = 0

# Verbindung zur Datenbank herstellen
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                              host=HOST, database=MYSQL_DATABASE)
c = conn.cursor()

# Einen neuen Kunden in der Datenbank anlegen
def neuerKunde(vorname,nachname,passwort):
    c.execute(f'insert into kunde (vorname,nachname,passwort) values ("{vorname}","{nachname}","{passwort}");')
    conn.commit()

# Einen neuen Kunden mit Eingaben aus der Konsole anlegen
def neuerKundeKonsole():
    vorname = input("What is your first name? ")
    nachname = input("What is your last name? ")
    passwort = getpass("Input your Password: ")
    neuerKunde(vorname,nachname,passwort)
    print("\nNew customer created!\n")

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

# Gibt die KundenID des zuletzt angelegten Kunden zurück
def neuesterKundeID():
    c.execute("select kunden_ID from kunde order by kunden_ID desc limit 1;")
    ID = c.fetchone()
    return ID[0]

# Gibt alle KundenIDs als Liste aus
def alleKundenIDsListe():
    c.execute("Select kunden_ID from kunde")
    alleIDs = c.fetchall()
    kundenIDs = []
    for ID in alleIDs:
        kundenIDs.append(ID[0])
    return kundenIDs

def nameAusDatenbank():
    c.execute(f"select vorname,nachname from kunde where kunden_ID = {kundennummer};")
    name = c.fetchone()
    name = name[0] + " " + name[1]
    return name


# Einen neuen Escooter in der Datenbank anlegen
def neuerEscooter(standort,mietpreis):
    c.execute(f'insert into escooter (standort,mietpreis) values ("{standort}",{mietpreis});')
    conn.commit()

# Einen neuen Escooter mit Eingaben aus der Konsole anlegen
def neuerEscooterKonsole():
    standort = input("Where is the scooter located? Input the city name: ") #viell. noch dynamisch die Städte anzeigen
    mietpreis = input("Price per Minute? In EUR: ")
    neuerEscooter(standort,mietpreis)
    print("\nNew scooter added!\n")

# Zeigt alle Escooter aus der Datenbank auf der Konsole an
def escooterAusgeben():
    select_query = 'SELECT * FROM escooter'
    c.execute(select_query)

    # Alle Zeilen abrufen
    rows = c.fetchall()

    # Daten ausgeben
    for row in rows:
        print(f"ScooterID: {row[0]}  Standort: {row[1]}  Preis : {row[2]}€")
    print()

# Liest alle ScooterIDs aus der Datenbank aus und gibt eine Liste mit diesen aus
def alleScooterIDsListe():
    c.execute("Select scooter_ID from escooter")
    alleIDs = c.fetchall()
    scooterIDs = []
    for ID in alleIDs:
        scooterIDs.append(ID[0])
    return scooterIDs

# Berechnet den Fahrpreis für gewünschten Scooter über die angebene Zeit und gibt diesen zurück
def fahrpreisberechnen():
    # Alle vorhandenen Scooter IDs in eine variable speichern

        # dem Benutzer alle vorhanden Scooter auf der Konsole anzeigen

        # den Benutzer fragen, welche Scooter ID gewünscht ist

        # Überprüfen, ob gegebene ID in der Liste aller IDs vorhanden ist

            # Wenn ID vorhanden ist, dann mit ID den Mietpreis vom entsprechenden Scooter aus Datenbank beziehen

            # Benutzer fragen, wie lange der Scooter genutzt werden soll

            # Endpreis berechnen und ausgeben
            return
            # Wenn ID nicht vorhanden ist, Fehlermeldung ausgeben

    

def fahrpreisBerechnenAlt():
    scooterID = input("Input ScooterID: ")
    c.execute(f"select mietpreis from escooter where scooter_ID = {scooterID}")
    preis = c.fetchone()
    zeit = Decimal(input("How long would you like to rent the scooter for? "))
    return round(preis[0] * zeit,2)


# Bruahcen wir wahrschienlich nicht mehr
# Startet das anlegen eines neuen Mietvorgangs
def neuerMietvorgang():
    c.execute("Select kunden_ID from kunde")
    alleIDs = c.fetchall()
    kundenIDs = []
    for ID in alleIDs:
        kundenIDs.append(ID[0])
    while True:
        kundenID = int(input("Please input your CustomerID: "))
        # Kunden ID ist vorhanden
        if kundenID in kundenIDs:
            mietvorgangAnlegen(kundenID)
            print("Mietvorgang angelegt")
            break
        else:
            print("The customer ID is not in our Database. Do you want to create a new User? y/n")
            x = input()
            if x == "y":
                neuerKundeKonsole()
                mietvorgangAnlegen(neuesterKundeID())
                break


# Legt einen neuen Mietvorgang in der Datenbank an      
def mietvorgangAnlegen():
    alleIDs = alleScooterIDsListe()
    while True:
        escooterAusgeben()
        scooterID = int(input("Please input the ScooterID: "))
        if scooterID in alleIDs:
            startzeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(f"insert into mietvorgang(scooter_ID,kunden_ID,startzeit,abgeschlossen) values ({scooterID},{kundennummer},'{startzeit}',FALSE)")
            conn.commit()
            break
        else:
            print("ScooterID does not exist, please try again")


# Schließt einen Mietvorgang ab und berechnet den dazugehörigen Preis
def mietvorgangAbschließen():
    vorgangs_ID = input("What is you rental number? ")
    c.execute(f"select startzeit from mietvorgang where mietvorgang_ID = {vorgangs_ID}")
    startzeit = c.fetchone()
    endzeit = datetime.now()
    zeitdifferenz = endzeit - startzeit[0]
    zeitdifferenz = round(zeitdifferenz.total_seconds() / 60)
    c.execute(f"SELECT escooter.mietpreis from mietvorgang join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.mietvorgang_ID = {vorgangs_ID}")
    minutenpreis = c.fetchone()
    preis = zeitdifferenz * minutenpreis[0]
    c.execute(f"update mietvorgang set abgeschlossen = TRUE,endzeit = '{endzeit}',preis = {preis} where mietvorgang_ID = {vorgangs_ID}")
    conn.commit()

# Zeig alle aktiven Mietvorgänge an
def alleAktiveMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = FALSE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  ScooterID: {row[1]}  KundenID: {row[2]} Name: {row[8]} {row[9]}  Startzeit: {row[3]}")

# Zeigt alle aktiven Mietvorgänge vom aktiven User an
def aktiveMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = FALSE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  ScooterID: {row[1]}  Startzeit: {row[3]}")

# Zeig alle abgeschlossenen Mietvorgänge an
def alleAbgeschlosseneMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = TRUE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  ScooterID: {row[1]}  KundenID: {row[2]} Name: {row[8]} {row[9]}  Startzeit: {row[3]} Endzeit: {row[4]} Preis: {row[5]}€")

# Zeigt alle abeschlossenen Mietvorgänge vom aktiven User an
def abgeschlosseneMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = TRUE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  ScooterID: {row[1]}  Startzeit: {row[3]} Endzeit: {row[4]} Preis: {row[5]}€")

# Loggt den User ein
def einloggen():
    IDs = alleKundenIDsListe()
    kundenID = int(input("Please enter your Customer ID to Log in: "))
    if kundenID in IDs:
        #passwort abfragen
        c.execute(f"select passwort from kunde where kunden_ID = {kundenID}")
        passwortDB = c.fetchone()
        passwort = getpass()
        if passwort == passwortDB[0]:
            print("erfolgreich eingeloggt")
            global kundennummer
            kundennummer = kundenID
            return True
        else:
            print("Invalid Password")
            return False
    else:
        print("There is no Customer with this ID. Do you want to create a new Account? y/n")
        if input() == "y":
            neuerKundeKonsole()
        return False

""""
# Schleife zum abfragen aller vom User gewünschten Eingaben
while True:
    print('''Welcome to Scooteq! What would you like to do? Please input the corresponding number: 
              Calculate fare - 1                
              Add a new customer - 2
              Add a new scooter - 3
              Start a new rental - 4
              End program - 5''') #6,7 noch hinzufügen
    x = input()
    if x == "1":
        print(f"{fahrpreisBerechnenAlt()}€")
    elif x == "2":
        neuerKundeKonsole()
    elif x == "3":
        neuerEscooterKonsole()
    elif x == "4":
        neuerMietvorgang()
    elif x == "5":
        break
    elif x == "6":
        aktiveMietvorgängeAusgeben()
        abgeschlosseneMietvorgängeAusgeben()
    elif x == "7":
        kundenAusgeben()
        escooterAusgeben()
    elif x == "8":
        mietvorgangAbschließen()
    elif x == "9":
        einloggen()
        print(kundennummer)
    else:
        print("Invalid entry. Please try again.")
"""

while True:
    print("""Willkommen bei scootech
          Einloggen 1
          neuer account 2
          admin shit 3
          beenden 4""")
    x = input()
    if x == "1":
        login = einloggen()
        if login == True:
            print(f"Hallo {nameAusDatenbank()}")
            while True:
                print("Was willst du tun?")
                y = input()
                if y == "1":
                    mietvorgangAnlegen()
                if y == "2":
                    mietvorgangAbschließen()
                if y == "3":
                    aktiveMietvorgängeAusgeben()
                if y == "4":
                    abgeschlosseneMietvorgängeAusgeben()
                if y == "5":
                    fahrpreisberechnen()
                # ausloggen
                if y == "6":
                    break
        # noch mehr shit muss passieren danach
    elif x == "2":
        neuerKundeKonsole()
    elif x == "3":
        # admin menu
        neuerEscooterKonsole()
    elif x == "4":
        break





# Ab hier random Befehle zum Testen von Dingen, nicht direkt relevant

#print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    

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