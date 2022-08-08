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

## RUNTIME
#CREATE DRIVER AND INITIALIZE
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://instagram.com')
input('Login and press enter')

#GRAB DESIRED HEADERS OR FALLBACK TO KNOWN HEADERS + SET INTERCEPTOR
head1 = input('x-asbd-id: ')
if head1 == '':
    head1 = '198387'
head2 = input('x-csrftoken: ')
if head2 == '':
    head2 = 'Mq8zaku3nylpTQfTk9AsrPIARhswomP3'
head3 = input('x-ig-app-id: ')
if head3 == '':
    head3 = '936619743392459'
head4 = input('x-ig-www-claim: ')
if head4 == '':
    head4 = 'hmac.AR0RIUxUnDNk-raCJddgxtYop_Lo-Rk1ZcuspO3MCreuCrfd'
print('Using headers:', [head1,head2,head3,head4])
driver.request_interceptor = req_int

#MAKE A REQUEST AND GRAB RESPONSE
friend = '4118873852'
max_id = 1
count = 99
followers = []

#EXECUTE UNTIL ALL FOLLOWERS ARE GRABBED
while True:
    driver.get('https://i.instagram.com/api/v1/friendships/' + friend + '/followers/?count=' + str(count) + '&max_id=' + str(max_id) + '&search_surface=follow_list_page')
    element = driver.find_element('tag name','pre')
    response = element.get_attribute('innerHTML')
    res_json = json.loads(response)
    users = res_json["users"]
    #LOOP THROUGH ALL NEW USERS AND APPEND THEM TO FRIEND'S FOLLOWERS
    for u in users:
        followers.append(u)
        print('Users:',len(followers),end='\r')
    #BREAK LOOP WHEN USERS IS 0
    #if len(res_json["users"])<count:
    #if not res_json["big_list"]):
    if len(res_json["users"])==0:
        break
    max_id = max_id + count
    time.sleep(0.2)

textfile = open(friend + '.json', 'w')
textfile.write(json.dumps(followers))
textfile.close()

print(len(followers))
input("End of code")