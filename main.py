import socket  # 导入 socket 模块
from flask import Flask
from flask import render_template
from flask import request
import time
import threading


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
    host = "0.0.0.0"  # 获取本地主机名
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


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程：" + self.name)
        test_connect()
        print("退出线程：" + self.name)


def test_connect():
    global c
    global qos
    a1 = "01 0F 00 00 00 04 01 00 3E 96"

    while True:
        if qos == 1:
            try:
                print('心跳包')
                c.send(bytes.fromhex(a1))
                time.sleep(0.5)
                c.send(bytes.fromhex(a1))
                time.sleep(0.5)
                c.send(bytes.fromhex(a1))
                time.sleep(0.5)
                c.send(bytes.fromhex(a1))
                time.sleep(0.5)
                time.sleep(600)
            except:
                print('关闭了正在占线的链接！')
                kill_socket()
                print('关闭实例')

                c = connect()
                print('新建实例')


app = Flask(__name__)
c = connect()
qos = 1
User_admin = ['qqbot', '1007800006', '2200475850', '1821269010', '1005944615', '1038888008', 'hardware']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get('user') in User_admin:
        open_door_test()
        return render_template('index.html')
    else:
        return render_template('bad.html')


thread1 = myThread(1, "Thread-1")
thread1.start()
app.run(port=14725, host='0.0.0.0')
