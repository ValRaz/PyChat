# Overview

For this project, I set out to deepen my understanding of networking fundamentals, concurrency, and GUI development by building PyChat, a real-time chat application in Python. PyChat allows multiple users to connect to a central server, exchange public broadcast messages, and send private one-to-one messages using a simple text protocol.

To use PyChat:

1. **Start the server**
   cd server
   python server.py
2. **Launch one or more clients**
   cd client
   python client.py

Each client window will automatically connect, receive a unique 6-digit User ID, and display the live list of connected users. Type a message into the input box and press **Send** (or hit Enter) to broadcast publicly. Click on a username in the list to prefill a `/msg <UserID> ` command for private messaging.

I built this software to practice low-level TCP socket programming, thread-safe server design, interactive GUI construction with Tkinter, and automated testing with pytest.

[Software Demo Video](https://www.youtube.com/watch?v=Zpo5Pu6H6r8)

# Network Communication

I implemented a **Client-Server** architecture over **TCP** on port **65432** bound to `127.0.0.1`. Messages are newline-delimited UTF-8 text.

* **Handshake**
  Server → Client:
  Welcome to PyChat Server!
  ID:<6-digit-UID>
  USERS:<UID1>,<UID2>,…

* **Public Broadcast**
  Client → Server: `<message>\n`
  Server → All Clients: `<UID>: <message>\n`

* **Private Messaging**
  Client → Server: `/msg <targetUID> <text>\n`
  Server → Recipient: `[Private] <senderUID>: <text>\n`
  Server → Sender (echo): `[Private] To <targetUID>: <text>\n`

# Development Environment

* **Editor/IDE:** Visual Studio Code (with Python extension)
* **Language:** Python 3.13
* **Libraries & Tools:**

  * Standard library: `socket`, `threading`, `tkinter` (with `scrolledtext`)
  * Third-party: `ntplib` for NTP timestamping; `pytest`, `pytest-socket` for testing

# Useful Websites

* [Python Tkinter Official Documentation](https://docs.python.org/3/library/tkinter.html)
* [TkDocs Tutorial](https://tkdocs.com/tutorial/)
* [Real Python: Python GUI Programming with Tkinter](https://realpython.com/python-gui-tkinter/)
* [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
* [pytest Documentation](https://docs.pytest.org/)


# Future Work

* Add encryption for secure messaging
* Enable file and image transfers between clients
* Support multiple chat rooms or channels
* Improve error handling, reconnection logic, and idle timeouts
