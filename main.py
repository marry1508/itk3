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
ADMINPW = "admin"   #Passwort für die Adminkonsole
kundennummer = 0    #Kundennummer des aktiven Users


# Verbindung zur Datenbank herstellen
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                              host=HOST, database=MYSQL_DATABASE)
c = conn.cursor()


# Einen neuen Kunden in der Datenbank anlegen
def neuerKunde(vorname,nachname,passwort):
    # Übergebene Daten in die Datenbank schreiben
    c.execute(f'insert into kunde (vorname,nachname,passwort) values ("{vorname}","{nachname}","{passwort}");')
    conn.commit()


# Einen neuen Kunden mit Eingaben aus der Konsole anlegen
def neuerKundeKonsole():
    # Daten für Accounterstellung abfragen
    vorname = input("What is your first name? ")
    nachname = input("What is your last name? ")
    passwort = getpass("Input your Password: ")
    # Bestätigung für Accounterstellung
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
    # Kunden aus Datenbank abrufen
    c.execute('SELECT * FROM kunde')
    rows = c.fetchall()
    # Kunden auf Konsole ausgeben
    for row in rows:
        print(f"KundenID: {row[0]}  Name: {row[1]} {row[2]}")
    print()


# Gibt die KundenID des zuletzt angelegten Kunden zurück
def neuesterKundeID():
    # Höchste KundenID aus Datenbank abfragen und ausgeben
    c.execute("select kunden_ID from kunde order by kunden_ID desc limit 1;")
    ID = c.fetchone()
    return ID[0]


# Gibt alle KundenIDs als Liste aus
def alleKundenIDsListe():
    # Alle KundenIDs aus Datenbank ausgeben lassen
    c.execute("Select kunden_ID from kunde")
    alleIDs = c.fetchall()
    # KundenIDs in eine Liste schreiben, damit mit Daten weitergearbeitet werden kann und anschließend ausgeben
    kundenIDs = []
    for ID in alleIDs:
        kundenIDs.append(str(ID[0]))
    return kundenIDs


# Ändert den Vornamen des Aktiven Benutzers
def vornamenAnpassen():
    clear()
    firstname = input("Please enter your new first name: ")
    clear()
    print(f"Is the name {firstname} correct? y/n")
    x  = input()
    if x == "y":
        c.execute(f"update kunde set vorname = '{firstname}' where kunden_ID = {kundennummer}")
        conn.commit()
        clear()
        print("First name updated!")
        warten()
    else:
        clear()
        print("Update cancelled.")
        warten()


# Ändert den Nachnamen des aktiven Benutzers
def nachnamenAnpassen():
    clear()
    lastname = input("Please enter your new last name: ")
    clear()
    print(f"Is the name {lastname} correct? y/n")
    x  = input()
    if x == "y":
        c.execute(f"update kunde set nachname = '{lastname}' where kunden_ID = {kundennummer}")
        conn.commit()
        clear()
        print("Last name updated!")
        warten()
    else:
        clear()
        print("Update cancelled.")
        warten()


# Ändert das Passwort des aktiven Benutzers
def passwordAnpassen():
    clear()
    c.execute(f"select passwort from kunde where kunden_ID = {kundennummer}")
    passwortDB = c.fetchone()
    passwort = getpass("Please enter your password before you can continue")
    if passwort == passwortDB[0]:
        clear()
        newPasswort = getpass("Please enter your new password: ")
        newPasswort2 = getpass("Please enter your new password again: ")
        if newPasswort == newPasswort2:
            c.execute(f"update kunde set passwort = '{newPasswort}' where kunden_ID = {kundennummer}")
            conn.commit()
            clear()
            print("Password updated!")
            warten()
        



# Gibt den Namen des aktiven Users aus der Datenbank aus
def nameAusDatenbank():
    # Vor und Nachame des aktiven Users aus Datenbank abfragen
    c.execute(f"select vorname,nachname from kunde where kunden_ID = {kundennummer};")
    name = c.fetchone()
    # Name zusammenbauen und zurückgeben
    name = name[0] + " " + name[1]
    return name


# Einen neuen E-Scooter in der Datenbank anlegen
def neuerEscooter(standort,mietpreis):
    # Übergebene Daten in die Datenbank schreiben
    c.execute(f'insert into escooter (standort,mietpreis) values ("{standort}",{mietpreis});')
    conn.commit()


