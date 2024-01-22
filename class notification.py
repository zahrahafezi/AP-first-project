from datetime import datetime
import sqlite3
from sqlite3 import Error


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
