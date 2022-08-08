## IMPORTS
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

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
count = 10
#EXECUTE UNTIL ALL FOLLOWERS ARE GRABBED (LAST RESPONSE HAS LESS 'USERS' THAN COUNT)
while True:
    driver.get('https://i.instagram.com/api/v1/friendships/' + friend + '/followers/?count=' + str(count) + '&max_id=' + str(max_id) + '&search_surface=follow_list_page')
    element = driver.find_element('tag name','pre')
    response = element.get_attribute('innerHTML')
    res_json = json.loads(response)
    print(res_json["users"])

    if res_json["users"] < count-1:


    max_id = max_id + count

input("End of code")