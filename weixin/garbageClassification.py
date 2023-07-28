import requests
import json
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


host_api = 'https://www.mxnzp.com/api/rubbish/type?app_id=0srsejntjyvcphtw&app_secret=RXdGcm4velRyYnVsMStqcFpZYmx2QT09'


def garbageClassification(rubbish):
    try:
        queryResults = json.loads(requests.get(
            host_api, params={'name': rubbish}).text)['data']
        returnsResult = ''
        if queryResults['recommendList']:
            for garbageVariety in queryResults['recommendList']:
                returnsResult = returnsResult + '\n' + garbageVariety['goodsName'] + '：' + garbageVariety['goodsType']
        if queryResults['aim']:
            return (queryResults['aim']['goodsName'] + '：' + queryResults['aim']['goodsType'] + returnsResult)
        else:
            return (returnsResult)
    except:
        return ('未查到该垃圾')

#print(garbageClassification('电池'))
#print(requests.get(host_api, params={'name': '香油'}).text)