import threading
import socket
import time
import re
import pytest
from server.server import run_server

@pytest.fixture(scope="module")
def server_thread():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(0.5)
    yield

def recv_until(sock, marker, timeout=2):
    sock.settimeout(timeout)
    buf = ""
    while marker not in buf:
        chunk = sock.recv(1024).decode()
        if not chunk:
            break
        buf += chunk
    return buf

def test_handshake_and_broadcast(server_thread):
    clients = []
    # Connect three clients and verify full handshake in one shot
    for _ in range(3):
        c = socket.socket()
        c.connect(('127.0.0.1', 65432))
        txt = recv_until(c, "USERS:")
        assert "Welcome to PyChat Server!" in txt
        assert re.search(r"ID:\d{6}", txt), f"ID missing in handshake: {txt}"
        assert "USERS:" in txt
        clients.append(c)

    # Broadcast from each client and verify every client receives each message
    for idx, c in enumerate(clients):
        msg = f"Hi from {idx}"
        c.sendall((msg + "\n").encode())
        for rc in clients:
            data = recv_until(rc, msg)
            assert msg in data

    for c in clients:
        c.close()