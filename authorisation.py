import serial
import time
import sqlite3
import os
import cv2
import datetime
import base64
import pygame
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from insertion import create_database, display_data
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up the serial communication with Arduino - adjust the serial port and the baud rates as needed
serialConn = serial.Serial('/dev/tty.usbmodem11101', 9600)

# Initialize pygame mixer
pygame.mixer.init()
def take_picture(directory="pictures"):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    cam = cv2.VideoCapture(0)

    # Try to enable the flashlight if supported by the camera
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Set auto exposure to manual mode
    cam.set(cv2.CAP_PROP_EXPOSURE, -10)  # Set exposure value to a negative value (may vary depending on camera)

    # Wait for a short period to allow the flashlight to turn on
    time.sleep(1)

    ret, frame = cam.read()
    if ret:
        # Use timestamp to make a unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"{directory}/unauthorized_{timestamp}.jpg"
        cv2.imwrite(image_path, frame)

        # Play the click sound
        pygame.mixer.music.load("nice-camera-click-106269.mp3")
        pygame.mixer.music.play()

        # Send email with the captured image as an attachment
        send_email_async(image_path)

    cam.release()
def send_email(image_path):
    # Email configuration
    sender_email = "andersonmia1968@gmail.com"
    receiver_emails = [
        "karigirwasonia0@gmail.com",
        "vanessahirwa5@gmail.com",
        "kabalisamelissa2@gmail.com",
        # "irakramlaw@gmail.com"

    ]

    credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    token_path = os.path.join(os.path.dirname(__file__), "token.json")

    # Check if token file exists
    if not os.path.exists(token_path):
        # Create the token file and request authorization from the user
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, ['https://www.googleapis.com/auth/gmail.send'])
        creds = flow.run_local_server(port=0)
        # Save the credentials to the token file
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    # Load the credentials from the token file
    creds = Credentials.from_authorized_user_file(token_path)

    # Build the Gmail service using the credentials
    service = build("gmail", "v1", credentials=creds)

    # Create a multipart message object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)
    message["Subject"] = "Unauthorized Access Detected"

    # Add image attachment to the email
    with open(image_path, "rb") as file:
        attachment = MIMEImage(file.read())
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(image_path))
        message.attach(attachment)

    # Add a text message to the email body
    body_text = "Unauthorized access detected by the RFID System. Please check the attached image."
    message.attach(MIMEText(body_text, "plain"))

    # Encode the message as a raw string
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

    print("Email sent to the managers.")

def send_email_async(image_path):
    # Create a thread for sending the email
    email_thread = threading.Thread(target=send_email, args=(image_path,))
    email_thread.start()

def search_database(card_id):
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT card_id FROM authorised_cards WHERE card_id=?", (card_id,))
        result = cursor.fetchone()
    return result is not None


def create_product_array():
    product_array = [
        [1, "Smartphone", 1000, 100, 50],
        [2, "Laptop", 1500, 120, 60],
        [3, "Headphones", 200, 20, 10],
        [4, "Smart TV", 2500, 150, 70],
        [5, "Fitness Tracker", 150, 15, 8],
        [6, "Bluetooth Speaker", 100, 10, 5],
        [7, "Digital Camera", 800, 80, 40],
        [8, "Gaming Console", 500, 50, 25],
        [9, "Wireless Earbuds", 150, 15, 8],
        [10, "Portable Hard Drive", 120, 12, 6],
        [11, "Tablet", 600, 60, 30],
        [12, "Smart Watch", 300, 30, 15],
        [13, "Drones", 500, 50, 25],
        [14, "Gaming Keyboard", 150, 15, 8],
        [15, "Wireless Router", 80, 8, 4],
        [16, "External SSD", 200, 20, 10],
        [17, "Bluetooth Headset", 100, 10, 5],
        [18, "Printer", 250, 25, 12],
        [19, "Wireless Mouse", 50, 5, 3],
        [20, "Smart Home Hub", 150, 15, 8],
        [21, "VR Headset", 300, 30, 15],
        [22, "External Monitor", 200, 20, 10],
        [23, "Wireless Keyboard", 100, 10, 5],
        [24, "Power Bank", 50, 5, 3],
        [25, "Action Camera", 300, 30, 15],
        [26, "Portable Bluetooth Speaker", 80, 8, 4],
        [27, "Graphic Drawing Tablet", 200, 20, 10],
        [28, "Smart Thermostat", 150, 15, 8],
        [29, "Wireless Charging Pad", 50, 5, 3],
        [30, "Bluetooth Earphones", 100, 10, 5],
        [31, "Streaming Device", 80, 8, 4],
        [32, "Home Security Camera", 200, 20, 10],
        [33, "Wireless Soundbar", 150, 15, 8],
        [34, "USB Flash Drive", 50, 5, 3],
        [35, "Wireless Gaming Mouse", 100, 10, 5],
        [36, "Smart Bulbs", 80, 8, 4],
        [37, "Noise-Canceling Headphones", 200, 20, 10],
        [38, "Smart Plug", 50, 5, 3],
        [39, "Portable SSD", 150, 15, 8],
        [40, "Bluetooth Car Kit", 80, 8, 4],
        [41, "Fitness Smartwatch", 200, 20, 10],
        [42, "USB-C Hub", 50, 5, 3],
        [43, "Wireless Gaming Controller", 100, 10, 5],
        [44, "Wireless Range Extender", 80, 8, 4],
        [45, "Bluetooth Trackers", 150, 15, 8],
        [46, "Smart Doorbell", 200, 20, 10],
        [47, "Wireless Keyboard and Mouse Combo", 50, 5, 3],
        [48, "Gaming Mouse Pad", 80, 8, 4],
        [49, "Bluetooth Receiver", 100, 10, 5],
        [50, "Wireless Presenter", 50, 5, 3]
    ]
    return product_array

