"""
This script starts a socket server that listens 
for connections from the web server and processes messages.

The socket server is configured to run on port 5000 by default, 
but this can be changed by setting the SOCKET_PORT environment variable.
"""
import os
import socket
import json
from typing import Dict
from datetime import datetime
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_DB = os.getenv('MONGO_DB', 'messages_database')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'messages')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_AUTH_DB = os.getenv('MONGO_AUTH_DB', 'admin')

# Socket server configuration
SOCKET_HOST = os.getenv('SOCKET_HOST', 'localhost')
SOCKET_PORT = int(os.getenv('SOCKET_PORT', '5000'))

# MongoDB setup
try:
    mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB]
    messages_collection = db[MONGO_COLLECTION]

    # Check if MongoDB is reachable by performing a server check
    client.server_info()  # Will raise ServerSelectionTimeoutError if MongoDB is unavailable
    print("Connected to MongoDB successfully.")
except errors.ServerSelectionTimeoutError as e:
    print(f"Error: Could not connect to MongoDB: {e}")
    exit(1)


def save_message(data: Dict[str, str]) -> bool:
    """
    Saves a message to the MongoDB collection.
    Returns True if successful, False if an error occurs.
    :param data: The message data to be saved, including the username, message, and date.
    :return: True if the message was saved, False otherwise.
    """
    try:
        messages_collection.insert_one(data)
        return True
    except errors.PyMongoError as e:
        print(f"Error saving message to MongoDB: {e}")
        return False


def socket_server():
    """
    Starts a socket server that listens for connections from the web server and processes messages.
    Includes error handling for socket communication and MongoDB operations.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(('0.0.0.0', SOCKET_PORT))
        server_socket.listen(5)  # Listen for up to 5 connections
        print(f"Socket server listening on {SOCKET_HOST}:{SOCKET_PORT}")
    except socket.error as e:
        print(f"Error setting up socket server: {e}")
        exit(1)

    while True:
        try:
            # Accept a new connection from the web server
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")

            # Receive the message from the web server
            message = client_socket.recv(1024).decode('utf-8')

            # Convert the received message to a dictionary and add a timestamp
            message_data = json.loads(message)
            message_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Save the message to MongoDB
            if save_message(message_data):
                print(f"Message saved to MongoDB: {message_data}")
                client_socket.sendall(b"Message received and saved.")
            else:
                print("Failed to save message to MongoDB.")
                client_socket.sendall(b"Failed to save message to database.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON message: {e}")
            client_socket.sendall(b"Invalid message format.")
        except socket.error as e:
            print(f"Socket error during communication: {e}")
            client_socket.sendall(b"Socket communication error.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_socket.sendall(b"Server encountered an error.")
        finally:
            # Close the connection with the web server
            client_socket.close()


if __name__ == '__main__':
    socket_server()
