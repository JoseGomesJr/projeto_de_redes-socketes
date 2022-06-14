import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.3', 8080))
msg = "xabusco no bitico"
bMsg = msg.encode()
client.send(bMsg)
from_server = client.recv(4096)
client.close()
print(from_server)