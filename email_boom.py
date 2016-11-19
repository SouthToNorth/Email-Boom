#usr/bin/python2.7
#coding:utf-8

import binascii
import smtplib
import time
from pyDes import *

from email.mime.text import MIMEText

def sendMail(user,pwd,to,subject,text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject

    try:
        smtpServer = smtplib.SMTP('smtp.163.com',25)
        print "[+] Connecting To Mail Server "
        smtpServer.ehlo()
        print "[+] Starting Encrypted Session "
        smtpServer.starttls()
        smtpServer.ehlo()
        print "[+] Logging Into Mail Server"
        smtpServer.login(user,pwd)
        print "[+] Sending Mail "
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print "[+] Mail Sent Successfully "
    except Exception,e:
        
        print str(e)
        print "[-] Sending Mail Failed "

user = 'shizimeiyoula@163.com'
pwd = 'daozhu250'
 

#----------------------------------------------------------------------
def encrypt( filename):
    """
    取出正文内容
    """
    with open(filename) as content:
        data = content.readline()
    
    key = 'test_key'
    IV = 'test__IV'
    
    k = des(key,CBC, IV, pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(data)
    
    return binascii.hexlify(data)
    
"""
target = open('target.txt')
line = target.readline()
list = line.split(',')
for recvmail in list:
    sendMail(user,pwd, recvmail, '20133224', encrypt('content.txt'))

target.close() 
 """
  
#email boom!!
target = open('target.txt')
line = target.readline()
while line:
    list = line.split(',')
    for recvmail in list:
        sendMail(user,pwd, recvmail, '20133224', encrypt('content.txt'))
        time.sleep(5)

target.close()

'''
with open('target.txt') as target:
    recv = target.readline().replace(',',' ')
    sendMail(user, pwd, recv, '20133224', 'wedfrfrfjgksksdsdsas')
    print recv
'''