# Einen neuen Escooter mit Eingaben aus der Konsole anlegen
def neuerEscooterKonsole():
    # Alle vorhanden Escooter anzeigen
    print("These are our current scooters:")
    escooterAusgeben()
    # Daten für den neuen Escooter abfragen
    standort = input("Where is the scooter located? Input the district: ") 
    mietpreis = input("Price per minute? In EUR: ")
    # Bestätigung für Scootererstellung
    print("Would you like to create this scooter? y/n")
    if input() == "y":
        clear()
        neuerEscooter(standort,mietpreis)
        print("New scooter added")
    else:
        clear()
        print("Scooter creation cancelled!")


# Zeigt alle Escooter aus der Datenbank auf der Konsole an
def escooterAusgeben():
    # Alle Escooter aus Datenbank abfragen
    c.execute('SELECT * FROM escooter')
    rows = c.fetchall()
    # Escooter auf Konsole anzeigen
    for row in rows:
        print(f"ScooterID: {row[0]}  Standort: {row[1]}  Preis : {row[2]}€")
    print()


# Liest alle ScooterIDs aus der Datenbank aus und gibt eine Liste mit diesen aus
def alleScooterIDsListe():
    # Alle ScooterIDs aus der Datenbank abfragen
    c.execute("Select scooter_ID from escooter")
    alleIDs = c.fetchall()
    # ScooterIDs in eine Liste schreiben, damit mit Daten weitergearbeitet werden kann und anschließend ausgeben
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
        scooterID = input("Please input the scooter ID or press 'x' to cancel: ")
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
                    # Prüfen, ob Funktion beendet werden soll
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
        # Prüfen, ob Funktion beendet werden soll
        elif scooterID == "x":
            clear()
            print("Calculation cancelled!")
            return        
        # Wenn ID nicht vorhanden ist, Fehlermeldung ausgeben
        else:
            clear()
            print("ScooterID does not exist, please try again")
            warten()


# Legt einen neuen Mietvorgang in der Datenbank an      
def mietvorgangAnlegen():
    # Alle Vorhanden ScooterIDs in eine Variable schreiben
    alleIDs = alleScooterIDsListe()
    while True:
        # Alle vorhanden Escooter ausgeben
        clear()
        escooterAusgeben()
        # Abfragen, welchen Escooter der Kunde Nutzen will
        scooterID = input("Please input the ScooterID or type 'x' to cancel: ")
        # Prüfen, ob angegebene ScooterID in Liste mit allen IDs vorhanden ist
        if scooterID in alleIDs:
            # Startzeit bestimmen und neuen Mietvorgang in der Datenbank anlegen
            startzeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(f"insert into mietvorgang(scooter_ID,kunden_ID,startzeit,abgeschlossen) values ({scooterID},{kundennummer},'{startzeit}',FALSE)")
            conn.commit()
            clear()
            print(f"New rental started. Your rental ID is: {neuesterMietvorgangID()}")
            warten()
            break
        # Funktion bei Eingabe von x beenden
        elif scooterID == "x":
            clear()
            print("Rental cancelled.")
            warten()
            return
        # Meldung für falsche Eingabe
        else:
            clear()
            print("ScooterID does not exist, please try again!")
            warten()


# Schließt einen Mietvorgang ab und berechnet den dazugehörigen Preis
def mietvorgangAbschließen():
    while True:
        # Alle aktiven Mietvorgänge anzeigen lassen
        clear()
        print("These are your currently active rentals:")
        aktiveMietvorgängeAusgeben()
        # Abfragen, welcher Mietvorgang beendet werden soll
        vorgangs_ID = input("Input your rental number or type 'x' to cancel: ")
        # Prüfen, ob angegebene ID zu aktivem User gehört
        if vorgangs_ID in alleAktivenMietvorgangsIDsUser():
            # Startzeit aus Datenbank ziehen, Endzeit festlegen und Zeitdifferenz errechnen
            c.execute(f"select startzeit from mietvorgang where mietvorgang_ID = {vorgangs_ID}")
            startzeit = c.fetchone()
            endzeit = datetime.now()
            zeitdifferenz = endzeit - startzeit[0]
            zeitdifferenz = round(zeitdifferenz.total_seconds() / 60)
            # Mietpreis des zum Mietvorgang zugeordneten Escooters aus Datenbank ziehen
            c.execute(f"SELECT escooter.mietpreis from mietvorgang join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.mietvorgang_ID = {vorgangs_ID}")
            minutenpreis = c.fetchone()
            # Mietpreis berechnen und Mietvorgang aktualisieren
            preis = zeitdifferenz * minutenpreis[0]
            c.execute(f"update mietvorgang set abgeschlossen = TRUE,endzeit = '{endzeit}',preis = {preis} where mietvorgang_ID = {vorgangs_ID}")
            conn.commit()
            break
        # Funktion abbrechen
        elif vorgangs_ID == "x":
            return
        # Fehlermeldung bei Falscher Benutzereingabe
        else:
            clear()
            print("Invald Input, please try again!")
            warten()


