import requests
import os
import json

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base + 'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization' : 'Bearer ' + acc}
params = {'limit' : 40} # 40까지만 먹네?
instance = 'https://twingyeo.kr'

def toot(message):
    t = dict()
    t['status'] = message
    t['visibility'] = 'unlisted'
    requests.post(instance + '/api/v1/statuses', headers = headers, data = t)

def initial(dic, statdict):
    member = statdict['account']['username']
    dic[member] = 1

def update(dic, statdict):
    member = statdict['account']['username']
    count = int(dic.get(member))
    dic.update({member : count + 1})

def percentage(dict, name, entireNum):
    cnt = dict.get(name)
    percent = round(cnt / entireNum * 100, 1)
    return percent

uri = instance + '/api/v1/timelines/home'
timeline = requests.get(uri, headers = headers, params = params).json()
d = dict()
for i in range(len(timeline)):
    status = timeline[i]
    if status['reblog'] is None:
        if status['account']['username'] in d:
            update(d, status)
        else:
            initial(d, status)
    else:
        pass

msg = []
entireNum = sum(list(d.values()))
keys = list(d.keys())
for j in range(len(d)):
    name = keys[j]
    percent = percentage(d, name, entireNum)
    sentence = '@ ' + name + ' 님 ' + str(percent) + '%'
    msg.append(sentence)

message = 'solini 님의 탐라 비율입니다. \n\n'
for k in range(len(msg)):
    append = msg[k] + '\n'
    message += append

toot(message)