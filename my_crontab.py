#!/mnt/weka/opt/linux-rocky8-x86_64/gcc-12.2.0/anaconda3-2020.07-yv6vdwqiouaru27jxhpezh6t6mdpqf3e/bin/python3.8
# -*- coding: utf-8 -*-
import time
import os
import subprocess
import datetime
import signal
global global_continue
global_continue = True
global global_process_dict
global_process_dict = {}


def signal_handler(signal, frame):
    # 在捕获到 Ctrl+C 时执行的操作
    global global_continue
    global_continue = False
    print("Ctrl+C 被按下，程序即将退出", global_continue)


# 注册信号处理程序
signal.signal(signal.SIGINT, signal_handler)


def update_status():
    global global_process_dict
    finished_keys = []
    # 等待所有子线程结束后，再退出
    for key in global_process_dict.keys():
        if global_process_dict[key].poll() is None:
            print(key, "进程正在执行")
        else:
            print(key, "已经退出")
            finished_keys.append(key)
    for key in finished_keys:
        global_process_dict.pop(key)


try:
    while global_continue:
        comd = "source ~/.bashrc && source /opt/share/Modules/init/bash && module load singularityce && source source/run.sh > crontab_log"
        # comd = "sleep 1m"
        print(comd)
        time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        # process = subprocess.run(comd, shell = True)
        global_process_dict[time_str] = subprocess.Popen(comd, shell=True)
        print(time_str, 'done', global_continue)
        time.sleep(10)
        update_status()
    print("global_continue = ", global_continue, "exit")
    while len(global_process_dict) > 0:
        print("退出前检查")
        update_status()
        print(global_process_dict)
except KeyboardInterrupt:
    print("Ctrl+C 被按下，等待自动退出")
