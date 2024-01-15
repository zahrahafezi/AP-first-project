import sqlite3

# CONNECT TO THE DATABASE OR CREATE IT IF IF DOES NOR EXIST
conn = sqlite3.connect('clinic.db')

# CREATE A CURSOR TO PERFORM DATABASE OPERATIONS
cursor = conn.cursor()

# CREATE USER TABLE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# CREATE A TABLE OF DOCTORS
cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        education TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        clinic_id INTEGER,
        FOREIGN KEY (clinic_id) REFERENCES clinics(id)
    )
''')

# CREATE USER TABLE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        user_id INTEGER PRIMARY KEY,
        contact_number TEXT NOT NULL,
        city TEXT NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# CREATE AN APPOINTMENT SCHEDULE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_name TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(user_id)
    )
''')

# CREATE A TABLE OF CLINIC
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clinics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT NOT NULL,
        availability TEXT NOT NULL,
        services TEXT NOT NULL
    )
''')

# APPLY CHANGES
conn.commit()

# CLOSE THE CONNECTION
conn.close()




# ADD ROW
c.execute("INSERT INTO users (id, name, address, email, user_type, password) VALUES (1234, 'MAMMAD', 'MAMMADI', '123 Main St', '')")
