import socket

# Sets up server configuration
HOST = '127.0.0.1'
PORT = 65432

# Starts TCP server local host listening and welcome message for client connect.
def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"[PyChat Server] Listening at {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[PyChat Server] Connected by: {addr}")
            conn.sendall(b"Welcome to PyChat Server!")

if __name__ == "__main__":
    run_server()