# encoding=utf-8

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_netmiko import netmiko_send_command


nr = InitNornir(config_file="config.yaml", dry_run=True)

# # 列出所有组
# print(nr.inventory.groups)
# # 列出所有host
# print(nr.inventory.hosts)

# 筛选某个 platform 的所有hosts
cisco_iosv_devices = nr.filter(platform='cisco_ios')
# print(cisco_iosv_devices.inventory.hosts, type(cisco_iosv_devices.inventory.hosts))

def show_cmds(task):
    max_loops = 180 / 0.2
    cmd = "show run"
    show_result = task.run(netmiko_send_command,command_string=cmd,max_loops=max_loops)
    return show_result

results = cisco_iosv_devices.run(task=show_cmds)
print_result(results)

allresults = nr.run(task=show_cmds)
print_result(allresults)