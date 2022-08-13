## IMPORTS
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from os.path import exists

#REQUEST INTERCEPTOR FUNCTION (ADDS CUSTOM HEADERS)
def req_int(req):
    del req.headers['x-asbd-id']  
    req.headers['x-asbd-id'] = head1  
    del req.headers['x-csrftoken']  
    req.headers['x-csrftoken'] = head2  
    del req.headers['x-ig-app-id']  
    req.headers['x-ig-app-id'] = head3  
    del req.headers['Referer']  
    req.headers['x-ig-www-claim'] = head4  

## CONFIG
conf = open("config.json", "r")
conf_json = json.loads(conf.read())
count = 12                  #nº OF USERS TO GRAB AT ONCE
sleep = 10                   #SECONDS TO SLEEP
me = conf_json['me']        #INSTAGRAM USER CODE
head1 = conf_json['head1']  #x-asbd-id
head2 = conf_json['head2']  #x-csrftoken
head3 = conf_json['head3']  #x-ig-app-id
head4 = conf_json['head4']  #x-ig-www-claim
print('Using headers:', [head1,head2,head3,head4])

## INITIALIZE
#CREATE DRIVER AND INITIALIZE
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://instagram.com')
input('Login and press enter')

#SET INTERCEPTOR
driver.request_interceptor = req_int

## GRAB ALL FOLLOWING FOR 'ME'
max_id = 1
friend = me
followers = []

#EXECUTE UNTIL ALL FOLLOWING ARE GRABBED
while True:
    driver.get('https://i.instagram.com/api/v1/friendships/' + friend + '/following/?count=' + str(count) + '&max_id=' + str(max_id))
    element = driver.find_element('tag name','pre')
    response = element.get_attribute('innerHTML')
    res_json = json.loads(response)
    users = res_json["users"]
    #LOOP THROUGH ALL NEW USERS AND APPEND THEM TO ME'S FOLLOWING
    for u in users:
        followers.append(u)
        print('Users:',len(followers),end='\r')
    #BREAK LOOP WHEN big_list IS FALSE
    if not res_json["big_list"]:
        break
    max_id = max_id + count
    time.sleep(sleep)

myfollowing = followers.copy()
textfile = open('ME.json', 'w')
textfile.write(json.dumps(followers))
textfile.close()

print(len(followers), 'where obtained for your account')

## GRAB ALL FOLLOWERS FOR EACH OF ME'S FRIENDS
for friend_obj in myfollowing:
    max_id = 1
    friend = str(friend_obj['pk'])
    if exists('export/' + friend_obj["username"]):
        continue
    followers = []
    while True:
        driver.get('https://i.instagram.com/api/v1/friendships/' + friend + '/followers/?count=' + str(count) + '&max_id=' + str(max_id) + '&search_surface=follow_list_page')
        element = driver.find_element('tag name','pre')
        response = element.get_attribute('innerHTML')
        res_json = json.loads(response)
        users = res_json["users"]
        for u in users:
            followers.append(u)
            print('Users:',len(followers),end='\r')
        if not res_json["big_list"]:
            break
        max_id = max_id + count
        time.sleep(sleep)

    textfile = open('export/' + friend_obj['username'] + '.json', 'w')
    textfile.write(json.dumps(followers))
    textfile.close()

    print(friend_obj['username'] + ' has ', len(followers), ' followers')

input("End of code")