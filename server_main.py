from audioop import mul
from email.utils import localtime
from random import random, randrange
import socket
from _thread import * 
from datetime import datetime       #https://www.programiz.com/python-programming/datetime/current-time


#get local ip adress and start in port 81 hosting of tcp server
ServerSideSocket = socket.socket()
server_ipaddr = socket.gethostbyname(socket.gethostname())
server_port = 81
max_multi_connections = 10              #connections at the same time 
try:
    ServerSideSocket.bind((server_ipaddr, server_port))
except Exception as err:
    print(err)
ServerSideSocket.listen(max_multi_connections)       #how many clients can connect in one session 

print(f'Server online on {server_ipaddr}:{server_port} with max {max_multi_connections} connections.')

#reset the session_database
# code to delete entire data 
# but not the file, it is in
# open file 
f = open("Database/session_database.txt", "r+") 
# absolute file positioning
f.seek(0) 
# to erase all data 
f.truncate() 



#login session for a client
def multi_threaded_client(client_connection):
    while True:
        #server wait for login data from client
        data = client_connection.recv(2048)
        client_msg = data.decode('utf-8')
        print(f'{client_address}:{datetime.now().strftime("%H:%M:%S")}:>> {client_msg}')       #server log with client ip, time, login data
        
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
        file.close
        
        
    
        #check if user_input is in user_database
        if  user_client_request in login_info.keys():   
                   
            if (login_info[user_client_request] == password_client_request):        #check if password is from this user

                #Send session key for secure requests
                session_key = f"{randrange(10000000000, 99999999999)}"
                client_connection.sendall(str.encode(f"Login successful:{session_key}"))
                #save sessionkey in cache file that client can authenicate
                with open('Database/session_database.txt', 'a') as add_last_line:
                    add_last_line.write(f'{user_client_request}, {session_key}\n')
                add_last_line.close()
                
            else:
                response = "Login Error:Wrong Password"
                client_connection.sendall(str.encode(response))
                
        else:
            response = "Login Error:Wrong Username"
            client_connection.sendall(str.encode(response))
            
        if not data:
            break
        
    client_connection.close()


#if new client connect start a client login session
while True:
    client_connection, client_address = ServerSideSocket.accept()
    print(f'Connected from {client_address} at {datetime.now().strftime("%H:%M:%S")}')
    start_new_thread(multi_threaded_client, (client_connection, ))
    
ServerSideSocket.close()
  
    