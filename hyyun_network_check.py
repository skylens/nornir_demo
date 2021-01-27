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

def show_cmds(task):
    cmds = task.host.data['cmds']
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

results = nr.run(task=show_cmds)
print_result(results)