from stations import stations
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
    }  

d_station = stations('北京', '武汉')
date = '2017-09-18'
from_station = d_station[0]
to_station = d_station[1]
url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
#url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=2017-09-16&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=WHN&purpose_codes=ADULT'
#req =urllib.request.Request(url,headers=headers)  
# ssl._create_default_https_context = ssl._create_unverified_context 
#html = urllib.request.urlopen(req).read().decode()  
#print(html)

res = requests.get(url, headers = headers,verify=False)
if res.status_code == 200:
    # print(res.__dict__['url'])
    r = res.json()
    available_trains = []
    for i in r['data']['result']:
        available_trains.append(re.findall(u'\|[GDKZT]\d{1,4}\|',i)[0].strip('|'))
else:
    print(res.status_code)
print(available_trains)

#30位是二等座，28位是硬卧
