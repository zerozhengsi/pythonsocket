#coding=utf-8
'''
Created on 2016年6月23日

@author: Administrator
'''
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5) 

print "[*] listening on %s%d" % (bind_ip,bind_port)

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "[*] received: %s" % request
    client_socket.send("ACK!")
    client_socket.close()

while True:
    client,addr = server.accept()
    
    print "[*] accepted connection from: %s%d" % (addr[0],addr[1])
    
    client_handle = threading.Thread(target=handle_client,args=(client,))
    client_handle.start()