from stations import stations
import requests
import re, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning



def query(from_station, to_station, date, train_nums):
    '''
    给定出发的火车站，到达的火车站，所想要的日期还有想要刷票的车次（list）
    有票就锁定，没票就一直刷
    '''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    headers = {  
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }  
    d_station = stations(from_station, to_station)
    from_station = d_station[0]
    to_station = d_station[1]
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, from_station, to_station
        )
    available_trains, train_list, query_time = [], [], 0
    while True:
        if not available_trains:
            res = requests.get(url, headers = headers, verify = False)
            if res.status_code == 200:
                try:
                    r = res.json()['data']['result']
                except Exception as e:
                    print(res.__dict__['url'])
                    break
                for i in r:
                    available_trains.append(re.findall(u'\|[GDKZT]\d{1,4}\|',i)[0].strip('|'))
                
                for j in train_nums:
                    train_list.append(available_trains.index(j))
            else:
                print('status_code:%d' %res.status_code)
                print(url)
                time.sleep(5)
                continue
        try:
            res = requests.get(url, headers = headers,verify=False)
            r = res.json()['data']['result']
        except Exception as e:
            print(e)
            print(url)
            time.sleep(5)
            continue
        for i in train_list:
            tmp = r[i].split('|')
            if tmp[28] != '' and tmp[28] != '无':
                print(available_trains[i] + '二等座有票了')
                break
            if tmp[30] != '' and tmp[30] != '无':
                print(available_trains[i] + '硬卧有票了')
                break
        print('第%d次查询' %query_time)
        query_time += 1
        time.sleep(5)

if __name__ == '__main__':
    query('北京', '武汉', '2017-09-30', ['Z37', 'Z207', 'Z285', 'Z53'])


#30位是二等座，28位是硬卧
