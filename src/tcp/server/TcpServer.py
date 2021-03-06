#coding=utf-8
'''
Created on 2016年6月23日

@author: Administrator
'''
import socket
import threading
import struct

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5) 

print "[*] listening on %s%d" % (bind_ip,bind_port)

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "[*] received: %s" % request
    print "[*] received length: %s" % len(request)
    start,length,code = struct.unpack("<ci6s",request[0:11])
    print "[*] received start: %s" % start
    print "[*] received length: %s" % length
    print "[*] received code: %s" % code
    samp = "%ssc" % length
    message,end = struct.unpack(samp,request[11:11+length+1])
    print "[*] received message: %s" % message
    print "[*] received end: %s" % end
    
    client_socket.send("ok!")
    client_socket.close()

while True:
    client,addr = server.accept()
    
    print "[*] accepted connection from: %s%d" % (addr[0],addr[1])
    
    client_handle = threading.Thread(target=handle_client,args=(client,))
    client_handle.start()