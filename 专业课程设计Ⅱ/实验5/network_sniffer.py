import threading
import tkinter as tk
from tkinter import ttk
import datetime
from kamene.all import *

# 创建GUI窗口
window = tk.Tk()
window.title("网络数据包抓取器")
window.geometry("800x600")

# 设置过滤条件的输入框
filter_entry = ttk.Entry(window, width=50)
filter_entry.pack()

# 网络接口选择栏
interface_var = tk.StringVar(window)
interface_var.set("")  # 设置默认值为空
interface_label = ttk.Label(window, text="选择网络接口:")
interface_label.pack()
interface_option_menu = ttk.OptionMenu(window, interface_var, "")
interface_option_menu.pack()

# 数据包列表框架
packet_frame = ttk.Frame(window)
packet_frame.pack()

# 创建数据包列表
packet_list_tree = ttk.Treeview(packet_frame, columns=("No.", "Time", "Source", "Destination", "Source Port", "Destination Port", "Length"), show="headings")
packet_list_tree.heading("No.", text="No.")
packet_list_tree.heading("Time", text="Time")
packet_list_tree.heading("Source", text="Source")
packet_list_tree.heading("Destination", text="Destination")
packet_list_tree.heading("Source Port", text="Source Port")
packet_list_tree.heading("Destination Port", text="Destination Port")
packet_list_tree.heading("Length", text="Length")
packet_list_tree.pack(side=tk.LEFT, fill=tk.BOTH)

# 创建垂直滚动条
scrollbar = ttk.Scrollbar(packet_frame, orient=tk.VERTICAL, command=packet_list_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
packet_list_tree.configure(yscrollcommand=scrollbar.set)

# 设置停止抓包的标志
stop_sending = threading.Event()
pause_flag = False  # 暂停标志

# 获取主机上的网络接口列表
interfaces = get_windows_if_list()
interface_names = [interface["name"] for interface in interfaces if interface.get("name")]
interface_var.set(interface_names[0])  # 设置默认值为第一个接口
interface_option_menu['menu'].delete(0, 'end')  # 清空选项菜单
for interface_name in interface_names:
    interface_option_menu['menu'].add_command(label=interface_name, command=tk._setit(interface_var, interface_name))

# 抓包处理函数
def process_packet(packet):
    global packet_list_tree
    if not pause_flag:
        # 处理抓到的数据包
        packet_no = packet_list_tree.insert("", "end", values=("", "", "", "", "", "", ""))  # 插入新行到数据包列表

        # 处理时间字段
        packet_time = packet.time
        if not isinstance(packet_time, datetime.datetime):
            packet_time = datetime.datetime.fromtimestamp(packet_time)
        packet_time = packet_time.strftime("%Y-%m-%d %H:%M:%S")  # 修改时间格式为"年-月-日 时:分:秒"

        # 获取IP层和TCP/UDP层信息
        if IP in packet:
            ip_layer = packet[IP]
            src = ip_layer.src
            dst = ip_layer.dst

            if TCP in packet:
                tcp_layer = packet[TCP]
                src_port = tcp_layer.sport
                dst_port = tcp_layer.dport
                length = ip_layer.len
            elif UDP in packet:
                udp_layer = packet[UDP]
                src_port = udp_layer.sport
                dst_port = udp_layer.dport
                length = ip_layer.len
            else:
                src_port = ""
                dst_port = ""
                length = ""

            # 更新数据包列表中的对应行
            packet_list_tree.set(packet_no, "No.", packet_list_tree.index(packet_no) + 1)  # 更新编号
            packet_list_tree.set(packet_no, "Time", packet_time)
            packet_list_tree.set(packet_no, "Source", src)
            packet_list_tree.set(packet_no, "Destination", dst)
            packet_list_tree.set(packet_no, "Source Port", src_port)
            packet_list_tree.set(packet_no, "Destination Port", dst_port)
            packet_list_tree.set(packet_no, "Length", length)

            packet_list_tree.yview_moveto(1.0)  # 自动滚动到底部

# 开始抓包
def capture_packet():
    global stop_sending, pause_flag
    stop_sending.clear()
    pause_flag = False

    # 清空数据包列表
    packet_list_tree.delete(*packet_list_tree.get_children())

    # 获取过滤条件
    filters = filter_entry.get()

    def capture_thread():
        packet_count = 0
        while not stop_sending.is_set():
            if pause_flag:
                continue

            packet = sniff(filter=filters, count=1, iface=interface_var.get())
            if packet:
                process_packet(packet[0])

            packet_count += 1
            if packet_count % 100 == 0:  # 每抓到100个数据包更新一次标题
                window.title("网络数据包抓取器 - 已抓到{}个数据包".format(packet_count))

    capture_thread = threading.Thread(target=capture_thread)
    capture_thread.start()

    # 更新界面按钮状态
    capture_button.config(text="停止抓包", command=stop_capture)
    pause_button.config(state=tk.NORMAL)

    # 更新界面标题
    window.title("网络数据包抓取器 - 已抓到{}个数据包".format(packet_count))

def stop_capture():
    global stop_sending
    stop_sending.set()

    # 更新界面按钮状态
    capture_button.config(text="开始抓包", command=capture_packet)
    pause_button.config(state=tk.DISABLED)

    # 更新界面标题
    window.title("网络数据包抓取器")

def pause_capture():
    global pause_flag
    pause_flag = not pause_flag

    # 更新按钮文本
    if pause_flag:
        pause_button.config(text="继续抓包")
    else:
        pause_button.config(text="暂停抓包")

def clear_packets():
    packet_list_tree.delete(*packet_list_tree.get_children())

# 创建抓包按钮
capture_button = ttk.Button(window, text="开始抓包", command=capture_packet)
capture_button.pack()

# 创建暂停按钮
pause_button = ttk.Button(window, text="暂停抓包", command=pause_capture, state=tk.DISABLED)
pause_button.pack()

# 创建清空数据包按钮
clear_button = ttk.Button(window, text="清空数据包", command=clear_packets)
clear_button.pack()

# 开始主循环
window.mainloop()
