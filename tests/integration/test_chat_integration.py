import threading
import socket
import time
import pytest
from server.server import run_server

# Starts server for testing.
@pytest.fixture(scope="module")
def server_thread():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(0.5)
    yield

# Tests multiclient connection and messaging functionality. 
def test_message_broadcast(server_thread):
    clients = [socket.socket() for _ in range(3)]
    for c in clients:
        c.connect(('127.0.0.1', 65432))
        _ = c.recv(1024)
        _ = c.recv(1024)

    clients[0].sendall(b"Hello")
    for c in clients:
        data = c.recv(1024).decode()
        assert "Hello" in data

    for c in clients:
        c.close()