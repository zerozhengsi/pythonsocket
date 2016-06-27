#coding=utf-8
'''
Created on 2016年6月27日

@author: Administrator
'''
import sys
import socket
import getopt
import threading
import subprocess

listen              = False
command             = False
upload              = False
execute             = False
target              = ""
upload_destination  = ""
port                = 0

def client_sender(client_buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        client.connect((target,port))
        if len(client_buffer):
            client.send(client_buffer)
            
        while True:
            recv_len = 1
            response = ""
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
                
            print response
            
            #等待更多输入
            client_buffer = raw_input("")
            client_buffer += "\n"
            
            client.send(client_buffer)
            
    except:
        print "[*] exception! exiting"
        client.close()
        
        
def server_loop():
    global target
    
    #如果没有定义目标，那我们监听所有接口
    if not len(target):
        target ="0.0.0.0"
        
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    while True:
        client_socket,addr = server.accept()
        
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()
        
def run_command(command):
    #换行
    command = command.rstrip()
    
    #运行命令并将输出返回
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        
    except:
        output = "failed to execute command. \r\n"
        
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    
    #检查上传文件
    if len(upload_destination):
        file_buffer = ""
        
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
                
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            #确认文件已经写
            client_socket.send("successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("failed saved file to %s\r\n" % upload_destination)
            
    
    #检查命令执行
    if len(execute):
        #运行命令
        output = run_command(execute)
        client_socket.send(output)
        
    #如果需要执行SHELL，那么进行另一个循环
    if command:
        while True:
            #跳出一个窗口
            client_socket.send("<BHP:#> ")
            
            #接收文件直到发现换行符(enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                
                #返还命令输出
                response = run_command(cmd_buffer)
                #返回响应数据
                client_socket.send(response)
                

            
            
        
