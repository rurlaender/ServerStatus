import psutil
from psutil._common import bytes2human
import json
import subprocess

def get_system_json():

    #Get memory usage
    mem = psutil.virtual_memory()
    mem_json = {}
    for var in vars(psutil._pslinux.svmem):
        if not var.startswith("_"):
            if var == "percent":
                mem_json[var] = getattr(mem, var)
            else:
                mem_json[var] = bytes2human(getattr(mem, var))

    #Get cpu usage
    cpu = psutil.cpu_percent(interval=0.5, percpu=True)
    cpu_json = {}
    cores = []
    for core in cpu:
        cores.append(core)
    cpu_json["cores"] = cores
    cpu_json["frequency"] = psutil.cpu_freq(percpu=False).current

    #Get network
    net_ifs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters(pernic=True)
    net_stat = psutil.net_if_stats()
    net_json = []
    for net_if in net_ifs:
        adapter = {}
        adapter["name"] = net_if
        adapter["up"] = getattr(net_stat[net_if],"isup")
        io = net_io[net_if]
        for var in vars(psutil._common.snetio):
            if not var.startswith("_"):
                if "bytes" in var:
                    adapter[var] = bytes2human(getattr(io, var))
                else:
                    adapter[var] = getattr(io, var)
        net_json.append(adapter)

    #get sensor data
    #RPI only
    sens_temp = psutil.sensors_temperatures()
    temp_json = {}
    temp_json["cpu"] = sens_temp["cpu_thermal"][0][1]


    #Disk usage
    #Get used disk space
    #df -h |grep mmcblk0p1| awk '{print $2 " " $3 " " $4 " " $5}'| sed 's/%//g
    #improve to finde all disks from a given list
    disktypes = ["mmcblk", "sd"]
    linux_cmd = "df -h | awk '{print $1\";\"$2\";\"$3\";\"$4}'"
    lines = (subprocess.getoutput(linux_cmd)).split('\n')
    disk_json = []
    for line in lines:
        disk = line.split(";")[0]
        for x in disktypes:
            if x in disk:
                json_data = {}
                vals = line.split(";")
                json_data["name"] =disk
                json_data["total"] = vals[1] 
                json_data["used"]  = vals[2] 
                json_data["free"]  = vals[3] 
                disk_json.append(json_data)
    #users
    users_json = []
    users = psutil.users()
    for user in users:
        user_json = {}
        for var in vars(psutil._common.suser):
            if not var.startswith("_"):
                user_json[var] = (getattr(user, var))
        users_json.append(user_json)

    

    system_status = {}
    system_status["cpus"] = cpu_json
    system_status["temperature"] = temp_json
    system_status["memory"] = mem_json
    system_status["network"] = net_json
    system_status["disks"] = disk_json
    system_status["users"] = users_json
    return system_status

