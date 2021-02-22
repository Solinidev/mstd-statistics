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

def selectNum(n):
    for lim in range(40, 0, -10):
        remain = n % lim
        if remain == 0:
            repeat = n / lim
            return lim, int(repeat)

def fetch_and_toot(instance, repeat, collect):
    uri = instance + '/api/v1/timelines/home'
    d = dict()
    for _ in range(repeat):
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
    for j in range(len(d)):
        name = sort[j][0]
        percent = percentage(d, name, entireNum)
        sentence = '@ ' + name + ' 님 ' + str(percent) + '%'
        msg.append(sentence)
        if j == 9:
            break

    message = ''
    for k in range(len(msg)):
        append = msg[k] + '\n'
        message += append

    baseTime = time.strftime('%H:%M', time.localtime(time.time()))
    message += '\n' + str(baseTime) + '(KST) 기준 최근 ' + str(collect) + '툿을 대상으로 측정한 상위 10명입니다.'
    toot(message, instance)

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, 'acc.txt')) as f:
        acc = f.read().strip()
    
    collect = 100
    lim, repeat = selectNum(collect)

    headers = {'Authorization': 'Bearer ' + acc}
    params = {'limit': lim}

    instance = 'https://twingyeo.kr'

    fetch_and_toot(instance, repeat, collect)