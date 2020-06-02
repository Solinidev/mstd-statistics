import requests
import os
import json

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base + 'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization':'Bearer ' + acc}
instance = 'https://twingyeo.kr'

uri = instance + '/api/v1/timelines/home'
timeline = requests.get(uri, headers = headers)

print(timeline.text)

# status = json.dumps(timeline.text)
# print(status)

# for t in timeline:
#     status = json.dumps(t.text)