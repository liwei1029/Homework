import socket
import tkinter as tk

server_port = 12345
server_sock = None
client_sock = None
command_entry = None
result_text = None

def start_server(server_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', server_port))
        s.listen(1)
        print("Server started and listening on port", server_port)
        return s
    except Exception as e:
        print("Error starting the server: ", str(e))
        return None

def accept_connection(server_sock):
    try:
        client_sock, client_address = server_sock.accept()
        print("Connection accepted from", client_address)
        return client_sock
    except Exception as e:
        print("Error accepting connection: ", str(e))
        return None

def send_data(sock, data):
    try:
        sock.send(data.encode())
    except Exception as e:
        print("Error sending data: ", str(e))

def receive_data(sock):
    try:
        data = sock.recv(1024).decode()
        return data
    except Exception as e:
        print("Error receiving data: ", str(e))
        return None

def execute_command():
    global client_sock

    command = command_entry.get()
    send_data(client_sock, command)

    if command == "exit":
        client_sock.close()
        server_sock.close()
        root.quit()

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Executing command: " + command + "\n\n")
    result_text.config(state=tk.DISABLED)

    result = receive_data(client_sock)
    result_text.config(state=tk.NORMAL)
    result_text.insert(tk.END, result + "\n")
    result_text.config(state=tk.DISABLED)

def clear_output():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

def main():
    global server_sock, client_sock, command_entry, result_text

    server_sock = start_server(server_port)
    if server_sock is None:
        return

    client_sock = accept_connection(server_sock)
    if client_sock is None:
        server_sock.close()
        return

    root = tk.Tk()
    root.title("Remote Control")

    command_frame = tk.Frame(root)
    command_frame.pack()

    command_label = tk.Label(command_frame, text="Enter command:")
    command_label.pack(side=tk.LEFT)

    command_entry = tk.Entry(command_frame, width=50)
    command_entry.pack(side=tk.LEFT)
    command_entry.focus()

    execute_button = tk.Button(root, text="Execute", command=execute_command)
    execute_button.pack()

    clear_button = tk.Button(root, text="Clear", command=clear_output)
    clear_button.pack()

    result_text = tk.Text(root, height=20, wrap=tk.WORD)
    result_text.pack(fill=tk.BOTH, expand=True)
    result_text.config(state=tk.DISABLED)

    root.mainloop()

if __name__ == '__main__':
    main()
