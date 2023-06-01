import tkinter as tk
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import threading
import time


def send_email():
    # 获取用户填写的信息
    mail_host = 'smtp.qq.com'
    mail_user = mail_user_entry.get()
    mail_pws = mail_pws_entry.get()
    my_mail = my_mail_entry.get()
    her_mail = her_mail_entry.get()
    cont = content_entry.get("1.0", tk.END)
    title = title_entry.get()
    send_count = int(send_count_entry.get())
    interval = int(interval_entry.get())

    # 创建计数器变量
    counter = 0

    # 更新计数器的值
    def update_counter():
        nonlocal counter
        counter += 1
        counter_value_label.config(text=str(counter))

    # 发送邮件的函数
    def send_email_thread():
        # 登录
        smtp = SMTP_SSL(mail_host)
        smtp.ehlo(mail_host)
        smtp.login(mail_user, mail_pws)

        for i in range(send_count):
            # 内容格式化
            msg = MIMEText(cont, 'plain', 'UTF-8')
            msg['Subject'] = Header(title, 'UTF-8')
            msg['From'] = my_mail
            msg['To'] = her_mail
            smtp.sendmail(my_mail, her_mail, msg.as_string())

            # 更新计数器的值
            update_counter()

            # 等待指定的时间间隔
            time.sleep(interval)

        smtp.quit()

    # 创建线程来发送邮件
    email_thread = threading.Thread(target=send_email_thread)
    email_thread.start()

# 创建窗口
window = tk.Tk()

# 设置窗口标题
window.title("发送邮件")

# 创建左侧容器
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT)

# 创建右侧容器
right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT)

# 创建标签和文本框
mail_user_label = tk.Label(left_frame, text="账号:")
mail_user_label.grid(row=0, column=0, sticky=tk.W)
mail_user_entry = tk.Entry(left_frame)
mail_user_entry.grid(row=0, column=1)

mail_pws_label = tk.Label(left_frame, text="授权码:")
mail_pws_label.grid(row=1, column=0, sticky=tk.W)
mail_pws_entry = tk.Entry(left_frame)
mail_pws_entry.grid(row=1, column=1)

my_mail_label = tk.Label(left_frame, text="发件人邮箱:")
my_mail_label.grid(row=2, column=0, sticky=tk.W)
my_mail_entry = tk.Entry(left_frame)
my_mail_entry.grid(row=2, column=1)

her_mail_label = tk.Label(left_frame, text="收件人邮箱:")
her_mail_label.grid(row=3, column=0, sticky=tk.W)
her_mail_entry = tk.Entry(left_frame)
her_mail_entry.grid(row=3, column=1)

# 创建标题和内容标签
title_label = tk.Label(right_frame, text="标题:")
title_label.grid(row=0, column=0, sticky=tk.W)
content_label = tk.Label(right_frame, text="邮件内容:")
content_label.grid(row=1, column=0, sticky=tk.W)

# 创建标题和内容文本框
title_entry = tk.Entry(right_frame)
title_entry.grid(row=0, column=1)
content_entry = tk.Text(right_frame, height=10, width=30)
content_entry.grid(row=1, column=1)

send_count_label = tk.Label(left_frame, text="发送数量:")
send_count_label.grid(row=4, column=0, sticky=tk.W)
send_count_entry = tk.Entry(left_frame)
send_count_entry.grid(row=4, column=1)

interval_label = tk.Label(left_frame, text="发送时间间隔（秒）:")
interval_label.grid(row=5, column=0, sticky=tk.W)
interval_entry = tk.Entry(left_frame)
interval_entry.grid(row=5, column=1)

# 创建计数器标签
counter_label = tk.Label(left_frame, text="已发送的邮件数量:")
counter_label.grid(row=6, column=0, sticky=tk.W)
counter_value_label = tk.Label(left_frame, text="0")
counter_value_label.grid(row=6, column=1, sticky=tk.W)

# 创建按钮
send_button = tk.Button(left_frame, text="发送邮件", command=send_email)
send_button.grid(row=7, column=0, columnspan=2)

# 运行窗口主循环
window.mainloop()
