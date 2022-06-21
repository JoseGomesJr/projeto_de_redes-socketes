#!/bin/python2.7
from cmath import e
import socket
from threading import Thread


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8080))
serv.listen(5)


def send_file(file, conn):
    print("aquiii")
    bytes_read = conn.recv(4096)              
    file.write(bytes_read)

def task():
    while True:
        conn, addr = serv.accept()
        from_client = ''
        welc_user = conn.recv(4096)
        print("Welcome " + str(welc_user))
        
        data = conn.recv(4096).decode('utf8')
        if not data: break
        from_client = data
        if from_client == 'RECV':
            arq = open("buff", 'wb+')
            send_file(arq, conn)
            arq.close()
        elif from_client == 'ENV':
            arq = open("buff", 'rb+')
            s = arq.read()
            conn.sendall(s)
            arq.close()

    conn.close()
    print (str(welc_user) + " disconnected")


thread1 = Thread(target=task)
thread2 = Thread(target=task)
thread1.start()
thread2.start()