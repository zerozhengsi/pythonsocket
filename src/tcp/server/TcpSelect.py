#coding=utf-8
'''
Created on 2016年6月23日

@author: Administrator
'''
import socket
import select

bind_ip = "0.0.0.0"
bind_port = 9000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5) 

print "[*] listening on %s%d" % (bind_ip,bind_port)

inputs = [server, ]
outputs = []
message_dict = {}

# def handle_client(client_socket):
#     request = client_socket.recv(1024)
#     print "[*] received: %s" % request
#     print "[*] received length: %s" % len(request)
#     start,length,code = struct.unpack("<ci6s",request[0:11])
#     print "[*] received start: %s" % start
#     print "[*] received length: %s" % length
#     print "[*] received code: %s" % code
#     samp = "%ssc" % length
#     message,end = struct.unpack(samp,request[11:11+length+1])
#     print "[*] received message: %s" % message
#     print "[*] received end: %s" % end
#     
#     client_socket.send("ok!")
#     client_socket.close()

while True:
    print "waiting for the next event"
    r_list, w_list, e_list = select.select(inputs, outputs, inputs, 1)
    for sk1_or_conn in r_list:
        if sk1_or_conn == server:
            conn, address = sk1_or_conn.accept()
            print "connection from:",address
            inputs.append(conn)
        else:
            try:
                data_bytes = sk1_or_conn.recv(1024)
                if data_bytes:
                    print "received %s from:%s" % (data_bytes,sk1_or_conn.getpeername())
                else:
                    if sk1_or_conn not in outputs:
                        outputs.append(sk1_or_conn)
                    
            except Exception as ex:
                print "delete conn"
                inputs.remove(sk1_or_conn)
            