import tkinter as tk
from tkinter import scrolledtext
import socket, threading
import ntplib

# Sets up global networking and NTP client
client_socket = None
ntp_client    = ntplib.NTPClient()
user_id       = None  

# Sets up GUI and networking.
root = tk.Tk()
root.title("PyChat Client")

chat_log = scrolledtext.ScrolledText(root, width=50, height=20, state='disabled')
chat_log.pack(padx=10, pady=10)

input_box = tk.Entry(root, width=40)
input_box.pack(side=tk.LEFT, padx=(10,0), pady=5)

connect_button = tk.Button(root, text="Connect", width=10)
connect_button.pack(side=tk.LEFT, padx=5, pady=5)
send_button = tk.Button(root, text="Send", width=10)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

# Receives messages in a background thread and updates the GUI.
def receive_messages():
    global user_id
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Displays assigned user ID when first received.
            if data.startswith("ID:") and user_id is None:
                user_id = data.split(":", 1)[1]
                root.title(f"PyChat Client — ID {user_id}")
                chat_log.config(state='normal')
                chat_log.insert('end', f"[System] Your user ID: {user_id}\n")
                chat_log.config(state='disabled')
                chat_log.yview('end')
                continue

            # Records NTP-based timestamp.
            ts = ntp_client.request('pool.ntp.org', version=3).tx_time

            # Displays broadcasted messages.
            chat_log.config(state='normal')
            chat_log.insert('end', data + "\n")
            chat_log.config(state='disabled')
            chat_log.yview('end')
        except:
            break

# Connects to the server and changes button to Disconnect.
def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    connect_button.config(text="Disconnect", command=disconnect_from_server)
    threading.Thread(target=receive_messages, daemon=True).start()

# Disconnects from the server and returns button to Connect.
def disconnect_from_server():
    global client_socket
    try:
        client_socket.close()
    except:
        pass
    client_socket = None
    connect_button.config(text="Connect", command=connect_to_server)

# Sends the user-typed message to the server.
def send_message():
    msg = input_box.get().strip()
    if msg and client_socket:
        client_socket.sendall(msg.encode('utf-8'))
        input_box.delete(0, tk.END)

connect_button.config(command=connect_to_server)
send_button.config(command=send_message)
input_box.bind('<Return>', lambda e: send_message())

# Auto connect on startup.
root.after(100, connect_to_server)

root.mainloop()






