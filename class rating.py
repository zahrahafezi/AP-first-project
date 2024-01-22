import sqlite3
from sqlite3 import Error


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
