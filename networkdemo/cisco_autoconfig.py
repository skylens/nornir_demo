#!/usr/bin/python3
#-*- coding:utf-8 -*-
# ScriptName:  Cisco_Autoconfig.py
# Create Date: 2020-07-08 16:35
# Modify Date: 2020-07-08 16:35
#***************************************************************#
from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException #引入netmiko连接模块、报错模块
import getpass #引入密码模块
import time #引入时间模块
date = time.strftime('%Y%m%d', time.localtime()) #赋予date变量
password = getpass.getpass('Password:') #赋予password变量

host={
'192.168.1.10',
'192.168.1.11',
}; #定义需要下发配置的主机 IP

for ip in host: #定义循环
    #创建字典
    cisco_ios = {
    'device_type':"cisco_ios", #定义设备类型
    'ip':ip, #调用变量ip
    'port':'22', #指定端口，默认为22
    'username':'admin', #设备登录名
    'password':password, #调用getpass模块
    #'secret' : 'admin' #enable密码
    }
    try:
	cisco_connect = ConnectHandler(**cisco_ios) #传入设备字典与设备建立SSH连接。
	print ("Sucessfully Login to",ip)
	print ("Building configuration...")
	config = ['ntp server 192.168.1.1','ntp server 192.168.1.2','do show run | sec ntp'] #定义需要配置的命令
	input = cisco_connect.send_config_set(config) #执行命令
	print(input) #打印输出结果
	print(ip,'Was finished!\n',"-"*100)
    except NetmikoAuthenticationException : #认证失败报错记录
	e1 = open(f'{date}.txt','a')
	print(date,ip,'[Error 1] Authentication failed.\n',file = e1)
	e1.close
    except NetmikoTimeoutException : #登录超时报错记录
	e2 = open(f'{date}.txt','a')
	print(date,ip,'[Error 2] Connection timed out.\n',file = e2)
	e2.close
    except : #未知报错记录
	e3 = open(f'{date}.txt','a')
	print(date,ip,'[Error 3] Unknown error.\n',file = e3)
	e3.close
cisco_connect.disconnect() #断开SSH连接