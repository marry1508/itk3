#!/usr/bin/env python3

import cgi
import cgitb
import mysql.connector

cgitb.enable()  # CGI-Fehlermeldungen aktivieren

# Verbindungsinformationen als Variablen speichern
MYSQL_ROOT_PASSWORD="my-secret-pw"
MYSQL_DATABASE="customer"
MYSQL_USER="root"
HOST='127.0.0.1'
TABLE_NAME='customer'

print("Content-Type: text/html\n")  # HTML-Header

# Formulardaten auslesen
form = cgi.FieldStorage()
customer_id = form.getvalue('customer_id')
new_age = form.getvalue('new_age')

if customer_id and new_age:
    # Verbindung zur MySQL-Datenbank herstellen
    conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                                   host=HOST, database=MYSQL_DATABASE)
    c = conn.cursor()

    # Datensatz aktualisieren
    update_query = f'UPDATE {TABLE_NAME} SET age = %s WHERE id = %s'
    c.execute(update_query, (new_age, customer_id))
    conn.commit()

    # Verbindung schließen
    conn.close()

    print(f'Datensatz für Benutzer-ID {customer_id} erfolgreich aktualisiert!')
else:
    print("Fehler: Benutzer-ID und neues Alter müssen angegeben werden.")
