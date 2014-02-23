#-*- coding:UTF-8 -*-
#! /usr/bin/python

import getpass,sys
from spider import renrenspider

version = "0.3"

if __name__ == "__main__":
	email=raw_input('请输入用户名：')
	password=getpass.getpass('请输入密码：')
	renrenspider=renrenspider(email,password)
	renrenspider.login()
	mode=999

	while(mode!='000'):
		mode=raw_input('请输入操作代码：')
		if(mode=='120'):
			content=raw_input('请输入状态内容：')
			renrenspider.publish(content)
		if(mode=='200'):
			content=raw_input('请输入要访问的ID：')
			renrenspider.visit(content)
		if(mode=='100'):
			renrenspider.feed(renrenspider.file)
			renrenspider.show()
	sys.exit()

