import socket

ClientMultiSocket = socket.socket()

host = "192.168.178.179"
port = 81

ClientMultiSocket.connect((host, port))


while True:

    user_name = input('User: ')
    password = input('Password: ')
    login_send = f'{user_name},{password}'
    ClientMultiSocket.send(str.encode(login_send))
    res = ClientMultiSocket.recv(2048)
    login_server_answer = res.decode('utf-8')
    user_msg, session_token = login_server_answer.split(':')
    print(user_msg)
    if user_msg == "Login successful":
        ClientMultiSocket.send(str.encode(session_token))
        
           
        
    
    
ClientMultiSocket.close() 