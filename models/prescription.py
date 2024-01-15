import mysql.connector
from mysql.connector import Error

class Prescription:
    def __init__(self, db_connection, patient_name, patient_id, doctor_name, doctor_id, clinic, id_appointment):
        self.db_connection = db_connection
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.doctor_name = doctor_name
        self.doctor_id = doctor_id
        self.clinic = clinic
        self.id_appointment = id_appointment
        self.prescription = None

        self.write_prescription()

    def write_prescription(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO prescriptions (patient_name, patient_id, doctor_name, doctor_id, clinic, id_appointment, prescription)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (self.patient_name, self.patient_id, self.doctor_name, self.doctor_id, self.clinic, self.id_appointment, self.prescription))
            self.db_connection.commit()
            print("Prescription added successfully.")
        except Error as e:
            print(f"Error adding prescription: {e}")




# Example Usage:
if __name__ == "__main__":
    try:
        db_config = {
            'host': 'your_host',
            'user': 'your_username',
            'password': 'your_password',
            'database': 'your_database'
        }
        connection = mysql.connector.connect(**db_config)

        # Create a prescription
        prescription1 = Prescription(connection, patient_name="John Doe", patient_id=1, doctor_name="Dr. Smith", doctor_id=1, clinic="ABC Clinic", id_appointment=101)
        
        # Display prescriptions and pharmacy records
        prescription1.display_prescriptions()

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        # بستن اتصال به پایگاه داده
        if connection.is_connected():
            connection.close()
            print("Connection closed.")
