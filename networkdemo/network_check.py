#!/usr/bin/env python3

from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException

import logging

# log记录
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

def screen_handle(net_connect,output):
    null_more = []
    if "---- More ----" in output:
        # 遇到more，就多输入几次个空格，normalize=False表示不取消命令前后空格*。
        output += net_connect.send_command_timing('            \n', strip_prompt=False, strip_command=False, normalize=False)
    more = output.split("\n")
    for i in more:
        null_more.append(i.replace('  ---- More ----               ', '').replace('  ---- More ----', ''))
    return null_more

if __name__ == "__main__":
    # 设备信息
    huawei = {
        'device_type': 'huawei_vrpv8',
        'host':   '10.20.1.1',
        'username': 'admin',
        'password': 'passw0rd',
        'session_log': 'output.txt'
    }
    # commonds = ['display ip interface brief']
    # for n_device in devices:
    #     for n_commond in commonds:
    #         get_crc(n_device, n_commond)
            # 每个设备操作完之后，关闭连接
        # ConnectHandler(**n_device).disconnect()
    try:
        net_connect = ConnectHandler(**huawei)
        print(net_connect.find_prompt())
        # 设置分屏，如果设备支持 screen-length 0 temporary
        # net_connect.send_command("screen-length 0 temporary")
        # 使用 send_command 会报错，使用 send_command_timing 对不能关闭分屏出现的 more 进行处理
        output = net_connect.send_command_timing("display version | no-more")
        # output = net_connect.send_command_timing(commonds)
        # print(screen_handle(net_connect,output))
        print(output)
        # for s in screen_handle(net_connect,output):
        #     print(s)
    except (EOFError,NetMikoTimeoutException):
        print('Can not connect to Device')
    except (EOFError, NetMikoAuthenticationException):
        print('username/password wrong!')
    except (ValueError, NetMikoAuthenticationException):
        print('enable password wrong!')
    ConnectHandler(**huawei).disconnect()

    
