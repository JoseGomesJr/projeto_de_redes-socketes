#!/bin/python2.7
from re import T
import socket
import sys
from threading import Thread
from turtle import delay

FORMAT = "utf-8"
MSG_SEP = "|"

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8080))
serv.listen(5)

class File():
    def __init__(self, filename, filesize):
        self.filename = filename
        self.filesize = filesize

    def white_arq(self, to_receive, conn):

        with open("buff", 'wb+') as file:
            while True:
                if to_receive > 0:
                    print("to_receive")
                    bytes_read = conn.recv(min(to_receive, 4096))               
                    file.write(bytes_read)
                    to_receive -= len(bytes_read)
                else:
                    break

    def read_arq(self):
        arq = open("buff", 'rb+')
        s = arq.read()
        arq.close()
        return s

arq = File(" ", 0 )


def send_file(file, conn):
    print("aquiii")
    filesize, file.filename =  (conn.recv(4096).decode(FORMAT).split(MSG_SEP, 1))

    to_receive = int(filesize)
    file.filesize = to_receive

    file.white_arq(to_receive, conn)

def recv_file(file, conn):
    if file.filename == " " or file.filesize == 0:
        return False
    print(file.filename)
    conn.send(f"{file.filesize}{MSG_SEP}{file.filename}".encode(FORMAT))
    s = file.read_arq()
    conn.sendall(s)
    return True
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
            send_file(arq, conn)
        elif from_client == 'ENV':
            if not recv_file(arq, conn):
                print("Nenhum arquivo encontrado")
            else:
                print("Arquivo enviado")

    conn.close()
    print (str(welc_user) + " disconnected")

if __name__ == "__main__":
    thread1 = Thread(target=task)
    thread2 = Thread(target=task)
    thread1.start()
    thread2.start()
    input("Pressione entre")
    sys.exit()