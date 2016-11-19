#!usr/bin/python2.7
#coding:utf-8

import binascii

import smtplib
from pyDes import *

from email.mime.text import MIMEText


def sendMail(user,pwd,to,subject,text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject

    try:
        smtpServer = smtplib.SMTP('smtp.xxxx.com',25) #port is changed with your smtp server
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
        print "[+] Mail Sent Successfully\n "
    except Exception,e:
        
        print str(e)
        print "[-] Sending Mail Failed "

user = 'youmail@xxx.com'
pwd = 'you smtp passwd'
 

#----------------------------------------------------------------------
#using DES_CBC to encrypt Content
def encrypt( filename):
    """
    Get Content
    """
    with open(filename) as content:
        data = content.readline()
    
    key = 'test_key'  #8 or multiple of 8 bits
    IV = 'test__IV'   #8 bits
    
    k = des(key,CBC, IV, pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(data)
    
    return binascii.hexlify(d)
    

target = open('target.txt')
line = target.readline()
list = line.split(',')
for recvmail in list:
    sendMail(user,pwd, recvmail, '20133254_test', encrypt('content.txt'))
 

target.close() 
 
'''   
#email boom!!
target = open('target.txt')
line = target.readline()
while line:
    list = line.split(',')
    for recvmail in list:
        sendMail(user,pwd, recvmail, 'subject', 'content')

target.close()
'''
'''
with open('target.txt') as target:
    recv = target.readline().replace(',',' ')
    sendMail(user, pwd, recv, 'subject', content')
    print recv
'''
