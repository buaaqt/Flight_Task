from prettytable import PrettyTable
from bs4 import BeautifulSoup
import requests
import json
import time
import sys
import csv

##city = {'阿尔山': 'YIE', '阿克苏': 'AKU', '阿拉善右旗': 'RHT', '阿拉善左旗': 'AXF', '阿勒泰': 'AAT', '阿里': 'NGQ', '澳门': 'MFM',
##      '安庆': 'AQG', '安顺': 'AVA', '鞍山': 'AOG', '巴彦淖尔': 'RLK', '百色': 'AEB', '包头': 'BAV', '保山': 'BSD', '北海': 'BHY',
##      '北京': 'BJS', '白城': 'DBC', '白山': 'NBS', '毕节': 'BFJ', '博乐': 'BPL', '重庆': 'CKG', '昌都': 'BPX', '常德': 'CGD',
##      '常州': 'CZX', '朝阳': 'CHG', '成都': 'CTU', '池州': 'JUH', '赤峰': 'CIF', '揭阳': 'SWA', '长春': 'CGQ', '长沙': 'CSX',
##      '长治': 'CIH', '承德': 'CDE', '沧源': 'CWJ', '达县': 'DAX', '大理': 'DLU', '大连': 'DLC', '大庆': 'DQA', '大同': 'DAT',
##      '丹东': 'DDG', '稻城': 'DCY', '东营': 'DOY', '敦煌': 'DNH', '芒市': 'LUM', '额济纳旗': 'EJN', '鄂尔多斯': 'DSN', '恩施': 'ENH',
##      '二连浩特': 'ERL', '佛山': 'FUO', '福州': 'FOC', '抚远': 'FYJ', '阜阳': 'FUG', '赣州': 'KOW', '格尔木': 'GOQ', '固原': 'GYU',
##      '广元': 'GYS', '广州': 'CAN', '贵阳': 'KWE', '桂林': 'KWL', '哈尔滨': 'HRB', '哈密': 'HMI', '海口': 'HAK', '海拉尔': 'HLD',
##      '邯郸': 'HDG', '汉中': 'HZG', '杭州': 'HGH', '合肥': 'HFE', '和田': 'HTN', '黑河': 'HEK', '呼和浩特': 'HET', '淮安': 'HIA',
##      '怀化': 'HJJ', '黄山': 'TXN', '惠州': 'HUZ', '鸡西': 'JXA', '济南': 'TNA', '济宁': 'JNG', '加格达奇': 'JGD', '佳木斯': 'JMU',
##      '嘉峪关': 'JGN', '金昌': 'JIC', '金门': 'KNH', '锦州': 'JNZ', '嘉义': 'CYI', '西双版纳': 'JHG', '建三江': 'JSJ', '晋江': 'JJN',
##      '井冈山': 'JGS', '景德镇': 'JDZ', '九江': 'JIU', '九寨沟': 'JZH', '喀什': 'KHG', '凯里': 'KJH', '康定': 'KGT', '克拉玛依': 'KRY',
##      '库车': 'KCA', '库尔勒': 'KRL', '昆明': 'KMG', '拉萨': 'LXA', '兰州': 'LHW', '黎平': 'HZH', '丽江': 'LJG', '荔波': 'LLB',
##      '连云港': 'LYG', '六盘水': 'LPF', '临汾': 'LFQ', '林芝': 'LZY', '临沧': 'LNJ', '临沂': 'LYI', '柳州': 'LZH', '泸州': 'LZO',
##      '洛阳': 'LYA', '吕梁': 'LLV', '澜沧': 'JMJ', '龙岩': 'LCX', '满洲里': 'NZH', '梅州': 'MXZ', '绵阳': 'MIG', '漠河': 'OHE',
##      '牡丹江': 'MDG', '马祖': 'MFK', '南昌': 'KHN', '南充': 'NAO', '南京': 'NKG', '南宁': 'NNG', '南通': 'NTG', '南阳': 'NNY',
##      '宁波': 'NGB', '宁蒗': 'NLH', '攀枝花': 'PZI', '普洱': 'SYM', '齐齐哈尔': 'NDG', '黔江': 'JIQ', '且末': 'IQM', '秦皇岛': 'BPE',
##      '青岛': 'TAO', '庆阳': 'IQN', '衢州': 'JUZ', '日喀则': 'RKZ', '日照': 'RIZ', '三亚': 'SYX', '厦门': 'XMN', '上海': 'SHA',
##      '深圳': 'SZX', '神农架': 'HPG', '沈阳': 'SHE', '石家庄': 'SJW', '塔城': 'TCG', '台州': 'HYN', '太原': 'TYN', '扬州': 'YTY',
##      '唐山': 'TVS', '腾冲': 'TCZ', '天津': 'TSN', '天水': 'THQ', '通辽': 'TGO', '铜仁': 'TEN', '吐鲁番': 'TLQ', '万州': 'WXN',
##      '威海': 'WEH', '潍坊': 'WEF', '温州': 'WNZ', '文山': 'WNH', '乌海': 'WUA', '乌兰浩特': 'HLH', '乌鲁木齐': 'URC', '无锡': 'WUX',
##      '梧州': 'WUZ', '武汉': 'WUH', '武夷山': 'WUS', '西安': 'SIA', '西昌': 'XIC', '西宁': 'XNN', '锡林浩特': 'XIL', '香格里拉(迪庆)': 'DIG',
##      '襄阳': 'XFN', '兴义': 'ACX', '徐州': 'XUZ', '香港': 'HKG', '烟台': 'YNT', '延安': 'ENY', '延吉': 'YNJ', '盐城': 'YNZ', '伊春': 'LDS',
##      '伊宁': 'YIN', '宜宾': 'YBP', '宜昌': 'YIH', '宜春': 'YIC', '义乌': 'YIW', '银川': 'INC', '永州': 'LLF', '榆林': 'UYN', '玉树': 'YUS',
##      '运城': 'YCU', '湛江': 'ZHA', '张家界': 'DYG', '张家口': 'ZQZ', '张掖': 'YZY', '昭通': 'ZAT', '郑州': 'CGO', '中卫': 'ZHY', '舟山': 'HSN',
##      '珠海': 'ZUH', '遵义(茅台)': 'WMT', '遵义(新舟)': 'ZYI'}
city = {
        '北京': 'BJS', '重庆': 'CKG',
        '成都': 'CTU', '长沙': 'CSX',
        '广州': 'CAN',
        '合肥': 'HFE',
        '南京': 'NKG', 
        '青岛': 'TAO', '厦门': 'XMN', '上海': 'SHA',
        '深圳': 'SZX',
        '天津': 'TSN',
        '武汉': 'WUH', '西安': 'SIA'}

