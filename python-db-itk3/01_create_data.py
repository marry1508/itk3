import mysql.connector

MYSQL_ROOT_PASSWORD="my-secret-pw"
MYSQL_DATABASE="customer"
MYSQL_USER="root"
HOST='127.0.0.1'
TABLE_NAME='customer'

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, wenn sie nicht existiert)
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_ROOT_PASSWORD,
                              host=HOST,
                              database=MYSQL_DATABASE)
c = conn.cursor()


# Tabelle erstellen
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
'''
c.execute(create_table_query)

# Beispieldaten einfügen
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Alice', 30))
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Bob', 24))
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Charlie', 29))

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()
