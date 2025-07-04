import socket
import threading
import time
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
        buf += sock.recv(1024).decode()
    return buf

def test_user_list_update_on_connect_and_disconnect(server_thread):
    # Client A connects
    a = socket.socket()
    a.connect(('127.0.0.1', 65432))
    init = recv_until(a, "USERS:")
    ids0 = init.split("USERS:")[1].strip().split(",")
    assert len(ids0) == 1, f"Expected 1 user initially, got {ids0}"

    # Client B connects
    b = socket.socket()
    b.connect(('127.0.0.1', 65432))
    upd = recv_until(a, "USERS:")
    ids1 = upd.split("USERS:")[1].strip().split(",")
    assert len(ids1) == 2

    # Verify B sees same list
    buf_b = recv_until(b, "USERS:")
    ids_b = buf_b.split("USERS:")[1].strip().split(",")
    assert set(ids1) == set(ids_b)

    # B disconnects
    b.close()
    final = recv_until(a, "USERS:")
    ids2 = final.split("USERS:")[1].strip().split(",")
    assert len(ids2) == 1 and ids2[0] == ids0[0]

    a.close()