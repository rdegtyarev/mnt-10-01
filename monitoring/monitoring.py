#!/usr/bin/env python3

import json
import datetime
import time
import os

lines = []

with open('/proc/meminfo') as file:
    lines = [line.rstrip() for line in file]

mem_total = lines[0].replace('kB', '').replace(' ', '').split(':')
mem_available = lines[2].replace('kB', '').replace(' ', '').split(':')
swap_total = lines[14].replace('kB', '').replace(' ', '').split(':')
swap_free = lines[15].replace('kB', '').replace(' ', '').split(':')

date_time = datetime.datetime.now()
unixtime = time.mktime(date_time.timetuple())

metrics = {unixtime: {
    mem_total[0]: int(mem_total[1]),
    mem_available[0]: int(mem_available[1]),
    swap_total[0]: int(swap_total[1]),
    swap_free[0]: int(swap_free[1])
}
}
file_name = "/var/log/" + \
    str(date_time).split(' ')[0] + "-awesome-monitoring.log"

try:
    with open(file_name) as f:
        data = json.load(f)
    data.update(metrics)
    with open(file_name, 'w') as f:
        json.dump(data, f)
except:
    with open(file_name, 'w') as f:
        json.dump(metrics, f)
