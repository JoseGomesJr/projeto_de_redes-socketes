#!/bin/python3
from ast import Str
from re import T
import re
import socket

FORMAT = "utf-8"

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
                client.sendall(bytes)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))

welc = str(input("Digite seu nome: "))
bwelc = welc.encode()
client.send(bwelc)

def recv():
        str1 = "ENV"
        to_receive = 50
        bMsg_f = str1.encode("utf-8")
        client.send(bMsg_f)
        test= open("olha.txt", 'w')
        bytes_read = client.recv(min(to_receive, 4096)).decode(FORMAT)
        test.write( str(bytes_read.encode(FORMAT)) )


while(True):
        msg = str(input("msg: "))
        if(msg == "RECV"):
             recv()
        elif (msg == "ENV"):
                msg = str(input("NOME: "))   
                send_file(msg)

client.close()


#print(from_server)