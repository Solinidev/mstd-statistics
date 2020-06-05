import requests
import os
import json

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base + 'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization' : 'Bearer ' + acc}
params = {'limit' : 3} # 40까지만 먹네?
instance = 'https://twingyeo.kr'

def initial(dic, statdict):
    member = statdict['account']['username']
    dic[member] = 1

def update(dic, statdict):
    member = statdict['account']['username']
    count = int(dic.get(member))
    dic.update({member : count + 1})

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
print(d)