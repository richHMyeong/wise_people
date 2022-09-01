import socket
import json

comSocket = socket.socket()

svrIP = "127.0.0.1"
comSocket.connect((svrIP,5000))
print('Connected to '+svrIP)

while True:
   sendData = input(("Sending message: "))
   comSocket.send(sendData.encode()) #bytes형으로 변환하여 전송

   #bytes형으로 수신된 데이터를 문자열로 변환 출력
   print('Received message: {0}'.format(json.loads(comSocket.recv(1024).decode())))