# 远程控制程序

这是一个使用Python和Tkinter构建的客户端-服务器远程控制应用程序。它允许您远程在服务器上执行命令并在客户端上查看输出。



## 前提条件

在开始使用远程控制应用程序之前，需要满足以下条件：

- 安装了Python 3.x。您可以从官方网站 [Python官方网站](https://www.python.org/) 下载并安装最新的Python版本。

## 依赖库和模块安装

在使用远程控制应用程序之前，您需要安装以下依赖库和模块：

- `socket` 模块：用于网络通信。

```shell
pip install socket
```

- `pynput` 库：用于监听和控制键盘输入

```shell
pip install pynput
```

- `tkinter` 模块：用于构建图形用户界面（GUI）。
  - 对于Python 3.x，`tkinter` 是标准库，无需额外安装。
- `pyautogui` 库：用于在客户端执行鼠标和屏幕操作。

```shell
pip install pyautogui
```

请确保在安装上述依赖库和模块时使用了正确的命令，并根据您的系统环境进行安装。

## 使用方法

- 在服务器机器上运行`server.py`脚本来启动服务器。

```
python server.py
```

- 在`client.py`脚本中编辑`server_ip`和`server_port`变量，将其设置为服务器的IP地址和端口。

  ```
  def main():
      server_ip = 'xxx.xxx.xxx.xxx'
      server_port = 12345
  ```

- 在客户端机器上运行`client.py`脚本来启动客户端。

```
python client.py
```

- 在命令输入框中输入要执行的命令，并点击“执行”按钮将命令发送到服务器。

  ```shell
  在服务器端，常用的指令操作包括：
  
  文件和目录操作：
  
  列出当前目录下的文件和目录：ls（Linux）或 dir（Windows）
  切换到指定目录：cd <目录路径>
  创建目录：mkdir <目录名>
  删除文件或目录：rm <文件或目录路径>
  复制文件或目录：cp <源文件或目录> <目标文件或目录>
  移动文件或目录：mv <源文件或目录> <目标文件或目录>
  查看文件内容：cat <文件路径>（Linux）或 type <文件路径>（Windows）
  系统信息和状态：
  
  查看系统信息：uname -a（Linux）或 systeminfo（Windows）
  查看进程列表：ps（Linux）或 tasklist（Windows）
  查看网络连接：netstat（Linux）或 netstat -ano（Windows）
  查看系统资源使用情况：top（Linux）或 taskmgr（Windows）
  网络操作：
  
  Ping 测试：ping <目标IP或域名>
  域名解析：nslookup <域名>
  用户和权限管理：
  
  添加用户：adduser <用户名>（Linux）或 net user <用户名> <密码> /add（Windows）
  删除用户：deluser <用户名>（Linux）或 net user <用户名> /delete（Windows）
  修改用户密码：passwd <用户名>（Linux）或 net user <用户名> <新密码>（Windows）
  修改文件权限：chmod <权限设置> <文件路径>（Linux）或 icacls <文件路径> /grant <用户或组>:<权限>（Windows）
  系统管理：
  
  重启系统：reboot（Linux）或 shutdown /r（Windows）
  关闭系统：shutdown（Linux）或 shutdown /s（Windows）
  ```

  

- 命令执行的输出结果将显示在结果文本区域中。

- 要退出客户端和服务器，请在命令输入框中输入“exit”，然后点击“执行”按钮。

## 限制

- 该应用程序假设只有一个客户端与服务器建立连接。
- 服务器监听特定端口，并等待一个客户端连接。
- 客户端使用服务器的IP地址和端口连接到服务器。
- 该应用程序不提供任何身份验证或加密机制。请在受信任的网络环境中使用。
  

## 注意

在作者测试时server端运行在Windows10，client端运行在Kali Linux2022中

**免责声明：使用本工具进行端口扫描时，请遵守法律法规，并仅在合法授权的范围内使用。**
**作者对使用本工具导致的任何问题不承担任何责任。**