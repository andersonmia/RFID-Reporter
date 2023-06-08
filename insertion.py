import os
import sqlite3
import serial
import time

serialConn = serial.Serial('/dev/tty.usbmodem11101', 9600)


def create_database():
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS authorised_cards (
            entry INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT,
            balance INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0
        )
    ''')

    connection.commit()
    connection.close()


def insert_card(card_id, balance, points):
    print(card_id)
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM authorised_cards")
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute("INSERT INTO authorised_cards (card_id, balance, points) VALUES (?, ?, ?)",
                           (str(card_id), balance, points))
            connection.commit()

            print("Card inserted successfully.")
        else:
            print("Card not inserted. The table already contains at least one card.")


def display_data():
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authorised_cards")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Card ID: {row[1]}, Balance: {row[2]}, Points: {row[3]}")


def main():
    create_database()  # Create the database table if it doesn't exist

    # Read data from Arduino and extract card ID, balance, and points
    while True:
        time.sleep(0.1)  # Add a small delay to allow the Arduino to send the data
        if serialConn.in_waiting > 0:
            card_id = serialConn.readline().decode('utf-8').strip()
            balance = serialConn.readline().decode('utf-8').strip()
            points = serialConn.readline().decode('utf-8').strip()
            break

    # Insert the card data into the database
    insert_card(card_id, balance, points)

    # Display the data in the database
    display_data()

    # Exit the program after processing the data once
    exit()


if __name__ == "__main__":
    main()
