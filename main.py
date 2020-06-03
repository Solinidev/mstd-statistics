import requests
import os
import json

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base + 'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization' : 'Bearer ' + acc}
params = {'limit' : 2}
instance = 'https://twingyeo.kr'

uri = instance + '/api/v1/timelines/home'
timeline = requests.get(uri, headers = headers, params = params)
for t in timeline.iter_lines(): # 왜 되지????
    dec = t.decode('utf-8')
    break

dec = dec.strip('[]')
newdec = json.loads(dec) # limit 2 이상이면 작동안함, 왜 안 돼
print(newdec)

# dec = dict(dec)
# print(dec)
# print(type(dec))