# Zeig alle aktiven Mietvorgänge an
def alleAktiveMietvorgängeAusgeben():
    # Alle aktiven Mietvorgänge von alle Benutzern aus Datenbank holen
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = FALSE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    # Alle aus der Datenbank geholten Einträge auf der Konsole anzeigen lassen
    for row in rows:
        print(f"ID: {row[0]}  Location: {row[12]}  Customer ID: {row[2]} Name: {row[8]} {row[9]}  Start time: {row[3]}")


# Zeigt alle aktiven Mietvorgänge vom aktiven User an
def aktiveMietvorgängeAusgeben():
    # Alle aktiven Mietvorgänge des aktiven Users aus der Datenbank holen
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = FALSE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    # Alle aus der Datenbank geholten Einträge auf der Konsole anzeigen lassen
    for row in rows:
        print(f"ID: {row[0]}  Location: {row[12]}  Start time: {row[3]}")


# Gibt alle aktiven Mietvorgänge eines Users als Liste aus
def alleAktivenMietvorgangsIDsUser():
    # Alle IDs der aktiven Mietvorgänge des aktiven Users aus der Datenbank holen
    c.execute(f"select mietvorgang.mietvorgang_ID from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID where mietvorgang.abgeschlossen = FALSE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    # Alle aus Datenbank geholten IDs in eine Liste schreiben und zurückgeben
    IDs = []
    for row in rows:
        IDs.append(str(row[0]))
    return IDs


# Zeig alle abgeschlossenen Mietvorgänge an
def alleAbgeschlosseneMietvorgängeAusgeben():
    # Alle abgeschlossen Mietvorgänge von alle Usern aus Datenbank holen
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = TRUE order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    # Alle aus Datenbank geholten Einträge auf der Konsole anzeigen
    for row in rows:
        print(f"ID: {row[0]}  Location: {row[12]}  Customer ID: {row[2]} Name: {row[8]} {row[9]}  Start time: {row[3]} End time: {row[4]} Price: {row[5]}€")


# Zeigt alle abeschlossenen Mietvorgänge vom aktiven User an
def abgeschlosseneMietvorgängeAusgeben():
    # Alle abgeschlossenen Mietvorgänge des aktiven Benutzers auf der Konsole anzeigen lassen
    c.execute(f"select * from mietvorgang join kunde on kunde.kunden_ID = mietvorgang.kunden_ID join escooter on escooter.scooter_ID = mietvorgang.scooter_ID where mietvorgang.abgeschlossen = TRUE and kunde.kunden_ID = {kundennummer} order by mietvorgang.mietvorgang_ID asc")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}  Location: {row[12]}  Start time: {row[3]} End time: {row[4]} Price: {row[5]}€")


# Gibt die Mietvorgang_ID des zuletzt angelegten Mietvorgangs zurück
def neuesterMietvorgangID():
    # ID des Mietvorgang mit der höchsten ID aus der Datenbank holen und zurückgeben
    c.execute("select mietvorgang_ID from mietvorgang order by mietvorgang_ID desc limit 1;")
    ID = c.fetchone()
    return ID[0]


# Loggt den User ein
def einloggen():
    # KundenID des Benutzers abfragen
    kundenID = input("Please enter your customer ID to Log in: ")
    if kundenID in alleKundenIDsListe():
        # Bei Vorhandener ID passwort abfragen
        c.execute(f"select passwort from kunde where kunden_ID = {kundenID}")
        passwortDB = c.fetchone()
        passwort = getpass()
        if passwort == passwortDB[0]:
            global kundennummer
            kundennummer = kundenID
            return True
        else:
            print("Invalid password!")
            return False
    # Frage, ob neuer Account erstellt werden soll, wenn keine zu Customer ID kein Account existiert
    else:
        print("There is no account with this Customer ID. Would you like to create a new account? y/n: ")
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


