import requests
import json
import sys
import codecs
import datetime

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


host = 'https://www.mxnzp.com/api/lottery/common/latest?app_id=0srsejntjyvcphtw&app_secret=RXdGcm4velRyYnVsMStqcFpZYmx2QT09'
ssq_b = [['02', '03', '07', '18', '27', '30'], ['06', '12', '16', '17', '19', '21'], ['06', '10', '16',
         '21', '28', '29'], ['01', '12', '13', '19', '20', '28'], ['03', '07', '11', '18', '26', '28']]
ssq_a = ['09', '11', '08', '04', '05']
cjdlt_b = [['02', '03', '10', '11', '18'], ['08', '09', '26', '29', '35'], ['13', '16', '20',
           '26', '27'], ['01', '03', '07', '13', '19'], ['02', '11', '13', '15', '31']]
cjdlt_a = [['03', '06'], ['05', '11'], [
    '02', '07'], ['04', '10'], ['01', '03']]
ssq_ok = {'0+1': '六等奖：5元', '1+1': '六等奖：5元', '2+1': '六等奖：5元', '3+1': '五等奖：10元', '4+0': '五等奖：10元',
          '4+1': '四等奖：200元', '5+0': '四等奖：200元', '5+1': '三等奖：3000元', '5+0': '二等奖：浮动', '6+1': '一等奖：浮动'}
cjdlt_ok = {'0+2': '九等奖：5元', '2+1': '九等奖：5元', '3+0': '九等奖：5元', '1+2': '九等奖：5元', '3+1': '八等奖：15元', '2+2': '八等奖：15元',
            '4+0': '七等奖：100元', '3+2': '六等奖：200元', '4+1': '五等奖：300元', '4+2': '四等奖：3000', '5+0': '三等奖：10000', '5+1': '二等奖：浮动', '5+2': '一等奖：浮动'}


def get_cp(code):
    if code == '双色球':
        params = (
            ('appkey', 'de80fc06804a4350'),
            ('caipiaoid', '11'),  # 14
            ('issueno', ''),
        )
        response = json.loads(requests.get(
            'https://api.jisuapi.com/caipiao/query', params=params).text)['result']

        return (('双色球', response['issueno'], response['number'].split(' '), response['refernumber'].split(' '), response['opendate']))
    if code == '超级大乐透':
        params = (
            ('appkey', 'de80fc06804a4350'),
            ('caipiaoid', '14'),  # 14
            ('issueno', ''),
        )
        response = json.loads(requests.get(
            'https://api.jisuapi.com/caipiao/query', params=params).text)['result']

        return (('超级大乐透', response['issueno'], response['number'].split(' '), response['refernumber'].split(' '), response['opendate']))


def main(code):
    r_list = get_cp(code)
    result = []
    week_list = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    week_num = datetime.datetime.strptime(
        r_list[4], '%Y-%m-%d').weekday()
    if r_list:
        cc = [week_list[week_num]]
        if r_list[0] == '超级大乐透':
            for x in range(5):
                a = 0
                b = 0
                for y in cjdlt_b[x]:
                    if y in r_list[2]:
                        a += 1
                for z in cjdlt_a[x]:
                    if z in r_list[3]:
                        b += 1
                result.append(('{}+{}').format(a, b))
            for x in result:
                y = cjdlt_ok.get(x)
                if y is not None:
                    cc.append(y)

        if r_list[0] == '双色球':
            for x in range(5):
                a = 0
                b = 0
                for y in ssq_b[x]:
                    if y in r_list[2]:
                        a += 1
                if ssq_a[x] in r_list[3]:
                    b += 1
                result.append(('{}+{}').format(a, b))
            for x in result:
                y = ssq_ok.get(x)
                if y is not None:
                    cc.append(y)
        return cc

