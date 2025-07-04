import socket
import threading
import random

# Keeps track of all active client connections and maps user IDs to client sockets.
clients = []
clients_lock = threading.Lock()
user_sockets = {}

# Broadcasts a byte‐string message to all connected clients.
def broadcast(msg_bytes):
    with clients_lock:
        for conn in clients:
            try:
                conn.sendall(msg_bytes)
            except:
                pass

# Broadcasts the connected users list by IDs.
def broadcast_user_list():
    with clients_lock:
        user_list = ",".join(user_sockets.keys())
    # Sends users list as a clean standalone message
    broadcast(f"USERS:{user_list}\n".encode("utf-8"))

# Handles per‐client continuous messaging, unique ID assignment, and private messaging.
def handle_client(conn, addr):
    uid = f"{random.randint(0, 999999):06d}"
    with clients_lock:
        clients.append(conn)
        user_sockets[uid] = conn

    # Sends welcome message with assigned ID
    print(f"[PyChat Server] {uid} connected from {addr}")
    welcome_message = f"Welcome to PyChat Server!\nID:{uid}\n"
    conn.sendall(welcome_message.encode("utf-8"))
    broadcast_user_list()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode("utf-8").strip()
            if not message:
                continue

            print(f"[PyChat Server] {uid} says: {message}")

            # Handles private messaging
            if message.startswith("/msg "):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    continue
                target_uid, private_text = parts[1], parts[2]
                target_conn = user_sockets.get(target_uid)
                if target_conn:
                    target_conn.sendall(f"[Private] {uid}: {private_text}\n".encode("utf-8"))
                    conn.sendall(f"[Private] To {target_uid}: {private_text}\n".encode("utf-8"))
                continue

            # Main chat message broadcasting.
            broadcast(f"{uid}: {message}\n".encode("utf-8"))

    except ConnectionResetError:
        pass
    finally:
        # Removes this client and cleans up.
        with clients_lock:
            clients.remove(conn)
            user_sockets.pop(uid, None)
        conn.close()
        print(f"[PyChat Server] {uid} disconnected")
        broadcast_user_list()

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