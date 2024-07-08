import mysql.connector

# Verbindungsinformationen als Variablen speichern
MYSQL_ROOT_PASSWORD="my-secret-pw"
MYSQL_DATABASE="customer"
MYSQL_USER="root"
HOST='127.0.0.1'
TABLE_NAME='customer'

# Verbindung zur MySQL-Datenbank herstellen
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                               host=HOST, database=MYSQL_DATABASE)
c = conn.cursor()

# Daten aus der Tabelle lesen
select_query = f'SELECT * FROM {TABLE_NAME}'
c.execute(select_query)

# Alle Zeilen abrufen
rows = c.fetchall()

# Daten ausgeben
for row in rows:
    print(row)

# Typüberprüfung
print("Datentyp von rows:", type(rows))
if rows:
    print("Datentyp einer Zeile:", type(rows[0]))
    print("Datentyp eines Spaltenwerts (erste Spalte der ersten Zeile):", type(rows[0][0]))

# Verbindung schließen
conn.close()
