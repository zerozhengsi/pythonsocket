#coding=utf-8
'''
Created on 2016年7月11日

@author: zeroz
'''
import re,urllib2
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
import time

class Getmyip:
    
    def getip(self):
        try:
            myip = self.visit("http://www.ip.cn/")
        except Exception as err:
            myip = "So sorry!!!"+str(err)
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
    def sendmail(self,ip):
        sender = '18086605582@189.cn'  
        receiver = 'zerozhengsi@hotmail.com'  
        subject = 'my wlan ip'  
        smtpserver = 'smtp.189.cn'  
        username = '18086605582@189.cn'  
        password = '0193jsgawg'  
        
        msg = MIMEText('my wlan ip is :'+ip,'text')
        msg['Subject'] = Header(subject)   
        smtp = smtplib.SMTP()  
        smtp.connect(smtpserver)  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msg.as_string())  
        smtp.quit() 

oldip = ""
while True:
    getmyip = Getmyip()
    localip = getmyip.getip()
    print localip
    print "oldip:"+oldip
    if oldip != localip:
        getmyip.sendmail(localip)
        print "send mail success"
        oldip = localip
    time.sleep(3)
        
        