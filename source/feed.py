#-*- coding:UTF-8 -*-
#! /usr/bin/env python

from sgmllib import SGMLParser
import sys,urllib,urllib2,cookielib
import datetime
import time
import getpass

class spider(SGMLParser):
    def __init__(self,email,password):
        SGMLParser.__init__(self)
        self.h3=False
        self.h3_is_ready=False
        self.div=False
        self.h3_and_div=False
        self.a=False
        self.depth=0
        self.names=""
        self.dic={}
        self.email=email
        self.password=password
        self.domain='renren.com'
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)       

    def login(self):
        print '[%s] 开始登录' % datetime.datetime.now()
        url='http://www.renren.com/PLogin.do'
        postdata={
                  'email':self.email,
                  'password':self.password,
                  'domain':self.domain  
                  }
        try:
            req=urllib2.Request(url,urllib.urlencode(postdata))
            self.file=urllib2.urlopen(req).read()
            idPos = self.file.index("'id':'")
            self.id=self.file[idPos+6:idPos+15]
            tokPos=self.file.index("get_check:'")
            self.tok=self.file[tokPos+11:tokPos+21]
            rtkPos=self.file.index("get_check_x:'")
            self.rtk=self.file[rtkPos+13:rtkPos+21]
            print '[%s] 登录成功' % datetime.datetime.now()
        except:
            print '[%s] 登录失败' % datetime.datetime.now()
            sys.exit()

    def start_h3(self,attrs):
        self.h3 = True
    
    def end_h3(self):
        self.h3=False
        self.h3_is_ready=True
    
    def start_a(self,attrs):
        if self.h3 or self.div:
            self.a=True

    def end_a(self):
        self.a=False
             
    def start_div(self,attrs):
        if self.h3_is_ready == False:
            return
        if self.div==True:
            self.depth += 1
        
        for k,v in attrs:
            if k == 'class' and v == 'content':
                self.div=True;
                self.h3_and_div=True

    def end_div(self):
        if self.depth == 0:
            self.div=False
            self.h3_and_div=False
            self.h3_is_ready=False
            self.names=""

        if self.div == True:
            self.depth-=1

    def handle_data(self,text):
        if self.h3 and self.a:
            self.names+=text
        if self.h3 and (self.a==False):
            if not text:pass
            else: self.dic.setdefault(self.names,[]).append(text)
            return
            if self.h3_and_div:
                self.dic.setdefault(self.names,[]).append(text)
                 
    def show(self):
        type = sys.getfilesystemencoding()
        for key in self.dic:
            print ( (''.join(key)).replace(' ','')).decode('utf-8').encode(type), \
                ( (''.join(self.dic[key])).replace(' ','')).decode('utf-8').encode(type)

email=raw_input('请输入用户名：')
password=getpass.getpass('请输入密码：')
renrenspider=spider(email,password)
renrenspider.login()

renrenspider.feed(renrenspider.file)
renrenspider.show()
        
sys.exit()
