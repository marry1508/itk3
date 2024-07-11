import mysql.connector 
from datetime import datetime
from decimal import *
from getpass import getpass
import os

# Variablen definieren
MYSQL_ROOT_PASSWORD="passwort" ########PASS ÄNDERN
MYSQL_DATABASE="scootech"
MYSQL_USER="root"
HOST='localhost'
ADMINPW = "admin"
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
    print("Would you like to create this account? y/n")
    if input() == "y":
        clear()
        neuerKunde(vorname,nachname,passwort)
        print("New account created!")
        print(f"Your customer ID is: {neuesterKundeID()}")
        warten()
    else:
        clear()
        print("Account creation cancelled!")
        warten()

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
        kundenIDs.append(str(ID[0]))
    return kundenIDs

# Gibt den Namen des aktiven Users aus der Datenbank aus
def nameAusDatenbank():
    c.execute(f"select vorname,nachname from kunde where kunden_ID = {kundennummer};")
    name = c.fetchone()
    name = name[0] + " " + name[1]
    return name


# Einen neuen E-Scooter in der Datenbank anlegen
def neuerEscooter(standort,mietpreis):
    c.execute(f'insert into escooter (standort,mietpreis) values ("{standort}",{mietpreis});')
    conn.commit()

# Einen neuen Escooter mit Eingaben aus der Konsole anlegen
def neuerEscooterKonsole():
    print("These are our current scooters:")
    escooterAusgeben()
    standort = input("Where is the scooter located? Input the city name: ") 
    mietpreis = input("Price per Minute? In EUR: ")
    print("Would you like to create this scooter? y/n")
    if input() == "y":
        clear()
        neuerEscooter(standort,mietpreis)
        print("New scooter added!")
    else:
        clear()
        print("Scooter creation cancelled!")


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
        scooterIDs.append(str(ID[0]))
    return scooterIDs

# Berechnet den Fahrpreis für gewünschten Scooter über die angebene Zeit und gibt diesen zurück
def fahrpreisberechnen():
    # Alle vorhandenen Scooter IDs in eine variable speichern
    alleIDs = alleScooterIDsListe()
    while True:
        # dem Benutzer alle vorhanden Scooter auf der Konsole anzeigen
        escooterAusgeben()
        # den Benutzer fragen, welche Scooter ID gewünscht ist
        scooterID = input("Please input the ScooterID or press 'x' to cancel: ")
        # Überprüfen, ob vom User eingegebene ID in der Liste aller IDs vorhanden ist
        if scooterID in alleIDs:
            # Wenn ID vorhanden ist, dann mit ID den Mietpreis vom entsprechenden Scooter aus Datenbank beziehen
            c.execute(f"select mietpreis from escooter where scooter_ID = {scooterID}")
            fahrpreis = c.fetchone()
            # Benutzer fragen, wie lange der Scooter genutzt werden soll
            while True:
                clear()
                try:
                    fahrzeit = input("How long would you like to use the scooter for? (in minutes) or press 'x' to cancel: ")
                    if fahrzeit == "x":
                        clear()
                        print("Calculation cancelled!")
                        return
                    fahrzeit = int(fahrzeit)
                    clear()
                    break
                except:
                    clear()
                    print("Please enter a valid number")
                    warten()
            # Endpreis berechnen und ausgeben
            preis = fahrpreis[0] * fahrzeit
            print(f"Your ride total for {fahrzeit} minutes would be {preis}€")
            return
            # Wenn ID nicht vorhanden ist, Fehlermeldung ausgeben
        elif scooterID == "x":
            clear()
            print("Calculation cancelled!")
            return        
        else:
            clear()
            print("ScooterID does not exist, please try again")
            warten()



# Legt einen neuen Mietvorgang in der Datenbank an      
def mietvorgangAnlegen():
    alleIDs = alleScooterIDsListe()
    while True:
        clear()
        escooterAusgeben()
        scooterID = input("Please input the ScooterID or type 'x' to cancel: ")
        if scooterID in alleIDs:
            startzeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(f"insert into mietvorgang(scooter_ID,kunden_ID,startzeit,abgeschlossen) values ({scooterID},{kundennummer},'{startzeit}',FALSE)")
            conn.commit()
            clear()
            print(f"New rental started. Your rental ID is: {neuesterMietvorgangID()}")
            warten()
            break
        elif scooterID == "x":
            clear()
            print("Rental cancelled.")
            warten()
            break
        else:
            clear()
            print("ScooterID does not exist, please try again")
            warten()


