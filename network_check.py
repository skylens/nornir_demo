# encoding=utf-8

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_netmiko import netmiko_send_command
import os, zipfile
from datetime import datetime

nr = InitNornir(config_file="config.yaml")

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def show_cmds(task, cmds):
    # cmds = task.host.data['cmds']

    max_loops = 180 / 0.2
    outputs = ''
    for cmd in cmds:
        show_result = task.run(netmiko_send_command,
                               command_string=cmd,
                               max_loops=max_loops)
        outputs = outputs + '\n' + cmd + '\n\n' + show_result.result + '\n'
    # 获取巡检当天时间
    the_day = datetime.date(datetime.utcnow())
    # 用设备名命名结果
    log_name = task.host.name + '-(' + task.host.hostname + ')' + '.txt'
    # 设置存放巡检结果位置
    folder = '巡检目录' + str(the_day)
    file_name = os.path.join(folder,log_name)
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 调用 write_file 写入文件
    task.run(write_file,
             filename=file_name,
             content=str(outputs))
    # 打包结果
    zip_name = folder + '.zip'
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder, zipf)
    zipf.close()

huaweicmds = ["display clock","display version","display alarm active","display trapbuffer","display device","display cpu-usage","display memory","display current-configuration"]
h3ccmds = ["display clock","display version","display device","display cpu-usage","display memory","display current-configuration"]
if nr.filter(platform='huawei'):
    cmds = huaweicmds
elif nr.filter(platform='hp_comware'):
    cmds = h3ccmds
else:
    print("1")

results = nr.run(task=show_cmds)
# print_result(results)

# print(nr.inventory.groups)
#
# print(nr.inventory.hosts)
# hosts = nr.inventory.hosts
# # if nr.filter(platform='huawei'):
# # hosts是一个特殊的对象，类似字典的方法，key值是host的字符串，value是一个内置的类host
# for hostname, host_obj in hosts.items():
#     print('hostname, type(hostname):', hostname, type(hostname))
#     print('host_obj, type(host_obj):', host_obj, type(host_obj))
#     print('host_obj.hostname:', host_obj.hostname)
#     print('host_obj.username:', host_obj.username)
#     print('host_obj.data：', host_obj.data)

# list groups
# print(nr.inventory.groups)

# groups类似hosts 是一个特殊的对象
# groups = nr.inventory.groups
# for group_name, group_obj in groups.items():
#     print(group_name, type(group_name))
#     print(group_obj, type(group_obj))
#     print('group_obj.username:', group_obj.hostname)
#     print('group_obj.password:', group_obj.username)
#     print('group_obj.platform：', group_obj.platform)

huawei_devs = nr.filter(platform='huawei') # 筛选platf是huawei的设备
print(huawei_devs.inventory.hosts)