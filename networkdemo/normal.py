from netmiko import ConnectHandler
import logging

# log记录
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

huawei = {
    'device_type': 'huawei_vrpv8',
    'host': '10.200.18.31',
    'username': 'zhangpan15933016816',
    'password': 'HYYzp0123!',
    'session_log': 'output.txt'
}
def screen_handle(net_connect,output):
    null_more = []
    if "---- More ----" in output:
        # 遇到more，就多输入几次个空格，normalize=False表示不取消命令前后空格*。
        output += net_connect.send_command_timing('            \n', strip_prompt=False, strip_command=False, normalize=False)
    more = output.split("\n")
    for i in more:
        null_more.append(i.replace('  ---- More ----               ', '').replace('  ---- More ----', ''))
    return null_more

command = ['dis ver']
connect = ConnectHandler(**huawei)
full_config = ''
for cmd in command:
    config = screen_handle(connect, connect.send_command_timing(cmd))
    full_config = full_config + config
print(full_config)
connect.disconnect()
