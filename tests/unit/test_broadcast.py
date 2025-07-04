import socket
import threading
import pytest
from server.server import clients, clients_lock, broadcast

@pytest.fixture(autouse=True)
def clear_clients():
    with clients_lock:
        clients.clear()
    yield
    with clients_lock:
        clients.clear()

def test_broadcast_sends_to_all():
    s1, c1 = socket.socketpair()
    s2, c2 = socket.socketpair()
    with clients_lock:
        clients.extend([s1, s2])
    msg = b"hello\n"
    broadcast(msg)
    assert c1.recv(1024) == msg
    assert c2.recv(1024) == msg
    for s in (s1, s2, c1, c2):
        s.close()

def test_broadcast_handles_disconnect_gracefully():
    s1, c1 = socket.socketpair()
    s2, c2 = socket.socketpair()
    with clients_lock:
        clients.extend([s1, s2])
    # Simulate s1 gone
    s1.close()
    # Should not raise
    broadcast(b"test\n")
    # c2 still receives
    assert c2.recv(1024) == b"test\n"
    for s in (s2, c1, c2):
        s.close()

def test_broadcast_no_clients_does_nothing():
    with clients_lock:
        clients.clear()
    # Should not raise or block
    broadcast(b"nothing\n")