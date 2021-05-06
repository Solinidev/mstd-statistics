import requests
import json

def initial(dic, statdict):
    member = statdict['user']['username']
    dic[member] = 1

def update(dic, statdict):
    member = statdict['user']['username']
    count = int(dic.get(member))
    dic.update({member : count + 1})

def percentage(dict, name, entireNum):
    cnt = dict.get(name)
    percent = round(cnt / entireNum * 100, 1)
    return percent

def validate(note, d):
    if note['renoteId'] is None:
        if note['user']['username'] in d:
            update(d, note)
        else:
            initial(d, note)
    else:
        pass

def get_timeline_misskey(instance, token):
    uri = instance + '/api/notes/timeline'

    header = {
        'content-type' : 'application/json'
    }

    payload = {
        'limit' : 100,
        'i' : token
    }

    notes = requests.post(uri, headers = header, data = json.dumps(payload))
    return notes.json()

def calc_misskey(instance, token):
    d = dict()

    timeline = get_timeline_misskey(instance, token)
    for i in range(len(timeline)):
        note = timeline[i]
        try:
            if note['localOnly'] is True:
                pass
            validate(note, d)
        except:
            validate(note, d)


    sort = sorted(d.items(), key = lambda k : k[1], reverse = True)

    msg = []
    entireNum = sum(list(d.values()))
    for i in range(len(d)):
        name = sort[i][0]
        percent = percentage(d, name, entireNum)
        sentence = '@ ' + name + ' 님 ' + str(percent) + '%'
        msg.append(sentence)
        if i == 9:
            break

    message = ''
    for j in range(len(msg)):
        append = msg[j] + '<br>'
        message += append

    return message

# # print(message)
# create_note(instance, token, message)