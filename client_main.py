import socket

ClientMultiSocket = socket.socket()

host = "192.168.178.179"
port = 81

ClientMultiSocket.connect((host, port))


res = ClientMultiSocket.recv(2048)

while True:
    user_name = input('User: ')
    password = input('Password: ')
    login_send = f'{user_name},{password}'
    ClientMultiSocket.send(str.encode(login_send))
    res = ClientMultiSocket.recv(2048)
    sessionkey = res.decode('utf-8')
    print(sessionkey)
ClientMultiSocket.close()