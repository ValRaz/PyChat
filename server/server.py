import socket
import threading
import random

# Keeps track of all active client connections.
clients = []
clients_lock = threading.Lock()

# Broadcasts a byte‐string message to all connected clients.
def broadcast(msg_bytes):
    with clients_lock:
        for conn in clients:
            try:
                conn.sendall(msg_bytes)
            except:
                pass

# Handles per‐client continuous messaging and unique ID assignment:
def handle_client(conn, addr):
    uid = f"{random.randint(0, 99999):05d}"
    with clients_lock:
        clients.append(conn)

    # Sends welcome message with assigned ID
    print(f"[PyChat Server] {uid} connected from {addr}")
    conn.sendall(b"Welcome to PyChat Server!")
    conn.sendall(f"ID:{uid}".encode('utf-8'))

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"[PyChat Server] {uid} says: {message}")
            broadcast(f"{uid}: {message}".encode('utf-8'))
    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"[PyChat Server] {uid} disconnected")

# Starts the PyChat server and handles threading per client.
def run_server():
    HOST = '127.0.0.1'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[PyChat Server] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()

if __name__ == "__main__":
    run_server()