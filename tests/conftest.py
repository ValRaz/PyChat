import os
import sys

# 1) Prepend the project root (one level above tests/) to sys.path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pytest
from server.server import clients, clients_lock, user_sockets

@pytest.fixture(autouse=True)
def clear_server_state():
    # Before each test: close any lingering conns and clear state
    with clients_lock:
        for conn in clients:
            try: conn.close()
            except: pass
        clients.clear()
        user_sockets.clear()
    yield
    # After each test: same cleanup
    with clients_lock:
        for conn in clients:
            try: conn.close()
            except: pass
        clients.clear()
        user_sockets.clear()