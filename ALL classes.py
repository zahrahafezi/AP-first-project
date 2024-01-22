import random
import re
import hashlib
import sqlite3
from sqlite3 import Error
import request
from datetime import datetime


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


# -------------------------------------------------------------------------------------------


class Clinic:
    connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
    cursor = connection.cursor()

    def __init__(self, name, contact_number, address, email, services, reserve_slots=0, available=True):
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.name = name
        self.address = address
        self.email = email
        self.contact_number = contact_number
        self.services = services
        self.availability = available
        self.reserve_slots = reserve_slots

        # self.add_clinic()

    def add_clinic(self):
        try:
            def generate_random_id():
                random_id = random.randint(1000, 9999)
                return str(random_id)

            clinic_id = generate_random_id()
            self.cursor.execute(
                '''INSERT INTO clinics
                 (id, name, contact_number, address, email, availability, services, reserve_slots) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (clinic_id, self.name, self.contact_number, self.address, self.email, self.availability, self.services))

            self.connection.commit()

            api_url = 'http://127.0.0.1:5000/add_clinics'
            clinic_data = {
                "id": clinic_id,
                "name": self.name,
                "contact_number": self.contact_number,
                "address": self.address,
                "email": self.email,
                "availability": self.availability,
                "services": self.services
            }
            api_response = requests.post(api_url, json=clinic_data)

            if api_response.status_code == 200:
                print("Clinic data added to API.")
            else:
                print(f"Failed to add clinic data to API. Status code: {api_response.status_code}")
        except Error as e:
            print(f"SQLite error: {e}")

        # self.cursor.execute("SELECT * FROM clinics")
        # rows = self.cursor.fetchall()
        # for row in rows:
        #     print(row)

    def update_clinic_info(self):
        try:
            new_name = input("Enter new name (or press Enter to keep current): ")
            if new_name:
                self.name = new_name
                self.cursor.execute('''UPDATE clinics SET name = ?''', (new_name,))
            new_address = input("Enter new address (or press Enter to keep current): ")
            if new_address:
                self.address = new_address
                self.cursor.execute('''UPDATE clinics SET address = ?''', (new_address,))
            new_contact_info = input("Enter new contact_info (or press Enter to keep current): ")
            if new_contact_info:
                self.contact_number = new_contact_info
                self.cursor.execute('''UPDATE clinics SET contact_number = ?''',
                                    (new_contact_info,))
            new_services = input("Enter new services (or press Enter to keep current): ")
            if new_services:
                self.services = new_services
                self.cursor.execute('''UPDATE clinics SET services = ?''',
                                    (new_services,))

            new_availability = input("Enter new availability (or press Enter to keep current): ")
            if new_availability:
                self.availability = new_availability
                self.cursor.execute('''UPDATE clinics SET availability = ?''',
                                    (new_availability,))
            self.connection.commit()
            print("Clinic information updated successfully.")
        except Error as e:
            print(f"SQLite error: {e}")

    def set_availability(self, availability):
        try:
            self.cursor.execute('''UPDATE clinics SET availability = ? WHERE name = ?''', (availability, self.name))
            self.connection.commit()
            print(f"Availability for clinic '{self.name}' set to: {availability}")
        except Error as e:
            print(f"SQLite error: {e}")

    def view_appointment(self, clinic_id):
        try:
            self.cursor.execute('SELECT user_id and datetime FROM appointments WHERE clinic_id = ?', (clinic_id,))
            appointments = self.cursor.fetchone()
            print(appointments)
        except Error as e:
            print(f"SQLite error: {e}")


# clinic1 = Clinic("rose", "here", "email", "0192", "service", True)
# clinic1.update_clinic_info()

# ----------------------------------------------------------------------------------------------

class Appointment:
    def __init__(self, appointment_id, clinic_id, user_id, datetime, status="Scheduled"):
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.appointment_id = appointment_id
        self.clinic_id = clinic_id
        self.user_id = user_id
        self.datetime = datetime
        self.status = status

        self.add_appointment()

    def add_appointment(self):
        try:
            self.cursor.execute('''
                    INSERT INTO appointments (appointment_id, clinic_id, user_id, datetime, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.appointment_id, self.clinic_id, self.user_id, self.datetime, self.status))
            self.connection.commit()
            print("Appointment added successfully.")
        except Error as e:
            print(f"SQLite error: {e}")

    def reschedule_appointment(self, new_datetime):
        try:
            self.cursor.execute('select * from appointments where datetime = ?',
                                (new_datetime,))
            existing_appointment = self.cursor.fetchone()

            if existing_appointment is None:
                self.cursor.execute('UPDATE appointments SET datetime = ? WHERE appointment_id = ?',
                                    (new_datetime, self.appointment_id))
                self.cursor.execute('UPDATE appointments SET datetime = NULL WHERE appointment_id = ?',
                                    (self.appointment_id,))
                self.connection.commit()
                print(f"Appointment {self.appointment_id} has been rescheduled to {new_datetime}.")
            else:
                print("there is already an appointment in that time")
        except Error as e:
            print(f"SQLite error: {e}")

    def cancel_appointment(self):
        try:
            self.cursor.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?',
                                ("Cancelled", self.appointment_id))
            self.cursor.execute('UPDATE appointments SET datetime = NULL WHERE appointment_id = ?',
                                (self.appointment_id,))
            self.connection.commit()
            print(f"Appointment {self.appointment_id} has been cancelled.")
        except Error as e:
            print(f"SQLite error: {e}")

