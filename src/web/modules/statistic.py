import requests
import os
import json

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

def calculate(instance, token):
    uri = instance + '/api/v1/timelines/home'
    headers = {'Authorization' : 'Bearer ' + token}
    params = {'limit' : 25}
    d = dict()
    for _ in range(4):
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
        append = msg[k] + '<br>'
        message += append

    return message