wea_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
wea_url = "https://www.huoche.net/jichangtianqi/"
wea_resp = requests.get(wea_url, headers = wea_headers)
wea_soup = BeautifulSoup(wea_resp.text, 'lxml')
wea_soup_list = wea_soup.select('div[class="cont_gnzytq"] dl dd a')
airport_list = []

class Airport:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        
def xiecheng(dcity,acity,date,csv_ptr):
    global city

    # date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Content-Type": "application/json",
        # "origin": "https://flights.ctrip.com",
        "referer": "https://flights.ctrip.com/itinerary/roundtrip/",
        "Cookie": """"""
     }


    url = 'http://flights.ctrip.com/itinerary/api/12808/products'
    request_payload = {"flightWay":"Oneway",
            "classType":"ALL",
            "hasChild":'false',
            "hasBaby":'false',
            "searchIndex":1,
            "airportParams":[{"dcity":city.get(dcity),"acity":city.get(acity),"dcityname":dcity,"acityname":acity,"date":date}]}
            

    # 这里传进去的参数必须为 json 格式
    response = json.loads(requests.post(url,data=json.dumps(request_payload),headers=headers).text)
    routeList = response.get('data').get('routeList')

    if routeList is None:
##      print("Error rsp: {}, jump this req".format(response))
        return
