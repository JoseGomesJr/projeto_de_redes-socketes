#!/bin/python3
import os
from re import T
import re
import socket
import time

FORMAT = "utf-8"
MSG_SEP = "|"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

def send_file(filename):
    try:
        file = open(filename, 'rb')
    except PermissionError:
        print("Not Can't open file")
        return
    else:
        with file:
                bytes = file.read()
                str = "RECV"
                bMsg_f = str.encode("utf-8")
                client.send(bMsg_f)
                file_size = os.path.getsize(filename)
                print(file_size)
                client.send(f"{file_size}{MSG_SEP}{filename}".encode(FORMAT))
                time.sleep(0.5)
                client.sendall(bytes)

def recv():
        str1 = "ENV"
        to_receive = 50
        bMsg_f = str1.encode("utf-8")
        client.send(bMsg_f)
        filesize, filename = client.recv(4096).decode(FORMAT).split(MSG_SEP, 1)
        to_receive = int(filesize)
        with open(filename, 'wb+') as file:
                print(filename)
                while True:
                        if to_receive > 0:
                                bytes_read = client.recv(min(to_receive, 4096))               
                                file.write(bytes_read)
                                to_receive -= len(bytes_read)
                        else:
                                break
        #bytes_read = client.recv(min(to_receive, 4096)).decode(FORMAT)
        #test.write( str(bytes_read.encode(FORMAT)) )


def main():

        welc = str(input("Digite seu nome: "))
        bwelc = welc.encode()
        client.send(bwelc)
        while(True):
                msg = str(input("msg: "))
                if(msg == "RECV"):
                        recv()
                elif (msg == "ENV"):
                        msg = str(input("NOME: "))   
                        send_file(msg)
                elif (msg == "END"):
                        client.close()

if __name__ == "__main__":
    main()

#print(from_server)