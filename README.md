# Домашнее задание к занятию "10.01. Зачем и что нужно мониторить"

## Обязательные задания

1. Вас пригласили настроить мониторинг на проект. На онбординге вам рассказали, что проект представляет из себя 
платформу для вычислений с выдачей текстовых отчетов, которые сохраняются на диск. Взаимодействие с платформой 
осуществляется по протоколу http. Также вам отметили, что вычисления загружают ЦПУ. Какой минимальный набор метрик вы
выведите в мониторинг и почему?  

#### Решение
- White-box мониторинг (по возможности) - мониторинг платформы.
- Black-box мониторинг
  - CPU - вычисления загружают процессор, мониторим нагрузку.
  - RAM - в зависимости от архитектуры платформы, вероятнее всего перед записью файла на диск он формируется в RAM. Мониторим уровень загрузки RAM.
  - OPS - мониторинг скорости чтения записи на диск.
  - FS - метрики файловой системы, мониторим свободное пространство на диске. 

---
  
2. Менеджер продукта посмотрев на ваши метрики сказал, что ему непонятно что такое RAM/inodes/CPUla. Также он сказал, 
что хочет понимать, насколько мы выполняем свои обязанности перед клиентами и какое качество обслуживания. Что вы 
можете ему предложить?  

#### Решение
- Утвердить с заказчиком Соглашение об уровне обслуживания (SLA)
- Определяем сигналы, которые имеют наибольшее влияние на SLA. Для http сервиса это могут быть: Время отклика, Величина трафика, Уровень ошибок.
- Формируем на основании сигнала определяем уровни SLO, выводим на дашборд.
- Выводим на дашборд текущее состояние сигналов (SLI).
- По необходимости, настраиваем алерты на падение уровня сигналов ниже SLO.
Менеджер продукта может мониторить уровни SLI, реагировать на алерты.

---

3. Вашей DevOps команде в этом году не выделили финансирование на построение системы сбора логов. Разработчики в свою 
очередь хотят видеть все ошибки, которые выдают их приложения. Какое решение вы можете предпринять в этой ситуации, 
чтобы разработчики получали ошибки приложения?

#### Решение
Использовать open source решения. Для указанных выше задач можно использовать Prometheus в связке с Grafana. При необходимости аккумулировать логи можно использовать ELK или OpenSearch.
  
---  

3. Вы, как опытный SRE, сделали мониторинг, куда вывели отображения выполнения SLA=99% по http кодам ответов. 
Вычисляете этот параметр по следующей формуле: summ_2xx_requests/summ_all_requests. Данный параметр не поднимается выше 
70%, но при этом в вашей системе нет кодов ответа 5xx и 4xx. Где у вас ошибка?

#### Решение
В расчете упустили коды ответов 3xx (которых судя по результату будет 30%)
Корректная формула SLI = (summ_2xx_requests + summ_3xx_requests)/(summ_all_requests)

---

## Дополнительное задание (со звездочкой*) - необязательно к выполнению


а) работающий код python3-скрипта


```python
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

```

б) конфигурацию cron-расписания
```
* * * * * /usr/bin/python3 /mnt-10-01/monitoring/monitoring.py
```

в) пример верно сформированного 'YY-MM-DD-awesome-monitoring.log', имеющий не менее 5 записей
```json
{
    "1643446681.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2804932,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    },
    "1643446741.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2809412,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    },
    "1643446801.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2799580,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    },
    "1643446861.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2767376,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    },
    "1643446921.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2809180,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    },
    "1643446981.0": {
        "MemTotal": 7481476,
        "MemAvailable": 2799144,
        "SwapTotal": 2097148,
        "SwapFree": 1863712
    }
}

```