# Main menu
def mainMenu():
    clear()
    while True:
    # Schreibt Menu auf die Konsole
        print("""Welcome to Scooteq! 
What would you like to do? Please input the corresponding number: 
    Log in to your account -  1
    Create a new account - 2
    Enter the administration console - 3
    End the program - x""")
        # Menuauswahl von User abfragen
        x = input()
        clear()
        if x == "1":
            userMenu()
        # Startet das Anlegen eines neuen Benutzers
        elif x == "2":
            neuerKundeKonsole()
        # Öffnet das Adminmenu
        elif x == "3":
            adminMenu()
        # Beendet die Verbindung zur Datenbank und das Programm
        elif x == "x":
            conn.close()
            break


# User Menu
def userMenu():
    # Login Funktion ausführen
    login = einloggen()
    clear()
    # Öffnet User Menu bei erfolgreichem Login
    if login == True:
        while True:
            # Schreibt nächstes Menu auf die Konsole
            print(f"""Welcome to Scooteq, {nameAusDatenbank()}!
What would you like to do? Please input the corresponding number: 
    Start a new rental - 1
    End an active rental - 2
    Show your active rentals - 3
    Show past rentals - 4
    Calculate fare - 5
    Account settings - 6
    Log out - x""")
            # Menuauswahl vom User abfragen
            x = input()
            clear()
            # Startet die Anlage eines neuen Mietvorgangs mit dem aktiven Benutzer
            if x == "1":
                mietvorgangAnlegen()
            # Startet des Beenden eines Mietvorgangs mit dem aktiven Benutzer
            if x == "2":
                mietvorgangAbschließen()
                clear()
            # Startet das Anzeigen aller aktiven Mietvorgänge des aktiven Benutzers
            if x == "3":
                aktiveMietvorgängeAusgeben()
                warten()
            # Startet das Anzeigen aller abgeschlossenen Mietvorgänge des Benutzers
            if x == "4":
                abgeschlosseneMietvorgängeAusgeben()
                warten()
            # Startet die Berechnung eines Fahrpreises
            if x == "5":
                fahrpreisberechnen()
                warten()
            if x == "6":
                accountSettings()
            # Loggt den aktiven User aus
            if x == "x":
                break


# Account Settings
def accountSettings():
    while True:
        clear()
        print("""Account settings
What would you like to do? Please input the corresponding number: 
    Change first name - 1
    Change last name - 2
    Change password - 3
    Back - x""")
        x = input()
        if x == "1":
            vornamenAnpassen()
        if x == "2":
            nachnamenAnpassen()
        if x == "3":
            passwordAnpassen()
        if x == "x":
            clear()
        break


# Admin Menu
def adminMenu():
    # Fragt das Adminpasswort ab
    if getpass() == ADMINPW:
        while True:
            # Zeigt das Menu der Adminkonsole an
            clear()
            print("""Hello boss! What would you like to do? 
Please input the corresponding number: 
    Add a new scooter - 1
    Show all scooters - 2
    Show all users - 3
    Show all active rentals - 4
    Show all finished rentals - 5
    Leave administration console - x""")
            # Menuauswahl vom User abfragen
            x = input()
            clear()
            # Startet das Anlegen eines neuen Escooters 
            if x == "1":
                neuerEscooterKonsole()
                warten()
            # Startet das Anzeigen einer Liste mit allen Escootern
            if x == "2":
                escooterAusgeben()
                warten()
            # Startet das Anzeigen einer Liste mit allen Useraccounts
            if x == "3":
                kundenAusgeben()
                warten()
            # Startet das Anzeigen einer Liste mit allen aktiven Mietvorgängen
            if x == "4":
                alleAktiveMietvorgängeAusgeben()
                warten()
            # Startet das Anzeigen einer Liste mit allen abgeschlossenen Mietvorgängen
            if x == "5":
                alleAbgeschlosseneMietvorgängeAusgeben()
                warten()
            # Loggt aus der Adminkonsole aus
            if x == "x":
                break


# Programm fängt ab hier an
mainMenu()