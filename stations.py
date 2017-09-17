import re, os, json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def stations(from_station, to_station):
    '''
    返回车站的12306代码字典
    '''
    if os.path.exists('stations.txt'):
        fr = open('station.txt', 'r')
        js = fr.read()
        d_station = json.load(js)
    else:
        station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9025'
        respond_station = requests.get(station_url, verify=False)
        stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', respond_station.text)
        d_station = dict(stations)
        f = open('station.txt', 'w')
        jsObj = json.dumps(d_station) 
        f.write(jsObj)
        f.close()
    
    return [d_station[from_station], d_station[to_station]]

if __name__ == '__main__':
    print(stations('武汉', '北京'))