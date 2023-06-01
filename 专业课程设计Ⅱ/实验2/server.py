import socket
import tkinter as tk
from threading import Thread
from queue import Queue
import pyautogui
from pynput import keyboard

HOST = 'xxx.xxx.xxx.xxx'
PORT = 6875

def start_server():
    def handle_data(data):
        text_box.insert(tk.END, data + '\n')  # 在文本框末尾插入数据

    def on_receive_data(conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                handle_data(data.decode())
                response = "Data received!"
                conn.sendall(response.encode())

    def close_server():
        server_socket.close()
        root.destroy()

    def on_key_event(key):
        key_char = str(key)
        key_queue.put(key_char)

    def on_mouse_event(event):
        action = f"Mouse event: {event}"
        key_queue.put(action)

    def keyboard_listener():
        with keyboard.Listener(on_press=on_key_event) as listener:
            listener.start()

    def mouse_listener():
        with pyautogui.hook(callback=on_mouse_event) as listener:
            listener.start()

    def process_queue():
        while True:
            try:
                data = key_queue.get(block=False)
                if data == 'EXIT':
                    break
                handle_data(data)
            except Queue.Empty:
                pass

    root = tk.Tk()
    root.title("Server")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_box.pack()

    scrollbar.config(command=text_box.yview)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server started, waiting for connections...")

    close_button = tk.Button(root, text="Close Server", command=close_server)
    close_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", close_server)

    key_queue = Queue()

    keyboard_thread = Thread(target=keyboard_listener)
    keyboard_thread.start()

    mouse_thread = Thread(target=mouse_listener)
    mouse_thread.start()

    process_thread = Thread(target=process_queue)
    process_thread.start()

    while True:
        conn, addr = server_socket.accept()
        print("Connected by", addr)
        on_receive_data(conn)

        key_queue.put('EXIT')

        root.update()  # 刷新 GUI 界面

    root.mainloop()

if __name__ == '__main__':
    start_server()