# Schließt einen Mietvorgang ab und berechnet den dazugehörigen Preis
def mietvorgangAbschließen():
    while True:
        clear()
        print("These are your currently active rentals:")
        aktiveMietvorgängeAusgeben()
        vorgangs_ID = input("Input your rental number or type 'x' to cancel: ")
        if vorgangs_ID in alleAktivenMietvorgangsIDsUser():
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
            break
        elif vorgangs_ID == "x":
            break
        else:
            clear()
            print("Invald Input, please try again")
            warten()

# Zeig alle aktiven Mietvorgänge an
def alleAktiveMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = FALSE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  Standort: {row[12]}  KundenID: {row[2]} Name: {row[8]} {row[9]}  Startzeit: {row[3]}")

# Zeigt alle aktiven Mietvorgänge vom aktiven User an
def aktiveMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = FALSE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  Standort: {row[12]}  Startzeit: {row[3]}")

# Gibt alle aktiven Mietvorgänge eines Users als Liste aus
def alleAktivenMietvorgangsIDsUser():
    c.execute(f"select mietvorgang.mietvorgang_ID from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = FALSE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    IDs = []
    for row in rows:
        IDs.append(str(row[0]))
    return IDs

# Zeig alle abgeschlossenen Mietvorgänge an
def alleAbgeschlosseneMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = TRUE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  Standort: {row[12]}  KundenID: {row[2]} Name: {row[8]} {row[9]}  Startzeit: {row[3]} Endzeit: {row[4]} Preis: {row[5]}€")

# Zeigt alle abeschlossenen Mietvorgänge vom aktiven User an
def abgeschlosseneMietvorgängeAusgeben():
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = TRUE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  Standort: {row[12]}  Startzeit: {row[3]} Endzeit: {row[4]} Preis: {row[5]}€")

# Gibt die Mietvorgang_ID des zuletzt angelegten Mietvorgangs zurück
def neuesterMietvorgangID():
    c.execute("select mietvorgang_ID from mietvorgang order by mietvorgang_ID desc limit 1;")
    ID = c.fetchone()
    return ID[0]

# Loggt den User ein
def einloggen():
    IDs = alleKundenIDsListe()
    kundenID = input("Please enter your Customer ID to Log in: ")
    if kundenID in IDs:
        #passwort abfragen
        c.execute(f"select passwort from kunde where kunden_ID = {kundenID}")
        passwortDB = c.fetchone()
        passwort = getpass()
        if passwort == passwortDB[0]:
            global kundennummer
            kundennummer = kundenID
            return True
        else:
            print("Invalid Password.")
            return False
    else:
        print("There is no Customer with this ID. Would you like to create a new Account? y/n: ")
        if input() == "y":
            clear()
            neuerKundeKonsole()
        return False

# Wartet auf User Input um nächstes Menu zu zeigen
def warten():
    input("Press enter to continue...")
    clear()

# Leert die console
def clear():
    os.system('cls')


clear()
while True:
    print("""Welcome to Scooteq! 
What would you like to do? Please input the corresponding number: 
    Log in to your account -  1
    Create a new account - 2
    Enter the administration console - 3
    End the program - x""")
    x = input()
    clear()
    if x == "1":
        login = einloggen()
        clear()
        if login == True:
            while True:
                print(f"""Welcome to Scooteq, {nameAusDatenbank()}!
What would you like to do? Please input the corresponding number: 
    Start a new Rental - 1
    End an active rental - 2
    Show your active rentals - 3
    Show past rentals - 4
    Calculate fare - 5
    Log out - x""")
                y = input()
                clear()
                if y == "1":
                    mietvorgangAnlegen()
                if y == "2":
                    mietvorgangAbschließen()
                    clear()
                if y == "3":
                    aktiveMietvorgängeAusgeben()
                    warten()
                if y == "4":
                    abgeschlosseneMietvorgängeAusgeben()
                    warten()
                if y == "5":
                    fahrpreisberechnen()
                    warten()
                # ausloggen
                if y == "x":
                    break
    elif x == "2":
        neuerKundeKonsole()
    elif x == "3":
        if getpass() == ADMINPW:
            while True:
                clear()
                print("""Hello boss! What would you like to do? 
Please input the corresponding number: 
    Add a new Scooter - 1
    Show all Scooters - 2
    Show all Users - 3
    Show all active rentals - 4
    Show all finished rentals - 5
    Leave administration console - x
                      """)
                y = input()
                clear()
                if y == "1":
                    neuerEscooterKonsole()
                    warten()
                if y == "2":
                    escooterAusgeben()
                    warten()
                if y == "3":
                    kundenAusgeben()
                    warten()
                if y == "4":
                    alleAktiveMietvorgängeAusgeben()
                    warten()
                if y == "5":
                    alleAbgeschlosseneMietvorgängeAusgeben()
                    warten()
                if y == "x":
                    break
    elif x == "x":
        break


# Verbindung zur Datenbank schließen
conn.close()