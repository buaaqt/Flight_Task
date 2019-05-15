from prettytable import PrettyTable
import urllib.request
from bs4 import BeautifulSoup
import requests
import json
import time
import sys
import csv
import datetime
import random
import os

# 国内主要机场表
city = {
    '北京': 'BJS',
    '重庆': 'CKG',
    '成都': 'CTU',
    '长沙': 'CSX',
    '广州': 'CAN',
    '合肥': 'HFE',
    '南京': 'NKG',
    '青岛': 'TAO',
    '厦门': 'XMN',
    '上海': 'SHA',
    '深圳': 'SZX',
    '天津': 'TSN',
    '武汉': 'WUH',
    '西安': 'SIA'
}

# 爬虫headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Content-Type": "application/json",
    "origin": "https://flights.ctrip.com",
    "referer": "https://flights.ctrip.com/itinerary/roundtrip/",
    "Cookie": """"""
}

# 中国天气网的相关编号
wea_city_code = {
    '北京': '101010100',
    '重庆': '101040100',
    '成都': '101270101',
    '长沙': '101250101',
    '广州': '101280101',
    '合肥': '101220101',
    '南京': '101190101',
    '青岛': '101120201',
    '厦门': '101230201',
    '上海': '101020100',
    '深圳': '101280601',
    '天津': '101030100',
    '武汉': '101200101',
    '西安': '101110101'
}

# 爬ip代理池的网站url
proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
# 携程的url
url = 'http://flights.ctrip.com/itinerary/api/12808/products'

# 爬下来后的ip代理池存入proxiesList
proxiesList = []
tempProxiesList = []


# 获取ip代理池，代理池size固定为30，除非到30之前ip获取代码出错

def get_proxies():
    global proxy_url
    cnt = 0

    # 简单的requests获取网页
    response = requests.get(proxy_url, timeout=30)
    proxies_list = response.text.split('\n')
    for proxy_str in proxies_list:
        try:
            proxy_json = json.loads(proxy_str)
        except Exception as e:
            print(str(e))
            print('==============get_proxies_pool_error===============')
            print('==================>'+proxy_str+'<==================')
            break
        else:
            host = proxy_json['host']
            port = proxy_json['port']
            type = proxy_json['type']
            # 检查爬到的ip是否有效
            flag = verify(host, port, type)
            if flag:
                cnt += 1
            if cnt == 30:
                print('==============generate_proxies_pool_done===============')
                break
            # 到30个为止，太多也没有必要
    return


# 检查ip是否有效的函数，若有效且为'https'则返回True，否则返回False
def verify(ip,  port, type):
    global city, headers, url, proxiesList, tempProxiesList

    # 固定查询北京到南京的当日航班数据，作为测试
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": 'false',
        "hasBaby": 'false',
        "searchIndex": 1,
        "airportParams": [{"dcity": city.get("北京"), "acity": city.get("上海"), "dcityname": "北京", "acityname": "上海",
                           "date": str(datetime.date.today())}]
    }

    # 生成string格式的ip
    proxy = {}
    p = ip+":"+str(port)

    # 去携程网站试查询ip是否有效
    # 只检测'https'型的代理ip
    # 如果有效，就加入全局列表proxiesList，否则直接pass
    try:
        if type == 'https':
            response = json.loads(
                requests.post(url, data=json.dumps(request_payload), headers=headers, proxies={"https":p},
                              timeout=30).text)
            if response is None or response.get('data').get('error') is not None:
                return False

    except Exception as e:
        pass
    else:
        if type == "https":
            proxy['https'] = p
            tempProxiesList.append(proxy)
            print(proxy)
            return True

    return False


