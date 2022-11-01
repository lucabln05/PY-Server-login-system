from audioop import mul
from random import random, randrange
import socket
from _thread import *  


ServerSideSocket = socket.socket()
server_ipaddr = socket.gethostbyname(socket.gethostname())
server_port = 81
max_multi_connections = 10
try:
    ServerSideSocket.bind((server_ipaddr, server_port))
except Exception as err:
    print(err)
ServerSideSocket.listen(max_multi_connections)       #how many clients can connect in one session 

print(f'Server online on {server_ipaddr}:{server_port} with max {max_multi_connections} connections.')



#login session for a client
def multi_threaded_client(client_connection):
    client_connection.send(str.encode('Server is working: '))
    while True:
        data = client_connection.recv(2048)
        client_msg = data.decode('utf-8')
        print(f'{client_address}>> {client_msg}')
        
        #split incoming username and password
        try:
            user_client_request, password_client_request = client_msg.split(',')             #https://www.bitdegree.org/learn/python-split
        except Exception:
            user_client_request = "NONE"
            password_client_request = "NONE"
            
    
        #https://stackoverflow.com/questions/67361263/making-a-login-page-using-data-from-a-txt-file
        #read database and check if user and password are in there
        file = open('Database/user_database.txt', 'r')      #open user_database file in read only
        login_info = {}                                     #define a pre list for the database content
        #splite username and password in each line and add them in login_info list
        for line in file:
            database_user, database_password = line.split(',')
            database_password = database_password.strip()
            login_info[database_user] = database_password
    
        #check if user_input is in user_database
        if  user_client_request in login_info.keys():          
            if (login_info[user_client_request] == password_client_request):
                #Send session key for secure requests
                session_key = f"{randrange(10000000000, 99999999999)}"
                client_connection.sendall(str.encode(session_key))
            else:
                response = "Login Error"
                client_connection.sendall(str.encode(response))
        else:
            response = "Login Error"
            client_connection.sendall(str.encode(response))
        
        
        if not data:
            break
    client_connection.close()


#if new client connect start a client login session
while True:
    client_connection, client_address = ServerSideSocket.accept()
    print(f'Connected from {client_address}')
    start_new_thread(multi_threaded_client, (client_connection, ))
    
ServerSideSocket.close()
  
    