def display_products(product_array):
    for product in product_array:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Points: {product[3]}, Bonus: {product[4]}")
    
   

def getBalance():
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authorised_cards")
        rows = cursor.fetchall()
        for row in rows:
            ID = row[1]
            Balance = row[2]
            Points = row[3]
        return Balance

def getPoints():
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authorised_cards")
        rows = cursor.fetchall()
        for row in rows:
            ID = row[1]
            Balance = row[2]
            Points = row[3]
        return Points

def update_balance_and_points(card_id, new_balance, new_points):
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE authorised_cards SET balance=?, points=? WHERE card_id=?", (new_balance, new_points, card_id))
        connection.commit()
        serialConn.write(f"B{new_balance}".encode())
        serialConn.write(f"P{new_points}".encode())


def display_products_within_balance(product_array, balance):
    valid_products = [product for product in product_array if product[2] <= balance]
    if valid_products:
        print("Available products within your balance:")
        for product in valid_products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Points: {product[3]}, Bonus: {product[4]}")
    else:
        print("No products available within your balance.")


def display_products_within_points(product_array, available_points):
    valid_products = [product for product in product_array if product[3] <= available_points]
    if valid_products:
        print("Available products within your points range:")
        for product in valid_products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Points: {product[3]}, Bonus: {product[4]}")
    else:
        print("No products available within your points range.")


def update_points(card_id, new_points):
    db_file = os.path.join(os.path.dirname(__file__), 'RFID.db')
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE authorised_cards SET points = ? WHERE card_id = ?", (new_points, card_id))
        connection.commit()
        serialConn.write(f"P{new_points}".encode())


def main():
    create_database()  # Create the database table if it doesn't exist

    # Continuously read the card id from the Arduino and check if it's authorised
    while True:
        if serialConn.in_waiting > 0:
            card_id = serialConn.readline().decode('utf-8').strip()
            balance = serialConn.readline().decode('utf-8').strip()
            points = serialConn.readline().decode('utf-8').strip()
            print("Card id: " + card_id)
            print("Card balance: " + balance)
            print("Card points: " + points)
            authorised = search_database(card_id)
            if authorised:
                serialConn.write(b'A')
                print("Authorised card")

                product_array = create_product_array()
                display_products(product_array)

                selected_id = int(input("Enter the ID of the product you want to buy: "))
                selected_product = None
                for product in product_array:
                    if product[0] == selected_id:
                        selected_product = product
                        break

                if selected_product:
                    price = selected_product[2]
                    points_required = selected_product[3]
                    bonus = selected_product[4]

                    print("Selected product details:")
                    print(f"Name: {selected_product[1]}")
                    print(f"Price: {price}")
                    print(f"Points Required: {points_required}")
                    print(f"Bonus: {bonus}")

                    balance = getBalance()
                    points = getPoints()

                    payment_method = input("Choose payment method (money/points): ")
                    if payment_method.lower() == "money":
                        if int(balance) >= price:
                            balance = int(balance) - price
                            points = int(points) + bonus
                            print("Transaction successful.")
                            print(f"New balance: {balance}")
                            print(f"New points: {points}")
                            # Update the database with the new balance and points
                            update_balance_and_points(card_id, balance, points)
                            display_data()
                        else:
                            print("Insufficient balance. Please choose another product.")
                            # Display products within the price range of the balance
                            display_products_within_balance(product_array, int(balance))

                    elif payment_method.lower() == "points":
                        if int(points) >= points_required:
                            points = int(points) - points_required + bonus
                            print("Transaction successful.")
                            print(f"New points: {points}")
                            update_points(card_id, points)
                            display_data()
                        else:
                            print("Insufficient points. Please choose another product.")
                            display_products_within_points(product_array, int(points))
                            break

                else:
                    print("Invalid product ID. Please try again.")

            else:
                serialConn.write(b'D')
                print("Unauthorised card")
                take_picture()

            time.sleep(1)
        else:
            time.sleep(0.1)  # Sleep for a short period to avoid excessive looping



if __name__ == "__main__":
    main()