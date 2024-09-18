# Web and Socket Server with MongoDB Integration

This project implements a simple web server and a socket server using Python. The web server allows users to submit messages via an HTML form, which are then sent to a socket server for processing and saved to a MongoDB database. MongoDB authentication is also supported.

## Features

- **Web Server**: Serves HTML pages and handles form submissions.
- **Socket Server**: Receives messages from the web server and stores them in MongoDB.
- **MongoDB Integration**: Saves each message with a timestamp in MongoDB.
- **Error Handling**: Graceful handling of socket communication errors and MongoDB connection/authentication issues.
- **MongoDB Authentication**: Connects to MongoDB using credentials stored in an `.env` file.

## Requirements

- Python 3.7 or higher
- MongoDB (with authentication if required)
- Required Python packages:
  - `pymongo`
  - `python-dotenv`

## Project Structure

```bash
.
├── .env               # Environment variables (MongoDB and socket server configuration)
├── web_server.py      # Web server code
├── socket_server.py   # Socket server code
├── templates          # HTML templates directory
│   ├── index.html
│   ├── message.html
│   └── error.html
└── static             # Static resources (CSS, images, etc.)
    ├── css
    │   └── style.css
    └── images
        └── logo.png
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-repo/web-socket-mongo.git
cd web-socket-mongo
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

Create a requirements.txt file if needed:
```bash
pymongo
python-dotenv
```

3. Set up MongoDB:
Ensure you have MongoDB installed and running. If MongoDB requires authentication, make sure the user has proper permissions to access the database.

4. Configure the .env file:
Create a .env file in the root directory with the following content:
```bash
# Web server configuration
PORT=3000

# MongoDB configuration
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=messages_database
MONGO_COLLECTION=messages
MONGO_USER=my_user        # Replace with your MongoDB username
MONGO_PASS=my_password    # Replace with your MongoDB password
MONGO_AUTH_DB=admin       # Authentication database (commonly 'admin')

# Socket server configuration
SOCKET_HOST=localhost
SOCKET_PORT=5000
```

# Running the Project
1. Start the MongoDB service:
Make sure MongoDB is running on the configured MONGO_HOST and MONGO_PORT.

2. Run the Socket Server:

In one terminal window, run the socket server:

```bash
python socket_server.py
```

The socket server will listen on the configured SOCKET_HOST and SOCKET_PORT for incoming messages.

3. Run the Web Server:

In another terminal window, run the web server:

```bash
python web_server.py
```

The web server will listen on the configured PORT (default: 3000).

4. Access the Web Application:

Open your web browser and navigate to:

```bash
http://localhost:3000
```

You should see the home page (index.html). You can submit a message from the /message page, and it will be sent to the socket server for processing and saved in MongoDB.