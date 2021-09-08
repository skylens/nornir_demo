#!/usr/bin/python3
#-*- coding:utf-8 -*-
# ScriptName: network_ssh.py
# Create Date: 2020-07-26 12:39
# Modify Date: 2019-07-26 12:39
#***************************************************************#

from netmiko import ConnectHandler
def huawei(ip,username,password,secret):
    huawei = {
            'device_type': 'huawei',
            'ip': ip,
            'username': username,
            'password': password,
            'secret':secret,
    }
    command = ['dis cu']
    connect = ConnectHandler(**huawei)
    connect.enable()
    full_config = ''
    for cmd in command:
        config = connect.send_command(cmd)
        full_config = full_config + config
    return full_config
    connect.disconnect()

if __name__ == '__main__':
    host = ['1.1.1.1']
    for ip in host:
        huawei(ip,'你的账号','你的密码','enable密码')