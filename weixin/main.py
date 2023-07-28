# import werobot
# import ccc
import garbageClassification
import re
import json

import werobot
import caipiao

robot = werobot.WeRoBot(token='tokenhere')


def en_passwd(passwd, key):
    while True:
        if len(key) >= len(passwd):
            break
        key = key+key
    result = []
    for x, y in zip(passwd, key):
        result.append((ord(x) ^ ord(y)))
    return(result)


def de_passwd(passwd, key):
    while True:
        if len(key) >= len(passwd):
            break
        key = key+key
    result = ''
    for x, y in zip(passwd, key):
        result += chr(ord(y) ^ x)
    return(result)


@robot.handler
def hello(message):
    if re.match('^垃圾', message.content):
        result = garbageClassification.garbageClassification(re.sub('^垃圾', '', message.content, count=1))
        # print (result)
        return result
    if re.match('双色球', message.content) or re.match('超级大乐透', message.content):
        result = cccc.main(message.content)
        if len(result) == 1:
            return result[0]+': 未中奖'
        else:
            return ','.join(result)
    if re.match('^加密', message.content):
        text = re.sub('^加密', '', message.content).split('+')
        result = en_passwd(text[0], text[1])
        return str(result)


    if re.match('^解密', message.content):
        text = re.sub('^解密', '', message.content).split('+')
        result = de_passwd(json.loads(text[0]), text[1])
        return result




# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 8080
robot.run()



# a = '垃圾笔'
# if re.match('^垃圾', a):
#     print(re.sub('^垃圾','',a,count=1))


# robot = werobot.WeRoBot(token='tokenhere')


# @robot.handler
#def hello(message):
 #   if re.match('^垃圾', message.content):
  #      return garbageClassification(re.sub('^垃圾', '', message.content, count=1))
# print(hello('垃圾西瓜'))

    #    return message.content
    # result = ccc.main(message.content)
    # if len(result) == 1:
    #     return '未中奖'
    # else:
    #     return ','.join(result)


#     # 让服务器监听在 0.0.0.0:80
# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 80
# robot.run()