#    print(routeList)
    table=PrettyTable(["Airline","FlightNumber","DepartureDate",'ArrivalDate','PunctualityRate','LowestPrice'])
    if len(routeList[0].get('legs')) == 1:
            print('[')

    airport_url = 'https://www.huoche.net/jichangtianqi-'+city.get(dcity)+'/'
    request = requests.get(airport_url, headers = wea_headers, timeout=100)
    subsoup = BeautifulSoup(request.text, 'lxml')
    
    dict_cnt = 0
    for route in routeList:
        if len(route.get('legs')) == 1:
            if dict_cnt == 0:
                print('{')
            else:
                print(',{')
            
            info_list = []
            legs = route.get('legs')[0]
            flight = legs.get('flight')
##          info['Airline'] = flight.get('airlineName') 
##          info['FlightNumber'] = flight.get('flightNumber')
##          info['DepartureDate'] = flight.get('departureDate')[-8:-3]
##          info['ArrivalDate'] = flight.get('arrivalDate')[-8:-3]
##          info['PunctualityRate'] = flight.get('punctualityRate')
##          info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')
##          
##          table.add_row(info.values())
            print('\'出发地\':\'',dcity,'\',')
            print('\'目的地\':\'',acity,'\',')
            print('\'出发时间\':\'',flight.get('departureDate'),'\',')
            print('\'到达时间\':\'',flight.get('arrivalDate'),'\',')
            print('\'飞行时间\':\'待完善\',')
            print('\'航空公司\':\'',flight.get('airlineName') ,'\',')
            print('\'航班编号\':\'',flight.get('flightNumber') ,'\',')
            print('\'最低价格\':\'',legs.get('characteristic').get('lowestPrice') ,'\',')
            print('\'禁运事项\':\'易燃易爆物品、枪支弹药、管制刀具、有毒物质\',')
            print('\'AI预测延误概率\':\'',flight.get('punctualityRate') ,'\'')
            print('}\n')
            info_list.append(date)
            info_list.append(flight.get('departureAirportInfo').get('airportName'))
            info_list.append(flight.get('arrivalAirportInfo').get('airportName'))
            info_list.append(flight.get('departureDate'))
            info_list.append(flight.get('arrivalDate'))

            tem = subsoup.select('div[class="today_data_w"] li[class="fon14 fB"] span')
            if len(tem) == 1:
                info_list.append(tem[0].get_text())
            else:
                info_list.append('数据暂无')
                            
            wea = subsoup.select('div[class="today_data_w"] li[class="tqpng_01"] span')
            if len(wea) == 1:
                info_list.append(wea[0].get_text())
            else:
                info_list.append('数据暂无')
                            
            info_list.append('无持续风向')
            info_list.append(flight.get('punctualityRate'))
            csv_ptr.writerow(info_list)
            dict_cnt = dict_cnt+1

##  print(dcity,'------->',acity,date)
##  print(table)
    if len(routeList[0].get('legs')) == 1:
            print(']')

if __name__ == "__main__":
    
##    output = sys.stdout
##    outputfile = open('flight.txt','w')
##    sys.stdout = outputfile
    for i in wea_soup_list:
        airport_list.append(Airport(i.get_text(), "https:"+i['href']))
        
    csv_out = open('Data.csv','w',newline = '')
    head = ['日期','出发地','目的地','出发时间','到达时间','气温','风向','天气状况','延误率']
    csv_write = csv.writer(csv_out,dialect = 'excel')
    csv_write.writerow(head)
    
    for dcity in city:
        for acity in city:
            if dcity == acity:
                continue
                # print("Depart: {}, Arrival: {}".format(dcity, acity))
            xiecheng(dcity, acity, "2019-04-27",csv_write)
            time.sleep(1)
