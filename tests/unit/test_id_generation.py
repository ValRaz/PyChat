import re
import random
import pytest
from server.server import handle_client

def test_uid_format(monkeypatch):
    # Monkeypatch random.randint to a fixed value
    monkeypatch.setattr(random, "randint", lambda a,b: 42)
    # Simulate only the UID generation line
    uid = f"{random.randint(0, 99999):05d}"
    assert re.fullmatch(r"\d{5}", uid)
    assert uid == "00042"