import socket

# Server config
HOST = '127.0.0.1'
PORT = 65432

# Connects to PyChat TCP server, prints received welcome message. Dev testing phase 
def test_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        response = client_socket.recv(1024)
        print(f"[PyChat Client] Received: {response.decode()}")

if __name__ == "__main__":
    test_connection()