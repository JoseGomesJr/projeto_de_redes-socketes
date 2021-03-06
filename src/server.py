#!/bin/python2.7
import glob
import socket
import os
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
        path = os.getcwd() + "./files/" + self.filename
        with open(path, 'wb+') as file:
            while True:
                if to_receive > 0:
                    print("to_receive")
                    bytes_read = conn.recv(min(to_receive, 4096))
                    file.write(bytes_read)
                    to_receive -= len(bytes_read)
                else:
                    break

    def read_arq(self):
        t = "./files/" + self.filename
        path = f"./files/{self.filename}"
        arq = open(path, 'rb+')
        s = arq.read()
        arq.close()
        return s


arq = File(" ", 0)


def send_file(file, conn):
    filesize, file.filename = (
        conn.recv(4096).decode(FORMAT).split(MSG_SEP, 1))

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


def task(conn, addr):
    print(f"{addr} connected.")

    while True:
        from_client = ''

        data = conn.recv(4096).decode('utf8')
        if not data:
            break
        from_client = data[0:4]
        arq.filename = data[4:]
        print(f"{from_client},{addr}")
        if from_client == 'RECV':
            send_file(arq, conn)
        elif from_client == 'SEND':
            if not recv_file(arq, conn):
                print("Nenhum arquivo encontrado")
                filesize = 0
                str = "Nenhum arquivo"
                conn.send(f"{filesize}{MSG_SEP}{str}".encode(FORMAT))
            else:
                print("Arquivo enviado")
        elif from_client == 'LIST':
            arr = os.listdir("./files")
            file_list = ""
            for i in arr:
                if (i != ""):
                    arq.filename += i + "\n"
            if(arq.filename != ""):
                conn.send(arq.filename[:-1].encode())
            else:
                conn.send("Diretorio vazio".encode())
            print(arq.filename)
        elif from_client == 'ENDT':
            break
    conn.close()
    print(f"{addr}  disconnected")


if __name__ == "__main__":
    if not os.path.isdir("./files"):
        os.mkdir("./files")
    py_files = glob.glob('./files/*')
    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error")
    while True:
        conn, addr = serv.accept()
        thread1 = Thread(target=task, args=(conn, addr))
        thread1.start()
