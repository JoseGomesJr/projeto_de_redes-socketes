#!/bin/python3
import os
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
        print("Nao foi possivel acessar o arquivo")
        return
    else:
        print(f"Enviando {filename}")
        with file:
            bytes = file.read()
            str = "RECV" + filename
            bMsg_f = str.encode("utf-8")
            client.send(bMsg_f)
            file_size = os.path.getsize(filename)
            client.send(f"{file_size}{MSG_SEP}{filename}".encode(FORMAT))
            time.sleep(0.5)
            client.sendall(bytes)
    print("Arquivo enviado.")

def recv(file_name):
    to_receive = 50
    msg = "SEND" + file_name
    client.send(msg.encode("utf-8"))
    filesize, filename = client.recv(4096).decode(FORMAT).split(MSG_SEP, 1)
    to_receive = int(filesize)
    path = f"./downloads/{file_name}"

    with open(path, 'wb+') as file:
        print(f"Baixando {file_name}")
        while True:
            if to_receive > 0:
                bytes_read = client.recv(min(to_receive, 4096))               
                file.write(bytes_read)
                to_receive -= len(bytes_read)
            else:
                break
        print("Download completo.")

def create_dir():
    if not os.path.isdir("./downloads"):
        os.mkdir("./downloads")

def main():
    print("Arquivos baixandos são enviados para o diretorio src/downloads")
    print("Uso:\n LIST: Listar os arquivos no servidor\n SEND: Enviar um arquivo para o servidor\n RECV: Baixar um arquivo do servidor\n ENDT: Fechar")
    while(True):
        msg = str(input("> "))
        if(msg == "RECV"):
            msg = str(input("NOME DO ARQUIVO: "))
            recv(msg)
        elif (msg == "SEND"):
            msg = str(input("NOME DO ARQUIVO: "))   
            send_file(msg)
        elif (msg == "LIST"):
            bMsg_f = "LIST".encode("utf-8")
            client.send(bMsg_f)
            print(client.recv(4096).decode('utf8'))
        elif (msg == "ENDT"):
            bMsg_f = "ENDT".encode("utf-8")
            client.send(bMsg_f)
            client.close()
            break

if __name__ == "__main__":
    create_dir()
    main()