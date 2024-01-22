import sqlite3
from sqlite3 import Error


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
