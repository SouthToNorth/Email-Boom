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

user = 'shizimeiyoula@163.com'
password = 'daozhu250'
subject = 'Just a test'

data = 'python of sending mail'
to = 'web_vb200@sina.com'

#----------------------------------------------------------------------
def rsa_encrypt(data):
    #(pub_key,pri_key) = rsa.newkeys(32)
    #crypto = rsa.encrypt(data,pub_key)
    #return crypto

    """
    利用RSA对文件正文进行加密
    >>> (pub_key,priv_key) = rsa.newkeys(256)
    >>> crypto = rsa.encrypt(b'www',pub_key)
    >>> rsa.decrypt(crypto, priv_key)
    >>> 'www'
    """
     
    #生成一对密钥，保存为.pem文件,可以为下次使用准备，也可以直接实用生成的密钥，如开头注释所写
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
    定义邮件内容，包括正文与附件
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
        #设置附件MIME和文件名，注意附件的类型
        att = MIMEBase('txt','txt',filename = 'test.txt')
        #设置必要的头信息
        att.add_header('Content-Disposition','attachment',filename = 'test.txt')
        att.add_header('Content-ID','<0>')
        att.add_header('X-Attachment-ID','<0>')
        
        #将附件的内容加到邮件内容中去
        att.set_payload(f.read())
        #使用Base64编码
        encoders.encode_base64(att)
        #添加到MIMEMultipart
        msg.attach(att)  
'''


#----------------------------------------------------------------------
def sendmail(user,password,to,subject,msg):
    """
    发送函数，参数分别为：user,登陆名，password：登录密码，to:收件人,subject：邮件主题，
    msg：邮件内容，包括邮件的附件和正文
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