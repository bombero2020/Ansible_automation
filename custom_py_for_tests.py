import re
import json, requests

file = open('../output', 'r')
lines = file.readlines()

myip = ['10.67.38.40', '10.67.38.41']
task = 'TASK'
recapi = 'PLAY RECAP'
recap = {}
summary = {'ok': 0, 'changed': 0, 'unreachable': 0, 'failed': 0, 'skipped': 0, 'rescued': 0, 'ignored': 0}
hosts = [{'PASS': 'Maqueta1', 'HOST_IP': '10.67.38.40', 'USER': 'admin'},
         {'PASS': 'Maqueta1', 'HOST_IP': '10.67.38.41', 'USER': 'admin'}]
states=['ok', 'changed', 'unreachable', 'failed', 'skipped', 'rescued', 'ignored']

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)
print(todos)
json_string = json.dumps(lines)
print(json_string)

for sum in summary.keys():
    print(sum)


for host in hosts:
    ip = host['HOST_IP']
    recap[ip] = list(filter(lambda line: ip in line, lines))[-1]
    res = recap[ip].split(':')
    ok = res[1].replace('    ', ',')
    ok = ok.strip('\n').strip(' ').split(',')
    lu = [i for i in ok]
    print(lu)
    dic_ok = {ip: ok}
    print(dic_ok)
    # summary['ok'] = str(re.findall('ok=\d', recap[ip])).strip('ok=')
    # print('sumario', summary)

# print(recap.values())