# ------------------------------------------------------------------------------------------------


class Notification:
    def __init__(self, notification_id, user_id, timestamp):
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.notification_id = notification_id
        self.user_id = user_id
        self.massage = "It's one hour before your appointment"
        self.timestamp = timestamp

        self.send_notification()

    def send_notification(self):
        try:
            self.cursor.execute('''
                select datetime from Appointment where user_id =?''', (self.user_id,))
            appointment_time = self.cursor.fetchone()

            if appointment_time:
                current_time = datetime.datetime.now()
                time_difference = appointment_time[0] - current_time

                # Check if it's one hour before the appointment time
                if time_difference.total_seconds() <= 3600:
                    print(self.massage)
            else:
                print("No notification needed.")
        except Error as e:
            print(f"SQLite error: {e}")

# ----------------------------------------------------------------------------------------------------


class Medication:
    def __init__(self, user_name, user_id, clinic_id, name_medicine, medicine_id):
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.user_name = user_name
        self.user_id = user_id
        self.clinic_id = clinic_id
        self.name_medicine = name_medicine
        self.medicine_id = medicine_id
        self.status = 'not delivered'
        self.instructions = None

    def change_status(self):
        try:
            self.cursor.execute('UPDATE medication_record SET status = ? WHERE medicine_id = ?',
                                ('delivered', self.medicine_id))
            self.connection.commit()
            print(f"Medication status changed to 'delivered' for medicine ID: {self.medicine_id}")
        except Error as e:
            print(f"SQLite error: {e}")

    def add_medication_record(self):
        try:
            self.cursor.execute('''
                    INSERT INTO medication_record 
                    (user_name, user_id, clinic_id, name_medicine, medicine_id, status, instructions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.user_name, self.user_id, self.clinic_id, self.name_medicine, self.medicine_id,
                      self.status, self.instructions))
            self.connection.commit()
            print("Medication record added successfully.")
        except Error as e:
            print(f"SQLite error: {e}")


# -------------------------------------------------------------------------------------------------


class Rating:
    def __init__(self, opinion, rating, clinic_id):
        self.connection = sqlite3.connect("C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db")
        self.cursor = self.connection.cursor()
        self.clinic_id = clinic_id
        self.rating = rating
        self.opinion = opinion

    def validate_rate(self, rating):
        try:
            rating = int(rating)

            if rating in [1, 2, 3, 4, 5]:
                return rating
            else:
                print("Rating must be 1, 2, 3, 4, or 5.")
                return None

        except ValueError:
            print("Invalid rating format.")
            return None

    def add_rating(self):
        try:
            rate = input("please rate the clinic:")
            while not self.validate_rate(rate):
                rate = input("Enter your name: ")
            self.cursor.execute('''
                            INSERT INTO rating (rating, opinion, clinic_id)
                            VALUES (?, ?, ?)
                        ''', (rate, self.opinion, self.clinic_id))
            self.connection.commit()
            print("changes added successfully.")
        except Error as e:
            print(f"SQLite error: {e}")

    def average_rating(self):
        try:
            self.cursor.execute('SELECT rating FROM rating WHERE clinic_id = ?', (self.clinic_id,))
            ratings = self.cursor.fetchall()
            if not ratings:
                print("No ratings found for the clinic.")
                return None
            average = sum(ratings) / len(ratings)
            return average
        except Error as e:
            print(f"SQLite error: {e}")