#!/bin/python3
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.6', 8080))

welc = str(input("Digite seu nome: "))
bwelc = welc.encode()
client.send(bwelc)

while(True):
        msg = str(input("msg: "))
        if(msg == "xaxa"):
                break
        bMsg = msg.encode()
        client.send(bMsg)

client.close()
#print(from_server)