##    xiecheng("北京","重庆","2019-04-29",csv_write)
##    xiecheng("北京","成都","2019-04-29",csv_write)
##    xiecheng("北京","长沙","2019-04-29",csv_write)
##    xiecheng("北京","广州","2019-04-29",csv_write)
##    xiecheng("北京","合肥","2019-04-29",csv_write)
##    xiecheng("北京","南京","2019-04-29",csv_write)
##    xiecheng("北京","青岛","2019-04-29",csv_write)
##    xiecheng("北京","厦门","2019-04-29",csv_write)
##    xiecheng("北京","上海","2019-04-29",csv_write)
##    xiecheng("北京","深圳","2019-04-29",csv_write)
##    xiecheng("北京","天津","2019-04-29",csv_write)
##    xiecheng("北京","武汉","2019-04-29",csv_write)
##    xiecheng("北京","西安","2019-04-29",csv_write)
##    xiecheng("重庆","北京","2019-04-29",csv_write)
##    xiecheng("重庆","成都","2019-04-29",csv_write)
##    xiecheng("重庆","长沙","2019-04-29",csv_write)
##    xiecheng("重庆","广州","2019-04-29",csv_write)
##    xiecheng("重庆","合肥","2019-04-29",csv_write)
##    xiecheng("重庆","南京","2019-04-29",csv_write)
##    xiecheng("重庆","青岛","2019-04-29",csv_write)
##    xiecheng("重庆","厦门","2019-04-29",csv_write)
##    xiecheng("重庆","上海","2019-04-29",csv_write)
##    xiecheng("重庆","深圳","2019-04-29",csv_write)
##    xiecheng("重庆","天津","2019-04-29",csv_write)
##    xiecheng("重庆","武汉","2019-04-29",csv_write)
##    xiecheng("重庆","西安","2019-04-29",csv_write)
##    xiecheng("成都","北京","2019-04-29",csv_write)
##    xiecheng("成都","重庆","2019-04-29",csv_write)
##    xiecheng("成都","长沙","2019-04-29",csv_write)
##    xiecheng("成都","广州","2019-04-29",csv_write)
##    xiecheng("成都","合肥","2019-04-29",csv_write)
##    xiecheng("成都","南京","2019-04-29",csv_write)
##    xiecheng("成都","青岛","2019-04-29",csv_write)
##    xiecheng("成都","厦门","2019-04-29",csv_write)
##    xiecheng("成都","上海","2019-04-29",csv_write)
##    xiecheng("成都","深圳","2019-04-29",csv_write)
##    xiecheng("成都","天津","2019-04-29",csv_write)
##    xiecheng("成都","武汉","2019-04-29",csv_write)
##    xiecheng("成都","西安","2019-04-29",csv_write)
##    xiecheng("长沙","北京","2019-04-29",csv_write)
##    xiecheng("长沙","重庆","2019-04-29",csv_write)
##    xiecheng("长沙","成都","2019-04-29",csv_write)
##    xiecheng("长沙","广州","2019-04-29",csv_write)
##    xiecheng("长沙","合肥","2019-04-29",csv_write)
##    xiecheng("长沙","南京","2019-04-29",csv_write)
##    xiecheng("长沙","青岛","2019-04-29",csv_write)
##    xiecheng("长沙","厦门","2019-04-29",csv_write)
##    xiecheng("长沙","上海","2019-04-29",csv_write)
##    xiecheng("长沙","深圳","2019-04-29",csv_write)
##    xiecheng("长沙","天津","2019-04-29",csv_write)
##    xiecheng("长沙","武汉","2019-04-29",csv_write)
##    xiecheng("长沙","西安","2019-04-29",csv_write)
##    xiecheng("广州","北京","2019-04-29",csv_write)
##    xiecheng("广州","重庆","2019-04-29",csv_write)
##    xiecheng("广州","成都","2019-04-29",csv_write)
##    xiecheng("广州","长沙","2019-04-29",csv_write)
##    xiecheng("广州","合肥","2019-04-29",csv_write)
##    xiecheng("广州","南京","2019-04-29",csv_write)
##    xiecheng("广州","青岛","2019-04-29",csv_write)
##    xiecheng("广州","厦门","2019-04-29",csv_write)
##    xiecheng("广州","上海","2019-04-29",csv_write)
##    xiecheng("广州","深圳","2019-04-29",csv_write)
##    xiecheng("广州","天津","2019-04-29",csv_write)
##    xiecheng("广州","武汉","2019-04-29",csv_write)
##    xiecheng("广州","西安","2019-04-29",csv_write)
##    xiecheng("合肥","北京","2019-04-29",csv_write)
##    xiecheng("合肥","重庆","2019-04-29",csv_write)
##    xiecheng("合肥","成都","2019-04-29",csv_write)
##    xiecheng("合肥","长沙","2019-04-29",csv_write)
##    xiecheng("合肥","广州","2019-04-29",csv_write)
##    xiecheng("合肥","南京","2019-04-29",csv_write)
##    xiecheng("合肥","青岛","2019-04-29",csv_write)
##    xiecheng("合肥","厦门","2019-04-29",csv_write)
##    xiecheng("合肥","上海","2019-04-29",csv_write)
##    xiecheng("合肥","深圳","2019-04-29",csv_write)
##    xiecheng("合肥","天津","2019-04-29",csv_write)
##    xiecheng("合肥","武汉","2019-04-29",csv_write)
##    xiecheng("合肥","西安","2019-04-29",csv_write)
##    xiecheng("南京","北京","2019-04-29",csv_write)
##    xiecheng("南京","重庆","2019-04-29",csv_write)
##    xiecheng("南京","成都","2019-04-29",csv_write)
##    xiecheng("南京","长沙","2019-04-29",csv_write)
##    xiecheng("南京","广州","2019-04-29",csv_write)
##    xiecheng("南京","合肥","2019-04-29",csv_write)
##    xiecheng("南京","青岛","2019-04-29",csv_write)
##    xiecheng("南京","厦门","2019-04-29",csv_write)
##    xiecheng("南京","上海","2019-04-29",csv_write)
##    xiecheng("南京","深圳","2019-04-29",csv_write)
##    xiecheng("南京","天津","2019-04-29",csv_write)
##    xiecheng("南京","武汉","2019-04-29",csv_write)
##    xiecheng("南京","西安","2019-04-29",csv_write)
##    xiecheng("青岛","北京","2019-04-29",csv_write)
##    xiecheng("青岛","重庆","2019-04-29",csv_write)
##    xiecheng("青岛","成都","2019-04-29",csv_write)
##    xiecheng("青岛","长沙","2019-04-29",csv_write)
##    xiecheng("青岛","广州","2019-04-29",csv_write)
##    xiecheng("青岛","合肥","2019-04-29",csv_write)
##    xiecheng("青岛","南京","2019-04-29",csv_write)
##    xiecheng("青岛","厦门","2019-04-29",csv_write)
##    xiecheng("青岛","上海","2019-04-29",csv_write)
##    xiecheng("青岛","深圳","2019-04-29",csv_write)
##    xiecheng("青岛","天津","2019-04-29",csv_write)
##    xiecheng("青岛","武汉","2019-04-29",csv_write)
##    xiecheng("青岛","西安","2019-04-29",csv_write)
##    xiecheng("厦门","北京","2019-04-29",csv_write)
##    xiecheng("厦门","重庆","2019-04-29",csv_write)
##    xiecheng("厦门","成都","2019-04-29",csv_write)
##    xiecheng("厦门","长沙","2019-04-29",csv_write)
##    xiecheng("厦门","广州","2019-04-29",csv_write)
##    xiecheng("厦门","合肥","2019-04-29",csv_write)
##    xiecheng("厦门","南京","2019-04-29",csv_write)
##    xiecheng("厦门","青岛","2019-04-29",csv_write)
##    xiecheng("厦门","上海","2019-04-29",csv_write)
##    xiecheng("厦门","深圳","2019-04-29",csv_write)
##    xiecheng("厦门","天津","2019-04-29",csv_write)
##    xiecheng("厦门","武汉","2019-04-29",csv_write)
##    xiecheng("厦门","西安","2019-04-29",csv_write)
##    xiecheng("上海","北京","2019-04-29",csv_write)
##    xiecheng("上海","重庆","2019-04-29",csv_write)
##    xiecheng("上海","成都","2019-04-29",csv_write)
##    xiecheng("上海","长沙","2019-04-29",csv_write)
##    xiecheng("上海","广州","2019-04-29",csv_write)
##    xiecheng("上海","合肥","2019-04-29",csv_write)
##    xiecheng("上海","南京","2019-04-29",csv_write)
##    xiecheng("上海","青岛","2019-04-29",csv_write)
##    xiecheng("上海","厦门","2019-04-29",csv_write)
##    xiecheng("上海","深圳","2019-04-29",csv_write)
##    xiecheng("上海","天津","2019-04-29",csv_write)
##    xiecheng("上海","武汉","2019-04-29",csv_write)
##    xiecheng("上海","西安","2019-04-29",csv_write)
##    xiecheng("深圳","北京","2019-04-29",csv_write)
##    xiecheng("深圳","重庆","2019-04-29",csv_write)
##    xiecheng("深圳","成都","2019-04-29",csv_write)
##    xiecheng("深圳","长沙","2019-04-29",csv_write)
##    xiecheng("深圳","广州","2019-04-29",csv_write)
##    xiecheng("深圳","合肥","2019-04-29",csv_write)
##    xiecheng("深圳","南京","2019-04-29",csv_write)
##    xiecheng("深圳","青岛","2019-04-29",csv_write)
##    xiecheng("深圳","厦门","2019-04-29",csv_write)
##    xiecheng("深圳","上海","2019-04-29",csv_write)
##    xiecheng("深圳","天津","2019-04-29",csv_write)
##    xiecheng("深圳","武汉","2019-04-29",csv_write)
##    xiecheng("深圳","西安","2019-04-29",csv_write)
##    xiecheng("天津","北京","2019-04-29",csv_write)
##    xiecheng("天津","重庆","2019-04-29",csv_write)
##    xiecheng("天津","成都","2019-04-29",csv_write)
##    xiecheng("天津","长沙","2019-04-29",csv_write)
##    xiecheng("天津","广州","2019-04-29",csv_write)
##    xiecheng("天津","合肥","2019-04-29",csv_write)
##    xiecheng("天津","南京","2019-04-29",csv_write)
##    xiecheng("天津","青岛","2019-04-29",csv_write)
##    xiecheng("天津","厦门","2019-04-29",csv_write)
##    xiecheng("天津","上海","2019-04-29",csv_write)
##    xiecheng("天津","深圳","2019-04-29",csv_write)
##    xiecheng("天津","武汉","2019-04-29",csv_write)
##    xiecheng("天津","西安","2019-04-29",csv_write)
##    xiecheng("武汉","北京","2019-04-29",csv_write)
##    xiecheng("武汉","重庆","2019-04-29",csv_write)
##    xiecheng("武汉","成都","2019-04-29",csv_write)
##    xiecheng("武汉","长沙","2019-04-29",csv_write)
##    xiecheng("武汉","广州","2019-04-29",csv_write)
##    xiecheng("武汉","合肥","2019-04-29",csv_write)
##    xiecheng("武汉","南京","2019-04-29",csv_write)
##    xiecheng("武汉","青岛","2019-04-29",csv_write)
##    xiecheng("武汉","厦门","2019-04-29",csv_write)
##    xiecheng("武汉","上海","2019-04-29",csv_write)
##    xiecheng("武汉","深圳","2019-04-29",csv_write)
##    xiecheng("武汉","天津","2019-04-29",csv_write)
##    xiecheng("武汉","西安","2019-04-29",csv_write)
##    xiecheng("西安","北京","2019-04-29",csv_write)
##    xiecheng("西安","重庆","2019-04-29",csv_write)
##    xiecheng("西安","成都","2019-04-29",csv_write)
##    xiecheng("西安","长沙","2019-04-29",csv_write)
##    xiecheng("西安","广州","2019-04-29",csv_write)
##    xiecheng("西安","合肥","2019-04-29",csv_write)
##    xiecheng("西安","南京","2019-04-29",csv_write)
##    xiecheng("西安","青岛","2019-04-29",csv_write)
##    xiecheng("西安","厦门","2019-04-29",csv_write)
##    xiecheng("西安","上海","2019-04-29",csv_write)
##    xiecheng("西安","深圳","2019-04-29",csv_write)
##    xiecheng("西安","天津","2019-04-29",csv_write)
##    xiecheng("西安","武汉","2019-04-29",csv_write)
    csv_out.close()
##    outputfile.close()
##    sys.stdout = output

