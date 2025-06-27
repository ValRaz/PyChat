import socket
import threading
import random

# Keeps track of all active client connections
clients = []
clients_lock = threading.Lock()
# Maps socket -> user ID string
user_ids = {}

# Sends message to all connected except the sender
def broadcast(msg_bytes):
    with clients_lock:
        for conn in clients:
            try:
                conn.sendall(msg_bytes)
            except:
                pass

# Handles per client messaging
def handle_client(conn, addr):
    # Generates and stores a UID
    uid = f"{random.randint(0, 99999):05d}"
    # Adds new client to the list
    with clients_lock:
        clients.append(conn)

    print(f"[PyChat Server] Connection from {addr}")
    conn.sendall(b"Welcome to PyChat Server!")
    # Displays assigned ID to the user:
    conn.sendall(f"ID:{uid}".encode('utf-8'))

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[PyChat Server] Received from {addr}: {message}")

            # Broadcast to all other clients
            broadcast(f"{uid}: {message}".encode('utf-8'))
    except ConnectionResetError:
        pass
    finally:
        # Remove this client and clean up
        with clients_lock:
            clients.remove(conn)
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