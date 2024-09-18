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