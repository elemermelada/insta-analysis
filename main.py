from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def req_int(req):
    del req.headers['x-asbd-id']  
    req.headers['x-asbd-id'] = '198387'  
    del req.headers['x-csrftoken']  
    req.headers['x-csrftoken'] = 'Mq8zaku3nylpTQfTk9AsrPIARhswomP3'  
    del req.headers['x-ig-app-id']  
    req.headers['x-ig-app-id'] = '936619743392459'  
    del req.headers['Referer']  
    req.headers['x-ig-www-claim'] = 'hmac.AR0RIUxUnDNk-raCJddgxtYop_Lo-Rk1ZcuspO3MCreuCrfd'  

def res_int(req,res):
    print(res.body)


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://instagram.com')
input('Login first')

driver.request_interceptor = req_int
driver.response_interceptor = res_int
driver.get('https://i.instagram.com/api/v1/friendships/4118873852/followers/?count=10&max_id=580&search_surface=follow_list_page')
#print(driver.page_source)

input("End of code")