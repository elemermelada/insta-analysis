import os
import json

path = 'export/'
data = {}
myfollowing = []
template = {}

user_data = open('ME.json','r')
user_json = json.loads(user_data.read())
user_data.close()
for friend in user_json:
    myfollowing.append(friend['username'])
    template[friend['username']] = 0

for root, dirs, files in os.walk(path):
    for file in files:
        data[file[0:len(file)-5]] = template.copy()
        user_data = open(path + file,'r')
        user_json = json.loads(user_data.read())
        user_data.close()
        for friend in user_json:
            if friend['username'] in myfollowing:
                data[file[0:len(file)-5]][friend['username']] = 1


export = open('final.json','w')
export.write(json.dumps(data))
export.close()