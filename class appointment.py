import sqlite3
from sqlite3 import Error


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


# --------------------------------------------------------------------------------------------------------

