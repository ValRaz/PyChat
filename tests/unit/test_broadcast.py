import socket
import threading
import pytest
from server.server import clients, clients_lock, broadcast

# Clears and leftover clients
@pytest.fixture(autouse=True)
def clear_clients():
    with clients_lock:
        clients.clear()
    yield
    with clients_lock:
        clients.clear()

# Tests that broadcast sends messages to all connected sockets
def test_broadcast_sends_to_all():
    s1, c1 = socket.socketpair()
    s2, c2 = socket.socketpair()
    with clients_lock:
        clients.extend([s1, s2])
    msg = b"hello"
    broadcast(msg)
    assert c1.recv(1024) == msg
    assert c2.recv(1024) == msg

    s1.close(); s2.close(); c1.close(); c2.close()