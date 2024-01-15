import mysql.connector
from mysql.connector import Error


class Pharmacy:
    def __init__(self, db_connection, patient_name, patient_id, doctor_name, doctor_id, name_medicine, medicine_id):
        self.db_connection = db_connection
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.doctor_name = doctor_name
        self.doctor_id = doctor_id
        self.name_medicine = name_medicine
        self.medicine_id = medicine_id
        self.status = 'not delivered'
        self.instructions = None

        self.write_medication_instructions()

    def change_status(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('UPDATE pharmacy SET status = %s WHERE medicine_id = %s', ('delivered', self.medicine_id))
            self.db_connection.commit()
            print(f"Medication status changed to 'delivered' for medicine ID: {self.medicine_id}")
        except Error as e:
            print(f"Error changing status: {e}")

    def write_medication_instructions(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO pharmacy (patient_name, patient_id, doctor_name, doctor_id, name_medicine, medicine_id, status, instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.patient_name, self.patient_id, self.doctor_name, self.doctor_id, self.name_medicine, self.medicine_id, self.status, self.instructions))
            self.db_connection.commit()
            print("Medication instructions added successfully.")
        except Error as e:
            print(f"Error adding medication instructions: {e}")

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

        # Create a pharmacy record
        pharmacy1 = Pharmacy(connection, patient_name="John Doe", patient_id=1, doctor_name="Dr. Smith", doctor_id=1, name_medicine="Aspirin", medicine_id=201)

        pharmacy1.display_pharmacy()

        # Change status of pharmacy record
        pharmacy1.change_status()

        # Display updated pharmacy records
        pharmacy1.display_pharmacy()

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        # بستن اتصال به پایگاه داده
        if connection.is_connected():
            connection.close()
            print("Connection closed.")
