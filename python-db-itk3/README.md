# Update Customer Age

This project consists of various Python scripts and HTML files that allow you to create, read, and update customer data in a MySQL database. It includes a CGI script to interact with the customer data via an HTML form.

## Directory Structure

```
/your-directory
    /cgi-bin
        update_customer_cgi.py
    /templates
        form.html
    01_create_data.py
    02_read_data.py
    03_update_data.py
    04_update_data_user_input.py
    05_update_customer_cgi.py
    start_database.sh
```

## Requirements

- Python 3.x
- MySQL Server
- MySQL Connector for Python

## Installation

##

### Install MySQL Connector

```sh
pip install mysql-connector-python
```

## Files and Their Usage

### 1. Create Database and Tables

**File:** `01_create_data.py`

This script creates the MySQL database and the `customer` table.

**Detailed Explanation:**

```python
import mysql.connector

# MySQL connection details
MYSQL_ROOT_PASSWORD="my-secret-pw"
MYSQL_DATABASE="customer"
MYSQL_USER="root"
HOST='127.0.0.1'
TABLE_NAME='customer'

# Establish connection to the MySQL database
conn = mysql.connector.connect(
    user=MYSQL_USER, 
    password=MYSQL_ROOT_PASSWORD,
    host=HOST,
    database=MYSQL_DATABASE
)
c = conn.cursor()

# SQL query to create the table if it doesn't already exist
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
'''
c.execute(create_table_query)

# Insert sample data into the table
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Alice', 30))
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Bob', 24))
c.execute('INSERT INTO customer (name, age) VALUES (%s, %s)', ('Charlie', 29))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
```

**Execution:**

```sh
python 01_create_data.py
```

**Explanation:**

1. **Importing mysql.connector:**
   The script imports the `mysql.connector` module, which is used to connect to and interact with the MySQL database.

2. **MySQL Connection Details:**
   The script defines the connection details for the MySQL database, including the root password, database name, user, host, and table name.

3. **Establish Connection:**
   The script establishes a connection to the MySQL database using the specified connection details.

4. **Create Table Query:**
   The script defines an SQL query to create a table named `customer` if it does not already exist. The table has three columns:
   - `id`: An integer that auto-increments and serves as the primary key.
   - `name`: A varchar field to store the customer's name.
   - `age`: An integer to store the customer's age.

5. **Execute Create Table Query:**
   The script executes the create table query using the cursor object.

6. **Insert Sample Data:**
   The script inserts three sample records into the `customer` table:
   - Alice, age 30
   - Bob, age 24
   - Charlie, age 29

7. **Commit Changes:**
   The script commits the changes to the database to ensure the data is saved.

8. **Close Connection:**
   Finally, the script closes the connection to the database.

### 2. Read Data from the Database

**File:** `02_read_data.py`

This script reads the data from the `customer` table and prints it to the console.

**Execution:**

```sh
python 02_read_data.py
```

### 3. Update Data in the Database

**File:** `03_update_data.py`

This script updates the age of a customer in the `customer` table based on the customer ID.

**Execution:**

```sh
python 03_update_data.py
```

### 4. Database Update with User Input

**File:** `04_update_data_user_input.py`

This script prompts the user to enter a customer ID and a new age, and then updates the data in the database.

**Execution:**

```sh
python 04_update_data_user_input.py
```

### 5. HTML Form for Updating Data

**File:** `05_html_form.html`

This HTML file contains a form that allows the user to enter the ID and new age of a customer. Place this file in the `templates` directory.

### 6. CGI Script for Updating Data

**File:** `05_update_customer_cgi.py`

This CGI script processes the form data and updates the data in the `customer` table.

### 7. Start the Database

**File:** `start_database.sh`

A shell script to start the MySQL database server. This is used for Docker.

**Execution:**

```sh
bash start_database.sh
```

## Usage

### Run the CGI Script

1. **Make sure the CGI script is executable:**
   ```sh
   chmod +x cgi-bin/update_customer_cgi.py
   ```

2. **Start the HTTP server:**
   ```sh
   python -m http.server --cgi
   ```

3. **Open a browser and go to `http://localhost:8000/form.html` to display and test the form.**