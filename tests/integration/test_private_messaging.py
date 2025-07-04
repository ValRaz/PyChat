import socket
import time
import pytest
from server.server import run_server

@pytest.fixture(scope="module")
def server_thread():
    import threading
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(0.5)
    yield

def recv_until(sock, marker, timeout=2):
    sock.settimeout(timeout)
    data = ""
    while marker not in data:
        chunk = sock.recv(1024).decode()
        if not chunk:
            break
        data += chunk
    return data

def test_private_message_delivery(server_thread):
    # Setup two clients
    c1 = socket.socket()
    c2 = socket.socket()
    c1.connect(('127.0.0.1', 65432))
    c2.connect(('127.0.0.1', 65432))

    # Drain handshake
    buf1 = recv_until(c1, "USERS:")
    buf2 = recv_until(c2, "USERS:")

    # Extract IDs
    id1 = next(line.split(":",1)[1] for line in buf1.splitlines() if line.startswith("ID:"))
    id2 = next(line.split(":",1)[1] for line in buf2.splitlines() if line.startswith("ID:"))

    # Send private message
    text = "SecretMessage"
    c1.sendall(f"/msg {id2} {text}\n".encode())

    # Recipient sees it
    out2 = recv_until(c2, f"[Private] {id1}: {text}")
    assert f"[Private] {id1}: {text}" in out2

    # Sender sees echo
    out1 = recv_until(c1, f"[Private] To {id2}: {text}")
    assert f"[Private] To {id2}: {text}" in out1

    c1.close()
    c2.close()