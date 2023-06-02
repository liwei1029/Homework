# Email Sender

这是一个使用 Python 编写的简单的邮件发送程序。



## 功能

- 输入发件人和收件人的邮箱地址、授权信息以及邮件内容和标题。
- 可以设置发送的邮件数量和发送时间间隔。
- 实时显示已发送的邮件数量。
  

## 前提条件

- Python 3.x
- `smtplib` 模块：用于发送电子邮件。
- `email` 模块：用于创建和处理电子邮件的数据。
- `threading` 模块：用于创建和管理线程。
- `time` 模块：用于控制邮件发送的时间间隔。
- `tkinter` 模块：用于创建 GUI 界面。
- `tkinter.scrolledtext` 模块：用于创建可滚动的文本框。
- `tkinter.messagebox` 模块：用于显示消息框。
- `tkinter.ttk` 模块：用于创建更加现代化的 GUI 组件。
- `tkinter.font` 模块：用于自定义字体样式。

请确保您的 Python 环境中已安装这些依赖项。您可以使用以下命令检查某个依赖项是否已安装：

```shell
python -c "import 模块名"
```

如果发现某个依赖项未安装，可以使用以下命令来安装它们：

```shell
pip install secure-smtplib
```

## 使用说明

1.安装所需依赖：

```shell
pip install smtplib
```

2.在 `main.py` 文件中，替换以下变量的值为您自己的信息：

```
mail_user = 'your_email@example.com'  # 发件人邮箱
mail_pws = 'your_password'  # 发件人邮箱授权码
my_mail = 'your_email@example.com'  # 发件人邮箱
her_mail = 'recipient_email@example.com'  # 收件人邮箱
```

※获取QQ邮箱授权码
https://blog.csdn.net/qq_44275213/article/details/128666542

3.运行程序：

```
python EmailSender.py
```

## 生成客户端文件

```shell
pyinstaller --onefile EmailSender.py
```

- 生成的客户端文件在 dist 目录下

## 注意事项

- 请确保您的邮箱提供商允许使用 SMTP 协议发送邮件，并且已启用了相应的服务。
- 请注意合法使用该程序，并遵守相关法律法规和邮箱服务提供商的使用条款。
