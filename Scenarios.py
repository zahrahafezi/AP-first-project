# from class appointment import *
# from class clinic import *
# from class medication import *
# from class notification import *
# from class rating import *
# from class user import *
import hashlib
import pyotp
import sqlite3
from datetime import datetime
import requests

print('welcome to the medical clinic site')


class Scenario:
    connection = sqlite3.connect('C:/Users/TUF/Desktop/Projectphase1/clinic reservation.db')
    cursor = connection.cursor()

    def login_process(self):
        name = input('please enter your name: ')
        # check if username exist in database
        # if it does not, error, if it does continue
        # what if they were logged in
        self.cursor.execute('select user_type from users where name = ?', (name,))
        user_type = self.cursor.fetchone()
        option = int(input('Please select your login method:'
                           ' [1=enter with One-time password 2=enter with fixed password]:'))
        if option == '1':
            # using pyotp to create one-time password, Create a TOTP object
            totp = pyotp.TOTP(pyotp.random_base32())
            # Get the current OTP
            otp = totp.now()
            # Print the OTP
            print("Your one-time password is:", otp)
            password = input('please enter your password:')
            if password == otp:
                print("you are logged in!")
            else:
                print("wrong code entered!")
        elif option == '2':
            password = input('please enter your password:')
            self.cursor.execute("""SELECT password FROM users WHERE name = ?""", (name,))
            db_password = self.cursor.fetchone()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == db_password:
                print('you are logged in!')
            else:
                print('error!password does not match!')

        if user_type == "patient":
            print('welcome to appointment site ' + name + '!')
            # does it work like this? like saying just the number
            demands = input('1:Current reservation times,2:History of the past reservations, 3:Book a new appointment')
            current_time = datetime.now()
            self.cursor.execute('SELECT clinic_id, datetime FROM appointments WHERE user_id = ?', (name,))
            reservations = self.cursor.fetchall()
            # our reserve does not have time!
            if demands == "1":
                for clinic_id, reservation_time in reservations:
                    if reservation_time > current_time:
                        print(f"Upcoming reservation at clinic {clinic_id} on {reservation_time}")
            elif demands == "2":
                for clinic_id, reservation_time in reservations:
                    print(f"Upcoming reservation at clinic {clinic_id} on {reservation_time}")
            elif demands == "3":
                clinic_id = input("Enter clinic ID: ")
                reserved_slots = int(input("Enter number of slots to reserve: "))
                # Communicate with the API to reserve slots
                api_response = requests.post('http://127.0.0.1:5000',
                                             json={"id": clinic_id, "reserved": reserved_slots})

                if api_response.json()["success"]:
                    print("Appointment successfully booked.")
                else:
                    print("Failed to book appointment.")
                # user can only reserve times in the future
                # reserves add clinic class db uml scenario and minus the reserves





        # elif user_type == "clinic staff":
        #     print('welcome to appointment site ' + name + '!')
