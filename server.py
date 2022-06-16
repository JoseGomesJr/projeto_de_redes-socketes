#!/bin/python2.7
import socket
from threading import Thread


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.0.6', 8080))
serv.listen(5)

def task():
    while True:
        conn, addr = serv.accept()
        from_client = ''
        welc_user = conn.recv(4096)
        print("Welcome " + welc_user)

        while True:
            data = conn.recv(4096)
            if not data: break
            from_client = data
            print(welc_user + ": " +from_client)

        conn.close()
        print (welc_user + " disconnected")


thread1 = Thread(target=task)
thread2 = Thread(target=task)

thread1.start()
thread2.start()