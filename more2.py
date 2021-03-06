#!/usr/bin/python2.7
#-*- encoding: utf-8 -*-
import sys
import binascii
import locale
import poplib
import email
import string
import rsa
import binascii

from email import parser
from  pyDes import *

# make sure encoding
__g_codeset = sys.getdefaultencoding()
if "ascii"==__g_codeset:
    __g_codeset = locale.getdefaultlocale()[1]
#

def object2double(obj):
    if(obj==None or obj==""):
        return 0
    else:
        return float(obj)
    #end if    
#

def utf8_to_mbs(s):
    return s.decode("utf-8").encode(__g_codeset)
#

def mbs_to_utf8(s):
    return s.decode(__g_codeset).encode("utf-8")
#

host = 'pop.XX.com'
username = 'XXX@XX.com'
password = 'XXXXXXX'

pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)

#Get messages from server:
#
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
#print messages

#print "--------------------------------------------------"
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#print messages

#Parse message intom an email object:
# 分析
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
i = 0
for index in range(0,len(messages)):
    message = messages[index];
    i = i + 1;
    subject = message.get('subject')   
    h = email.Header.Header(subject)
    dh = email.Header.decode_header(h)
    subject = dh[0][0], dh[0][1]
    mailName = "mail%d.%s" % (i, subject)
    f = open('%d.log'%(i), 'w');
    print >> f, "[+] Date: ", message["Date"]
    print >> f, "[+] From: ", email.utils.parseaddr(message.get('from'))[1]
    print >> f, "[+] To: ", email.utils.parseaddr(message.get('to'))[1]
    print >> f, "[+] Subject: ", subject
    
    
    j = 0
    for part in message.walk():
        j = j + 1
        fileName = part.get_filename()
        contentType = part.get_content_type()
        mycode=part.get_content_charset();
        # save attachment
        if fileName:
            data = part.get_payload(decode=True)
            h = email.Header.Header(fileName)
            dh = email.Header.decode_header(h)
            fname = dh[0][0]
            encodeStr = dh[0][1]
            if encodeStr != None:
                fname = fname.decode(encodeStr, mycode)
            #end if
            fEx = open("%s"%(fname), 'wb')
            fEx.write(data)
            fEx.close()
        elif contentType == 'text/plain':# or contentType == 'text/html':
            #save content
            data = part.get_payload(decode=True)
            content=str(data);
            if mycode=='gb2312':
                content= mbs_to_utf8(content)
            #end if    
            #nPos = content.find('test')
            #print("nPos is %d"%(nPos))
            print >> f, "[+]content: ",data
            
            print  "[+] Date: ", message["Date"]
            print  "[+] From: ", email.utils.parseaddr(message.get('from'))[1]
            print  "[+] To: ", email.utils.parseaddr(message.get('to'))[1]
            print  "[+] Subject: ", subject            
                       
            with open('private_key.pem') as private_file:
                priv_key = rsa.PrivateKey.load_pkcs1(private_file.read())  
            
            decrypto = rsa.decrypt(binascii.unhexlify(data),priv_key)
            
            print >> f, "[+]RSA_Crypto:  ", binascii.unhexlify(data) + '\n\n\n'
              
            print >> f, "[+]Deccryption_Content: ", decrypto
            
            print  '[+]de_content:  ' + decrypto
            
        #end if
    #end for 
    f.close()
#end for    
pop_conn.quit()
