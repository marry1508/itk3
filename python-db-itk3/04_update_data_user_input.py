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

# Benutzereingaben für das Update erhalten
customer_id = input("Geben Sie die ID des Benutzers ein, dessen Alter aktualisiert werden soll: ")
new_age = input("Geben Sie das neue Alter des Benutzers ein: ")

# Sicherstellen, dass die Eingaben in den richtigen Datentyp konvertiert werden
customer_id = int(customer_id)
new_age = int(new_age)

# Datensatz aktualisieren
update_query = f'UPDATE {TABLE_NAME} SET age = %s WHERE id = %s'
c.execute(update_query, (new_age, customer_id))

# Änderungen speichern
conn.commit()

# Bestätigen, dass der Datensatz aktualisiert wurde
c.execute(f'SELECT * FROM {TABLE_NAME} WHERE id = %s', (customer_id,))
updated_row = c.fetchone()
print("Aktualisierter Datensatz:", updated_row)

# Verbindung schließen
conn.close()
