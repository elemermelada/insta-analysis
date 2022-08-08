## IMPORTS
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

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

## PARAM DEFINITION
count = 99                                                      #nº OF USERS TO GRAB AT ONCE
me = '336923518'                                                #INSTAGRAM USER CODE
head1 = '198387'                                                #x-asbd-id
head2 = 'gmEEiuqugChMe6nWYL9qS8RcNALSymFr'                      #x-csrftoken
head3 = '936619743392459'                                       #x-ig-app-id
head4 = 'hmac.AR0RIUxUnDNk-raCJddgxtYop_Lo-Rk1ZcuspO3MCreuCli9' #x-ig-www-claim
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
    time.sleep(0.2)

myfollowing = followers.copy()
textfile = open('ME_' + friend + '.json', 'w')
textfile.write(json.dumps(followers))
textfile.close()

print(len(followers), 'where obtained for your account')

## GRAB ALL FOLLOWERS FOR EACH OF ME'S FRIENDS
for friend_obj in myfollowing:
    max_id = 1
    friend = str(friend_obj['pk'])
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
        time.sleep(0.2)

    textfile = open(friend_obj['username'] + '.json', 'w')
    textfile.write(json.dumps(followers))
    textfile.close()

    print(friend_obj['username'] + ' has ', len(followers), ' followers')


input("End of code")