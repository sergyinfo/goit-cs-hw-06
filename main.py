import multiprocessing
from web_server import run_web_server
from socket_server import socket_server

if __name__ == '__main__':
    web_process = multiprocessing.Process(target=run_web_server)
    socket_process = multiprocessing.Process(target=socket_server)

    # Start both processes
    web_process.start()
    socket_process.start()

    # Join processes to ensure they run concurrently
    web_process.join()
    socket_process.join()