# 爬取天气数据，返回一个列表['气温','天气','风向']
def wea(cityName, days):
    global wea_city_code

    # requests天气网页
    # 生成需要查询的城市的url
    url = "http://www.weather.com.cn/weather/" + wea_city_code.get(cityName) + ".shtml"
    header = ("User-Agent",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
    # 获取网页
    opener = urllib.request.build_opener()
    opener.addheaders = [header]
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()
    html = html.decode('utf-8')

    # find出需要的数据
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')

    # 需要的几个数据容器
    day = li[days]
    ans = []
    inf = day.find_all('p')

    # 防止再当天晚上无法获取当日最高气温，若没有就默认30℃
    if inf[1].find('span') is None:
        temperature_highest = "30"
    else:
        temperature_highest = inf[1].find('span').string
        temperature_highest = temperature_highest.replace('℃', '')

    # 获取当日最低气温
    temperature_lowest = inf[1].find('i').string
    temperature_lowest = temperature_lowest.replace('℃', '')
    # 生成最高气温和最低气温统一的string，加入返回list
    temperature = "高温" + temperature_highest + "℃~低温" + temperature_lowest + "℃"
    ans.append(temperature)
    # 天气情况加入返回list
    ans.append(inf[0].string)

    # 获取风力，风向，填入list
    winDir = inf[2].find('span').get('title')
    winLev = inf[2].find('i').string
    win = winDir + " " + winLev
    ans.append(win)

    return ans


# 获取航班json数据
def get_flight_json(url, request_payload, headers):
    global proxiesList
    attempts = 0
    success = False
    proxiesLen = len(proxiesList)

    # 若爬取失败，则换个ip代理，重试所有的ip
    while attempts < 10 and not success:
        try:
            # 随机选择ip代理进行爬虫
            index = random.randint(0, proxiesLen - 1)
            proxies = proxiesList[index]
            response = json.loads(
                requests.post(url, data=json.dumps(request_payload), headers=headers, proxies=proxies,
                              timeout=30).text)
            if response is None or response.get('data').get('error') is not None:
                print(response)
                attempts += 1
                print("Error ip killed!", proxies)

            success = True
        except Exception as e:
            attempts += 1
            print(str(e))
            if attempts == 10:
                break

    if success is False:
        return None
    return response


# 航班数据爬取函数
def crawler(dcity, acity, date, csv_write, wea_info, i):
    global city, headers, url, proxiesList

    # 航班数据文件名
    fileName = 'flight'+str(i)+'.txt'

    # user_agent池，随机选择user_agent，防止网站反爬虫
    user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    # requests需要的查询信息
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": 'false',
        "hasBaby": 'false',
        "searchIndex": 1,
        "airportParams": [
            {"dcity": city.get(dcity), "acity": city.get(acity), "dcityname": dcity, "acityname": acity, "date": date}]
    }

    try:
        response = get_flight_json(url, request_payload, headers)
        if response is None:
            print("Error!")
            return

        # 若ip被封杀，则换ip一直到成功为止
        routeList = response.get('data').get('routeList')
        if routeList is None:
            if response.get('data').get('error') is not None:
                attempts = 0
                success = False

                while attempts < 10 and not success:
                    try:
                        response = get_flight_json(url, request_payload, headers)
                        if response is None or response.get('data').get('error') is not None:
                            attempts += 1
                            if attempts == 10:
                                break
                        else:
                            if response.get('data').get('error') is None:
                                success = True

                    except Exception as e:
                        attempts += 1
                        print(str(e))
                        if attempts == 10:
                            break

        # 若不是ip封杀出现的错误，则正常输出错误信息，直接返回
        routeList = response.get('data').get('routeList')
        if routeList is None:
            print("Error rsp: {}, jump this req".format(response))
            return

        # 文件写入
        with open(fileName, 'a') as f:
            hasItemFlag = False
            firstLoopFlag = True

            # 对每一个航班方案进行处理
            for route in routeList:
                # 若不是纯飞机方案，则舍弃
                if route.get('routeType') != 'Flight':
                    break

                # 若无相关信息，则处理下一个
                legs = route.get('legs')[0]
                if legs is None:
                    continue

                else:
                    # 若是第一轮，则输出开头的格式
                    if firstLoopFlag is True:
                        firstLoopFlag = False
                        hasItemFlag = True
                        f.writelines('[\n')
                        f.writelines('{')
                    # 若不是第一轮，则输出逗号和相关格式
                    else:
                        f.writelines(',{')

                    # 填入相关信息
                    info_list = []
                    flight = legs.get('flight')

                    f.writelines(str('\'出发地\':\'' + dcity + '\','))
                    f.writelines(str('\'出发机场\':\'' + flight.get('departureAirportInfo').get('airportName') + '\','))
                    f.writelines(str('\'目的地\':\'' + acity + '\','))
                    f.writelines(str('\'目的机场\':\'' + flight.get('arrivalAirportInfo').get('airportName') + '\','))
                    f.writelines(str('\'出发时间\':\'' + flight.get('departureDate') + '\','))
                    f.writelines(str('\'到达时间\':\'' + flight.get('arrivalDate') + '\','))
                    f.writelines('\'飞行时间\':\'待完善\',')
                    f.writelines(str('\'航空公司\':\'' + flight.get('airlineName') + '\','))
                    f.writelines(str('\'航班编号\':\'' + flight.get('flightNumber') + '\','))
                    f.writelines(str('\'最低价格\':\'' + str(legs.get('characteristic').get('lowestPrice')) + '\','))
                    f.writelines('\'禁运事项\':\'易燃易爆物品、枪支弹药、管制刀具、有毒物质\',')
                    f.writelines(str('\'AI预测延误概率\':\'' + flight.get('punctualityRate') + '\''))
                    f.writelines('}\n')

                    # 填入csv文件的信息
                    info_list.append(date)
                    info_list.append(flight.get('departureAirportInfo').get('airportName'))
                    info_list.append(flight.get('arrivalAirportInfo').get('airportName'))
                    info_list.append(flight.get('departureDate'))
                    info_list.append(flight.get('arrivalDate'))
                    info_list.extend(wea_info)
                    info_list.append(flight.get('punctualityRate'))
                    csv_write.writerow(info_list)

            # 若非空，则输出结尾格式
            if hasItemFlag is True:
                f.writelines(']')

    # 异常处理
    except Exception as e:
        print('爬取错误：' + str(e))
        return


if __name__ == "__main__":

    # 获取今日日期，并确定爬取当前日期后一周的航班信息
    today = str(datetime.date.today())
    date_list = today.split('-')
    begin = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    end = begin+datetime.timedelta(6)

    # 遍历此后一周的每一天
    for i in range((end - begin).days + 1):

        # 获取ip代理池
        tempProxiesList = []

        get_proxies()
        proxiesList = tempProxiesList
        print(proxiesList)

        day = begin+datetime.timedelta(days=i)
        csv_out = open('Data'+str(i)+'.csv', 'w', newline='')
        head = ['日期', '出发地', '目的地', '出发时间', '到达时间', '气温', '风向', '天气状况', '延误率']
        csv_write = csv.writer(csv_out, dialect='excel')
        csv_write.writerow(head)

        # 刷空flight.txt原有的信息
        with open('flight'+str(i)+'.txt', 'w') as f:
            f.write('\n')

        # 双重遍历城市列表
        for dcity in city:
            # 获取目的城市的天气，在这层爬取是为了减少天气网站的访问次数，避免被封杀
            weaInfo = wea(dcity, i)
            for acity in city:
                if dcity == acity:
                    continue

                print(dcity, '------->', acity, str(day))
                crawler(dcity, acity, str(day), csv_write, weaInfo, i)

        csv_out.close()

        time.sleep(60)

    # p = os.system('/data/wwwroot/web/web/code/GenerateIndex.py')
    # print('launch GenerateIndex.py:',p)
