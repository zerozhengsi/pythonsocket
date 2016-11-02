#coding=utf-8
'''
Created on 2016年7月8日

@author: Administrator
'''

import socket
import urlparse
import select
import threading

BUFLEN=8192


class Proxy(object):
    def __init__(self,conn,addr):
        self.source=conn
        self.request=""
        self.headers={}
        self.destnation=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.threadName = threading.current_thread().getName()
        self.run()

    def get_headers(self):
        header=''
        while True:
            header+=self.source.recv(BUFLEN)

            print "threadName=%s proxyLocalReceive:\r\n %s \r\n" %(self.threadName,header)
            index=header.find('\n')
            if index >0:
                break
        #firstLine,self.request=header.split('\r\n',1)
        firstLine=header[:index]
        self.request=header[index+1:]
        self.headers['method'],self.headers['path'],self.headers['protocol']=firstLine.split()

    def conn_destnation(self):
        url=urlparse.urlparse(self.headers['path'])
        if "http"==url[0]:
            hostname=url[1]
        else:
            hostname=url[2]
            
        port="80"
        if hostname.find(':') >0:
            addr,port=hostname.split(':')
        else:
            addr=hostname
        port=int(port)
        ip=socket.gethostbyname(addr)
        print ip,port
        self.destnation.connect((ip,port))
        data="%s %s %s\r\n" %(self.headers['method'],self.headers['path'],self.headers['protocol'])
        self.destnation.send(data+self.request)
        print "threadName=%s proxyRemoteReceive:\r\n %s \r\n" %(self.threadName,data+self.request)


    def renderto(self):
        readsocket=[self.destnation]
        while True:
            data=''
            (rlist,wlist,elist)=select.select(readsocket,[],[],3)
            if rlist:
                data=rlist[0].recv(BUFLEN)
                print "threadName=%s proxyLocalSend:\r\n %s \r\n" %(self.threadName,data)
                if len(data)>0:
                    self.source.send(data)
                else:
                    break
    def run(self):
        self.get_headers()
        self.conn_destnation()
        self.renderto()



class Server(object):

    def __init__(self,host,port,handler=Proxy):
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host,port))
        self.server.listen(5)
        self.handler=handler

    def start(self):
        while True:
            try:
                conn,addr=self.server.accept()
#                 thread.start_new_thread(self.handler,(conn,addr))
                client_handle = threading.Thread(target=self.handler,args=(conn,addr))
                client_handle.start()
            except:
                pass


if __name__=='__main__':
    s=Server('127.0.0.1',9000)
    s.start()
