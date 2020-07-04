import requests
import os
import json
import time

def toot(message, instance):
    t = dict()
    t['status'] = message
    t['visibility'] = 'unlisted'
    t['spoiler_text'] = '타임라인 지분 측정기'
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

def fetch_and_toot(instance):
    uri = instance + '/api/v1/timelines/home'
    d = dict()
    for i in range(3):
        timeline = requests.get(uri, headers = headers, params = params).json()
        for m in range(len(timeline)):
            status = timeline[m]
            if status['reblog'] is None:
                if status['account']['username'] in d:
                    update(d, status)
                else:
                    initial(d, status)
            else:
                pass
        pointid = timeline[-1]['id']
        params['max_id'] = pointid

    sort = sorted(d.items(), key = lambda k : k[1], reverse = True)

    msg = []
    entireNum = sum(list(d.values()))
    num = 0
    for j in range(len(d)):
        name = sort[j][0]
        percent = percentage(d, name, entireNum)
        sentence = '@ ' + name + ' 님 ' + str(percent) + '%'
        msg.append(sentence)

    message = ''
    for k in range(len(msg)):
        append = msg[k] + '\n'
        message += append

    baseTime = time.strftime('%H:%M', time.localtime(time.time()))
    message += '\n' + str(baseTime) + '(KST) 기준 최근 120툿을 대상으로 측정합니다.'
    toot(message, instance)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(base + 'acc.txt') as f:
        acc = f.read().strip()

    headers = {'Authorization': 'Bearer ' + acc}
    params = {'limit': 40}

    instance = 'https://twingyeo.kr'

    fetch_and_toot(instance)