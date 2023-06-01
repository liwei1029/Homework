import time
import socket
import threading
import tkinter as tk
from ipaddress import ip_network
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

# 验证IP地址是否有效
def is_valid_ip(ip):
    try:
        ip_network(ip)
        return True
    except ValueError:
        return False

# 扫描指定IP的端口
def scan_ip(ip, port_min, port_max, update_progress):
    for port in range(port_min, port_max):
        # 进行端口连接和处理
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((str(ip), port))
        if result == 0:
            info = "Find --> [IP]: %s, [PORT]: %s" % (ip, port)
            result_text.insert(tk.END, info + "\n")
            result_text.see(tk.END)  # 滚动到末尾
        sock.close()

    update_progress(100)  # 扫描完成，更新进度为100%

# 扫描指定网段的端口
def scan_ip_range(ip_range, port_min, port_max, update_progress):
    ip_list = list(ip_network(ip_range).hosts())

    total_ips = len(ip_list)
    completed_ips = 0

    for ip in ip_list:
        if stop_scan_flag:
            break

        scan_ip(ip, port_min, port_max, update_progress)

        completed_ips += 1
        progress = int((completed_ips / total_ips) * 100)
        update_progress(progress)

# 开始扫描
def start_scan():
    global stop_scan_flag

    ip = entry_ip.get()
    ip_range = entry_ip_range.get()
    port_min = int(entry_port_min.get())
    port_max = int(entry_port_max.get())
    num_threads = int(entry_threads.get())

    if scan_mode_var.get() == "single_ip":
        if not is_valid_ip(ip):
            result_text.insert(tk.END, "请输入正确的IP地址\n")
            return

        result_text.insert(tk.END, f"开始扫描 IP: {ip}\n")

        # 创建一个后台线程执行扫描任务
        def run_scan():
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                executor.submit(scan_ip, ip, port_min, port_max, update_progress)

        # 创建后台线程并启动扫描任务
        scan_thread = threading.Thread(target=run_scan)
        scan_thread.start()

    elif scan_mode_var.get() == "ip_range":
        if not is_valid_ip(ip_range):
            result_text.insert(tk.END, "请输入正确的网段格式\n")
            return

        result_text.insert(tk.END, f"开始扫描网段: {ip_range}\n")
        progress_bar["value"] = 0
        progress_bar["maximum"] = 100

        stop_scan_flag = False

        # 创建一个后台线程执行扫描任务
        def run_scan():
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(scan_ip_range, ip_range, port_min, port_max, update_progress)

        # 创建后台线程并启动扫描任务
        scan_thread = threading.Thread(target=run_scan)
        scan_thread.start()

# 停止扫描
def stop_scan():
    global stop_scan_flag
    stop_scan_flag = True

# 清空状态框
def clear_result():
    result_text.delete(1.0, tk.END)
    progress_bar["value"] = 0

# 更新进度条和进度文本
def update_progress(progress):
    progress_bar["value"] = progress
    progress_text.set(f"扫描进度：{progress}%")
    progress_bar.update()

# 创建界面
def create_ui():
    global entry_ip, entry_ip_range, entry_port_min, entry_port_max, entry_threads, result_text, progress_bar, progress_text, stop_scan_flag, scan_mode_var

    window = tk.Tk()
    window.title("端口扫描工具")

    # 左侧区域：输入框和按键
    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    label_ip = tk.Label(left_frame, text="单个IP地址:")
    label_ip.grid(row=0, column=0, sticky=tk.W, pady=5)

    entry_ip = tk.Entry(left_frame)
    entry_ip.grid(row=0, column=1, pady=5)

    label_ip_range = tk.Label(left_frame, text="网段（CIDR格式）:")
    label_ip_range.grid(row=1, column=0, sticky=tk.W, pady=5)

    entry_ip_range = tk.Entry(left_frame)
    entry_ip_range.grid(row=1, column=1, pady=5)

    label_port_min = tk.Label(left_frame, text="最小端口:")
    label_port_min.grid(row=2, column=0, sticky=tk.W, pady=5)

    entry_port_min = tk.Entry(left_frame)
    entry_port_min.grid(row=2, column=1, pady=5)

    label_port_max = tk.Label(left_frame, text="最大端口:")
    label_port_max.grid(row=3, column=0, sticky=tk.W, pady=5)

    entry_port_max = tk.Entry(left_frame)
    entry_port_max.grid(row=3, column=1, pady=5)

    label_threads = tk.Label(left_frame, text="线程数:")
    label_threads.grid(row=4, column=0, sticky=tk.W, pady=5)

    entry_threads = tk.Entry(left_frame)
    entry_threads.grid(row=4, column=1, pady=5)

    scan_mode_var = tk.StringVar()
    scan_mode_var.set("single_ip")

    single_ip_radio = tk.Radiobutton(left_frame, text="单个IP", variable=scan_mode_var, value="single_ip")
    single_ip_radio.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)

    ip_range_radio = tk.Radiobutton(left_frame, text="网段", variable=scan_mode_var, value="ip_range")
    ip_range_radio.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)

    button_scan = tk.Button(left_frame, text="开始扫描", command=start_scan)
    button_scan.grid(row=7, column=0, columnspan=2, pady=5)

    button_stop = tk.Button(left_frame, text="停止扫描", command=stop_scan)
    button_stop.grid(row=8, column=0, columnspan=2, pady=5)

    button_clear = tk.Button(left_frame, text="清空状态", command=clear_result)
    button_clear.grid(row=9, column=0, columnspan=2, pady=5)

    # 右侧区域：状态框和进度条
    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.LEFT, padx=10, pady=10)

    progress_text = tk.StringVar()
    progress_label = tk.Label(right_frame, textvariable=progress_text)
    progress_label.pack(anchor=tk.W, pady=5)

    progress_bar = ttk.Progressbar(right_frame, length=200, mode='determinate')
    progress_bar.pack(pady=5)

    result_text = tk.Text(right_frame, height=10, width=50)
    result_text.pack()

    window.mainloop()

if __name__ == "__main__":
    stop_scan_flag = False  # 停止扫描标志

    create_ui()
