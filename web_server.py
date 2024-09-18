"""
A web server that serves static files (CSS, images) and HTML pages (index, message, error).

The web server also handles form submissions and 
forwards the data to a socket server for processing.
The web server is configured to run on port 3000 by default, 
but this can be changed by setting the PORT environment variable.
"""
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import json
import mimetypes
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Web server configuration
PORT: int = int(os.getenv('PORT', '3000'))

# Define the directory for templates and static resources
template_dir: str = os.path.join(os.path.dirname(__file__), 'templates')
static_dir: str = os.path.join(os.path.dirname(__file__), 'static')

# Socket server configuration
SOCKET_HOST = os.getenv('SOCKET_HOST', 'localhost')
SOCKET_PORT = int(os.getenv('SOCKET_PORT', '5000'))

class CustomHandler(SimpleHTTPRequestHandler):
    """
    A custom handler that extends SimpleHTTPRequestHandler 
    to serve HTML files and handle form submissions.
    """

    def do_GET(self):
        """
        Handles GET requests. Serves static files (CSS, images) and HTML pages (index, message, error).
        """

        # Check if the request is for static resources (starts with /static/)
        if self.path.startswith('/static/'):
            # Correctly replace only the first occurrence of /static/
            file_path = os.path.join(static_dir, self.path.replace('/static/', '', 1))
            # Print the resolved static file path for debugging
            print(f"Static file path: {file_path}")
            if os.path.exists(file_path) and not os.path.isdir(file_path):
                # Serve the static file if it exists
                self.send_static(self.path)
            else:
                print("Static file not found.")
                self.send_error(404)
                return

        # Serve HTML pages based on the request path
        file_path: Optional[str] = None
        match self.path:
            case '/':
                file_path = os.path.join(template_dir, 'index.html')
            case '/message':
                file_path = os.path.join(template_dir, 'message.html')
            case '/error':
                file_path = os.path.join(template_dir, 'error.html')
            case _:
                # For any other path, serve a 404 error
                self.send_error(404)
                return

        # Check if the requested HTML file exists
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            self.send_html_file(file_path)
        else:
            print("HTML file not found.")
            self.send_error(404)

    def send_html_file(self, filepath: str, status: int = 200):
        """
        Sends an HTML file as a response.

        :param filepath: The path to the HTML file to be sent.
        :param status: The HTTP status code to be sent.
        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filepath, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, file_path: str):
        """
        Sends a static file as a response.
        """
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{file_path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_error(self, code, message=None, explain=None):
        """
        Handles errors (404 Not Found) and returns the error.html page if a 404 occurs.
        """
        if code == 404:
            error_page_path = os.path.join(template_dir, 'error.html')
            try:
                with open(error_page_path, 'rb') as file:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(file.read())  # Send the error page content
            except FileNotFoundError:
                # If error.html is not found, send a simple 404 response
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
        else:
            return super().send_error(code, message, explain)

    def do_POST(self):
        """
        Handles POST requests. Receives form data and forwards 
        it to the socket server for processing.
        """
        if self.path == '/submit_message':
            try:
                # Get the length of the POST data and read it
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                parsed_data = dict(x.split('=') for x in post_data.split('&'))

                # Prepare the message to send to the socket server
                message = json.dumps({
                    "username": parsed_data.get('username', ''),
                    "message": parsed_data.get('message', '')
                })

                # Send the message to the socket server
                self.send_to_socket_server(message)

                # Respond to the form submission
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Message received and forwarded to socket server.")

            except (ValueError, KeyError) as e:
                # Handle form parsing errors
                print(f"Error parsing form data: {e}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid form data.")

            except Exception as e:
                # Handle any other unexpected errors
                print(f"Unexpected error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal server error.")

    def send_to_socket_server(self, message: str) -> None:
        """
        Sends a message to the socket server via TCP.
        Includes proper error handling in case of connection or communication failures.
        :param message: The message to be sent in JSON format.
        """
        try:
            # Establish a TCP connection to the socket server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SOCKET_HOST, SOCKET_PORT))
                sock.sendall(message.encode('utf-8'))
                print(f"Message sent to socket server: {message}")

        except ConnectionRefusedError:
            # If the socket server is not reachable
            print("Error: Could not connect to the socket server.")
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b"Socket server unavailable. Please try again later.")

        except socket.error as e:
            # General socket error handling
            print(f"Socket error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Socket communication error.")


def run_web_server(
        server_class: HTTPServer = HTTPServer, 
        handler_class: SimpleHTTPRequestHandler = CustomHandler
    ) -> None:
    """
    Starts the HTTP server on the specified port.
    :param server_class: The class for the HTTP server.
    :param handler_class: The handler class that will manage HTTP requests.
    """
    server_address: tuple = ('', PORT)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f'Serving on port {PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_web_server()