#!/usr/bin/python2.7
#coding:utf-8

import binascii
import smtplib
import rsa
import binascii

from  email import encoders
from  email.mime.text import MIMEText
from  email.mime.base import MIMEBase
from  email.mime.multipart import MIMEMultipart

user = 'XXX@XX.com'
password = 'XXX'
subject = 'Just a test'

data = 'python of sending mail'
to = 'XXX@XX.com'

#----------------------------------------------------------------------
def rsa_encrypt(data):
    #(pub_key,pri_key) = rsa.newkeys(32)
    #crypto = rsa.encrypt(data,pub_key)
    #return crypto

    """
    use RSA encrypted content
    >>> (pub_key,priv_key) = rsa.newkeys(256)
    >>> crypto = rsa.encrypt(b'www',pub_key)
    >>> rsa.decrypt(crypto, priv_key)
    >>> 'www'
    """
     
    #make a couple key,kepp as .pem, repare for next,also could use sraight produce keys
    #(pub_key, priv_key) = rsa.newkeys(256)
    (pub_key,priv_key) = rsa.newkeys(1024)
    
    
    pubfile = open('public_key.pem','w+')
    pubfile.write(pub_key.save_pkcs1())
    pubfile.close()
    
    prifile = open('private_key.pem','w+')
    prifile.write(priv_key.save_pkcs1())
    prifile.close()
    
    with open('public_key.pem') as public_file:
        pub_key = rsa.PublicKey.load_pkcs1(public_file.read())
    '''   
    with open('private_key.pem') as private_file:
        priv_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    '''  
    crypto = rsa.encrypt(data,pub_key)
    
        
    decrypto = rsa.decrypt(crypto,priv_key)
    print crypto
    print decrypto
    
    return binascii.hexlify(crypto)
    

#----------------------------------------------------------------------
def msg_cont(filename):
    """
    content attachment
    msg.attach(payload)
    """
    msg = MIMEMultipart()
    msg ['From'] = user
    msg ['To'] = to
    msg ['subject'] = subject
    
    msg.attach(MIMEText(rsa_encrypt(data), _subtype='plain', _charset='us-ascii'))
    
    att = MIMEText(open('test.txt','rb').read(),'base64','utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment;filename = "test1.txt"'
    msg.attach(att)  
    
    return msg
'''  
    with open('test.txt','rb') as f:
        #attachment of MIME name of attachment,and notice type of file
        att = MIMEBase('txt','txt',filename = 'test.txt')
        #head information
        att.add_header('Content-Disposition','attachment',filename = 'test.txt')
        att.add_header('Content-ID','<0>')
        att.add_header('X-Attachment-ID','<0>')
        
        #make attachment into email
        att.set_payload(f.read())
        #base 64
        encoders.encode_base64(att)
        #add into MIMEMultipart
        msg.attach(att)  
'''


#----------------------------------------------------------------------
def sendmail(user,password,to,subject,msg):
    """
    user，password，to:,subject，
    msg：attachment coontent
    """

    try:
        SmtpServer = smtplib.SMTP(host='smtp.163.com', port=25)
        SmtpServer.ehlo()
        SmtpServer.starttls()
        SmtpServer.ehlo()
        SmtpServer.login(user, password)
        SmtpServer.sendmail(user,to,msg.as_string())
        SmtpServer.close()        
        print 'success'
    except Exception,e:
        print str(e)
        print 'send failed'        

sendmail(user, password, to, subject, msg_cont('test.txt'))    
