# 键盘和鼠标监控系统

该项目由客户端程序和服务器端程序组成，可以实现对远程主机上键盘和鼠标事件的实时监控。客户端程序捕获事件并将其发送到服务器端进行显示。



## 特点

- 监控和记录客户端计算机上的键盘和鼠标事件。
- 使用网络接口将监控结果发送到远程服务器。
- 在服务器端实时显示接收到的结果。

## 前提条件

- Python 3.x
- `socket` 模块
- `pynput` 库
- `tkinter` 模块
- `pyautogui` 库

## 使用方法

1. 克隆仓库或下载 `client.py` 和 `server.py` 文件。
    在安装之前，需要确保已经安装了 `pip` 工具。 使用以下命令安装所需的依赖库： 

    ```
     pip install pynput tkinter pyautogui
    ```

    

2. 在 `client.py` 和 `server.py` 文件中配置主机和端口：

    - 在 `client.py` 中：
    
        ```python
        HOST = 'xxx.xxx.xxx.xxx'  # 替换为服务器的 IP 地址
        PORT = 6875  # 替换为所需的端口号
        ```

    - 在 `server.py` 中：
    
        ```python
        HOST = 'xxx.xxx.xxx.xxx'  # 替换为服务器的 IP 地址
        PORT = 6875  # 替换为所需的端口号
        ```

3. 在服务器机器上运行 `server.py` 文件：

    ```bash
    python server.py
    ```

4. 在客户端机器上运行 `client.py` 文件：

    ```bash
    python client.py
    ```

5. 客户端程序将开始监控客户端机器上的键盘和鼠标事件。事件将被发送到服务器并实时显示。

6. 服务器程序将接收来自客户端的事件并在图形用户界面（GUI）中显示。服务器 GUI 将实时显示键盘和鼠标事件。

7. 要停止程序，请关闭服务器 GUI 或在服务器终端上按下 `Ctrl+C`。



## 注意

在作者测试时server端运行在Windows10，client端运行在Kali Linux2022中