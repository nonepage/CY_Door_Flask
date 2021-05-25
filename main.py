import socket  # 导入 socket 模块
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import time


def send_to_open():
    global c

    a1 = "01 0F 00 00 00 04 01 00 3E 96"
    a2 = "01 05 00 02 FF 00 2D FA"
    a3 = "01 05 00 03 FF 00 7C 3A"
    a4 = "01 0F 00 00 00 04 01 00 3E 96"

    print(bytes.fromhex(a1))
    c.send(bytes.fromhex(a1))
    time.sleep(0.5)

    print(bytes.fromhex(a2))
    c.send(bytes.fromhex(a2))
    time.sleep(0.5)

    print(bytes.fromhex(a3))
    c.send(bytes.fromhex(a3))
    time.sleep(3)

    print(bytes.fromhex(a4))
    c.send(bytes.fromhex(a4))


def kill_socket():
    global c
    c.close()


def connect():
    s = socket.socket()  # 创建 socket 对象
    host = "192.168.10.53"  # 获取本地主机名
    port = 6666  # 设置端口
    s.bind((host, port))  # 绑定端口
    s.listen(1)  # 等待客户端连接
    a, addr = s.accept()  # 建立客户端连接
    return a


# 按间距中的绿色按钮以运行脚本。
def open_door_test():
    # 全局变量
    # qos：互斥锁
    # c： socket连接对象
    global c
    global qos
    if qos == 1:

        qos = 0
        try:
            send_to_open()

        except:
            print('关闭了正在占线的链接！')
            kill_socket()
            print('关闭实例')

            c = connect()
            print('新建实例')

            send_to_open()
            print('重新开门')

        qos = 1


app = Flask(__name__)
c = connect()
qos = 1


@app.route('/', methods=['GET', 'POST'])
def index():
    open_door_test()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=14725, host='0.0.0.0')