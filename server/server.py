import socket
import threading

# Handles single client communication with message echoing.
def handle_client(conn, addr):
    print(f"[PyChat Server] Connection from {addr}")
    conn.sendall(b"Welcome to PyChat Server!")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"[PyChat Server] Received from {addr}: {message}")
            conn.sendall(f"User: {message}".encode('utf-8'))
        except ConnectionResetError:
            break
    conn.close()
    print(f"[PyChat Server] Disconnected {addr}")

# Starts the PyChat server and listens for connections.
def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[PyChat Server] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

# Server configuration.
HOST = '127.0.0.1'
PORT = 65432

if __name__ == "__main__":
    run_server()