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

# Creates a frame to hold chat log and input row
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Creates the chat display area
chat_log = scrolledtext.ScrolledText(
    left_frame, width=50, height=20, state='disabled'
)
chat_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Creates the display input and buttons
bottom_frame = tk.Frame(left_frame)
bottom_frame.pack(side=tk.TOP, fill=tk.X)

# Creates message input and buttons in bottom_frame
input_box = tk.Entry(bottom_frame, width=40)
send_button = tk.Button(bottom_frame, text="Send", width=10)
connect_button = tk.Button(bottom_frame, text="Connect", width=10)

input_box.pack(side=tk.LEFT, padx=5, pady=(0,10))
send_button.pack(side=tk.LEFT, padx=5, pady=(0,10))
connect_button.pack(side=tk.LEFT, padx=5, pady=(0,10))

# Creates connected users list
user_listbox = tk.Listbox(root, width=15)
user_listbox.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10), pady=10)
user_listbox.insert(tk.END, "Users:")

# Receives messages in a background thread and updates the GUI.
def receive_messages():
    global user_id
    while True:
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                break

            # Updates the online users list
            if data.startswith("USERS:"):
                ids = data.split(":", 1)[1].split(",")
                user_listbox.delete(0, tk.END)
                user_listbox.insert(tk.END, "Users:")
                for uid in ids:
                    if uid:
                        user_listbox.insert(tk.END, uid)
                continue

            # Displays user ID as assigned.
            if data.startswith("ID:") and user_id is None:
                user_id = data.split(":", 1)[1]
                root.title(f"PyChat Client — ID {user_id}")
                chat_log.config(state='normal')
                chat_log.insert('end', f"[System] Your user ID: {user_id}\n")
                chat_log.config(state='disabled')
                chat_log.yview('end')
                continue

            # Displays broadcasted or private messages.
            chat_log.config(state='normal')
            chat_log.insert('end', data + "\n")
            chat_log.config(state='disabled')
            chat_log.yview('end')

        except:
            break

# Sends user messages to the server.
def send_message():
    msg = input_box.get().strip()
    if msg and client_socket:
        client_socket.sendall(msg.encode('utf-8'))
        input_box.delete(0, tk.END)

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

# Opens private messaging on click.
def on_user_select(event):
    selection = event.widget.curselection()
    if selection:
        idx = selection[0]
        target_uid = event.widget.get(idx)
        if target_uid != "Users:":
            input_box.delete(0, tk.END)
            input_box.insert(0, f"/msg {target_uid} ")
            input_box.focus()

# Wires up buttons and listbox events
send_button.config(command=send_message)
connect_button.config(command=connect_to_server)
input_box.bind('<Return>', lambda e: send_message())
user_listbox.bind('<<ListboxSelect>>', on_user_select)

# Auto connect on startup.
root.after(100, connect_to_server)

root.mainloop()