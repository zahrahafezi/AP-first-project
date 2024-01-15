
import requests
from unidecode import unidecode
# تعریف کلاس UserManager
class UserManager:
    def __init__(self):
        self.users = {}

    # متد ثبت نام کاربر
    def register_user(self, username, password_type):
        if username not in self.users:
            password = input("Enter your password: ")
            # ذخیره اطلاعات کاربر در دیکشنری
            self.users[username] = {"password": password, "password_type": password_type}
            print(f"User {username} registered successfully!")
        else:
            print("Username is already taken. Please choose another one.")

    # متد احراز هویت کاربر
    def authenticate_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print(f"User {username} authenticated successfully!")
            return True
        else:
            print("Invalid credentials. Please check your username and password.")
            return False

# تعریف متد اصلی
def main():
    # ایجاد یک شی از کلاس UserManager
    user_manager = UserManager()

    # گرفتن نام کاربری و نوع رمز عبور از کاربر
    username = input("Enter your username: ")
    password_type = input("Choose your password type (fixed/one-time): ")

    # ثبت نام کاربر با استفاده از متد register_user
    user_manager.register_user(username, password_type)

    # گرفتن رمز عبور و احراز هویت با استفاده از متد authenticate_user
    password = input("Enter your password: ")
    user_manager.authenticate_user(username, password)

# اجرای متد main اگر فایل به عنوان اصلی اجرا شود
if __name__ == "__main__":
    main()


#--------------------------------------------------------------------------------------
    
class ReservationManager:
    def __init__(self):
        self.current_reservations = {}
        self.past_reservations = {}

    def reserve_time(self, username, time):
        # ذخیره وقت رزرو شده در لیست فعلی
        if username in self.current_reservations:
            self.current_reservations[username].append(time)
        else:
            self.current_reservations[username] = [time]

    def get_current_reservations(self, username):
        # دریافت وقت‌های رزرو فعلی کاربر
        return self.current_reservations.get(username, [])

    def get_past_reservations(self, username):
        # دریافت وقت‌های رزرو گذشته کاربر
        return self.past_reservations.get(username, [])

    def record_past_reservation(self, username, time):
        # ثبت وقت رزرو گذشته و حذف از لیست فعلی
        if username in self.current_reservations and time in self.current_reservations[username]:
            self.current_reservations[username].remove(time)
            if username in self.past_reservations:
                self.past_reservations[username].append(time)
            else:
                self.past_reservations[username] = [time]


class UserManager:
    def __init__(self):
        self.users = {}
        self.reservation_manager = ReservationManager()

    def register_user(self, username, password_type):
        if username not in self.users:
            password = input("Enter your password: ")
            self.users[username] = {"password": password, "password_type": password_type}
            print(f"User {username} registered successfully!")
        else:
            print("Username is already taken. Please choose another one.")

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print(f"User {username} authenticated successfully!")
            return True
        else:
            print("Invalid credentials. Please check your username and password.")
            return False

    def show_dashboard(self, username):
        print(f"Welcome, {username}!")
        print("1. View current reservations")
        print("2. View past reservations")
        print("3. Reserve a new time")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            current_reservations = self.reservation_manager.get_current_reservations(username)
            print(f"Current Reservations: {current_reservations}")
        elif choice == "2":
            past_reservations = self.reservation_manager.get_past_reservations(username)
            print(f"Past Reservations: {past_reservations}")
        elif choice == "3":
            time_to_reserve = input("Enter the time you want to reserve: ")
            self.reservation_manager.reserve_time(username, time_to_reserve)
            print(f"Reservation for {time_to_reserve} is successful!")

# تعریف متد اصلی
def main():
    user_manager = UserManager()

    username = input("Enter your username: ")
    password_type = input("Choose your password type (fixed/one-time): ")

    user_manager.register_user(username, password_type)

    password = input("Enter your password: ")
    if user_manager.authenticate_user(username, password):
        user_manager.show_dashboard(username)

if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------------
    


class ReservationManager:
    def __init__(self):
        self.base_url = "http://localhost:5000"  # آدرس اصلی API

    def reserve_time(self, username, time, clinic_id):
        # ارسال درخواست رزرو به API
        data = {"id": clinic_id, "reserved": 1}  # اینجا 1 به عنوان تعداد رزرو شده استفاده شده است
        response = requests.post(f"{self.base_url}/reserve", json=data)

        if response.status_code == 200 and response.json().get("success"):
            print(f"Reservation for {time} at clinic {clinic_id} is successful!")
        else:
            print("Reservation failed. Please try again.")

    def search_doctor(self, keyword):
        # جستجوی نام دکتر یا کلینیک با استفاده از API
        response = requests.get(f"{self.base_url}/slots")
        if response.status_code == 200:
            clinics = response.json()
            matching_clinics = [clinic for clinic in clinics if keyword.lower() in clinic.lower()]
            return matching_clinics
        else:
            print("Failed to retrieve clinic information from the API.")
            return []

class UserManager:
    def __init__(self):
        self.users = {}
        self.reservation_manager = ReservationManager()

    def register_user(self, username, password_type):
        if username not in self.users:
            password = input("Enter your password: ")
            self.users[username] = {"password": password, "password_type": password_type}
            print(f"User {username} registered successfully!")
        else:
            print("Username is already taken. Please choose another one.")

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print(f"User {username} authenticated successfully!")
            return True
        else:
            print("Invalid credentials. Please check your username and password.")
            return False

    def show_dashboard(self, username):
        print(f"Welcome, {username}!")
        print("1. View current reservations")
        print("2. View past reservations")
        print("3. Reserve a new time")
        print("4. Search for a doctor or clinic")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            current_reservations = self.reservation_manager.get_current_reservations(username)
            print(f"Current Reservations: {current_reservations}")
        elif choice == "2":
            past_reservations = self.reservation_manager.get_past_reservations(username)
            print(f"Past Reservations: {past_reservations}")
        elif choice == "3":
            time_to_reserve = input("Enter the time you want to reserve: ")
            clinic_id = input("Enter the clinic ID: ")
            self.reservation_manager.reserve_time(username, time_to_reserve, clinic_id)
        elif choice == "4":
            doctor_keyword = input("Enter the name of the doctor or clinic: ")
            matching_doctors = self.reservation_manager.search_doctor(doctor_keyword)
            print(f"Matching Doctors/Clinics: {matching_doctors}")

def main():
    user_manager = UserManager()

    username = input("Enter your username: ")
    password_type = input("Choose your password type (fixed/one-time): ")

    user_manager.register_user(username, password_type)

    password = input("Enter your password: ")
    if user_manager.authenticate_user(username, password):
        user_manager.show_dashboard(username)

if __name__ == "__main__":
    main()




class ReservationManager:
    # ... کدهای قبلی

    def show_available_slots(self, username):
        # درخواست دریافت وقت‌های موجود از API
        response = requests.get(f"{self.base_url}/slots")
        if response.status_code == 200:
            available_slots = response.json()
            print(f"Available Slots: {available_slots}")
            
            # انتخاب یک وقت از لیست
            selected_slot = input("Select a slot to reserve: ")
            clinic_id = input("Enter the clinic ID: ")
            
            # انجام رزرو
            self.reserve_time(username, selected_slot, clinic_id)
        else:
            print("Failed to retrieve available slots from the API.")

def main():
    # ... کدهای قبلی
    
    if user_manager.authenticate_user(username, password):
        user_manager.show_dashboard(username)
        # اضافه کردن نمایش وقت‌های موجود به این قسمت
        reservation_manager = ReservationManager()
        reservation_manager.show_available_slots(username)

if __name__ == "__main__":
    main()
