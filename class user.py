import random
import re
import hashlib
import sqlite3
from sqlite3 import Error


class Users:
    connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
    cursor = connection.cursor()

    def __init__(self):
        self.user_id = ""  # You can generate a unique user_id when needed
        self.name = ""
        self.email = ""
        self.password = ""
        self.user_type = ""
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.logged_in_user = None

    def close_connection(self):
        self.connection.close()

    def validate_name(self, name):
        return name.isalnum()

    def validate_password(self, password):
        pattern = r"^(?=.*[A-Z])(?=.*[0-9]).{8,}$"
        return re.match(pattern, password) and len(password) >= 8

    def register(self):
        try:
            self.name = input("Enter your name (alphabets and numbers only): ")
            while not self.validate_name(self.name):
                print("Invalid name. Please use only alphabets and numbers.")
                self.name = input("Enter your name: ")
            # Here you can insert 'self.name' into the database

            self.email = input("Enter your email: ")
            while not self.email.strip():
                print("Email cannot be empty.")
                self.email = input("Enter your email: ")
            # Here you can insert 'self.email' into the database

            self.password = input(
                "Enter your password (at least 8 characters, including an uppercase letter and a number): ")
            while not self.validate_password(self.password):
                print("Invalid password format.")
                self.password = input("Enter your password: ")
            password_hash = hashlib.sha256(self.password.encode()).hexdigest()
            # Here you can insert 'password_hash' into the database

            self.user_type = input("Enter user type (patient/clinic staff): ")
            while self.user_type not in ['patient', 'clinic staff']:
                print("Invalid user type. Choose 'patient' or 'clinic staff'.")
                self.user_type = input("Enter user type: ")

            # Here you can insert 'self.user_type' into the database

            def generate_random_id():
                # Generate a random 4-digit ID
                random_id = random.randint(1000, 9999)
                return str(random_id)

            user_id = generate_random_id()

            self.cursor.execute("INSERT INTO users (id, name, email, user_type, password) VALUES (?, ?, ?, ?, ?)",
                                (user_id, self.name, self.email, self.user_type, password_hash))

            self.connection.commit()
        except Error as e:
            print(f"SQLite error: {e}")

    # cursor.execute("SELECT * FROM users")
    #
    # # Fetch all the rows as a list of tuples
    # rows = cursor.fetchall()
    #
    # # Print the rows
    # for row in rows:
    #     print(row)

    def login(self, name, password):
        try:
            self.cursor.execute('SELECT password FROM users WHERE name = ?', (name,))
            result = self.cursor.fetchone()
            if result:
                stored_password_hash = result[0]
                entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
                if entered_password_hash == stored_password_hash:
                    print("Login successful.")
                    self.logged_in_user = name
                    return True
                else:
                    print("Incorrect password.")
                    return False
            else:
                print("Username not found.")
                return False
        except Error as e:
            print(f"SQLite error: {e}")

    def update_profile(self):
        try:
            if self.logged_in_user:
                new_name = input("Enter new name (or press Enter to keep current): ")
                if new_name:
                    self.cursor.execute("UPDATE users SET name = ?", (new_name,))
                    print("Name updated.")

                new_email = input("Enter new email (or press Enter to keep current): ")
                if new_email:
                    self.cursor.execute("UPDATE users SET email = ?", (new_email,))
                    print("Email updated.")

                new_password = input("Enter new password (or press Enter to keep current): ")
                if new_password and self.validate_password(new_password):
                    new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                    self.cursor.execute("UPDATE users SET password = ? ",
                                        (new_password_hash,))
                    print("Password updated.")

                new_user_type = input("Enter new user type (patient/clinic staff) (or press Enter to keep current): ")
                if new_user_type in ['patient', 'clinic staff']:
                    self.cursor.execute("UPDATE users SET user_type = ?", (new_user_type,))
                    print("User type updated.")
                self.connection.commit()
            else:
                print("Please log in before updating data")
        except Error as e:
            print(f"SQLite error: {e}")

    def view_appointment(self):
        try:
            self.cursor.execute('SELECT clinic_id and datetime FROM appointments WHERE user_id = ?', (self.user_id,))
            appointments = self.cursor.fetchone()
            print(appointments)
        except Error as e:
            print(f"SQLite error: {e}")

user = Users()
user.register()


# user1 = Users()
# user1.login("zahra2", "Zahra1382")
# user1.update_profile()
