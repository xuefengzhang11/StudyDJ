#!/usr/bin/python
# -*-coding:utf-8-*-
import http.client  # Python 2.x  httplib ->  Python 3.x http.client
import urllib.parse, hashlib, datetime, time, json, ssl, random


# ssl 认证
# ssl._create_default_https_context = ssl._

# 生成六位验证码
def createValidate():
    res = ''
    for i in range(6):
        res += str(random.randint(0, 9))
    return res


# 发送短信
def sendIndustrySms(to, expire):
    # 验证码
    validate = createValidate()
    # 短信模板
    smsContent = '【思达迪】您的验证码为{0}，请于{1}分钟内正确输入，' \
                 '如非本人操作，请忽略此短信。'.format(validate, expire)

    # 定义账号和密码，开户之后可以从用户中心得到这两个值
    accountSid = '5d17119caba84772a3e5ec3332493f8b'
    acctKey = 'ebf6b434bc18449ab197b8fc00e20574'

    # 定义地址，端口等
    serverHost = "api.miaodiyun.com"
    serverPort = 443
    industryUrl = "/20150822/industrySMS/sendSMS"

    # 格式化时间戳，并计算签名
    timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    rawsig = accountSid + acctKey + timeStamp
    m = hashlib.md5()
    m.update(str(rawsig).encode('utf-8'))
    sig = m.hexdigest()

    # 定义需要进行发送的数据表单
    params = urllib.parse.urlencode({'accountSid': accountSid, 'smsContent': smsContent,
                                     'to': to, 'timestamp': timeStamp, 'sig': sig})
    # 定义header
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    # 与构建https连接
    conn = http.client.HTTPSConnection(serverHost, serverPort)
    # Post数据
    conn.request(method="POST", url=industryUrl, body=params, headers=headers)
    # 返回处理后的数据
    response = conn.getresponse()
    # 读取返回数据
    jsondata = response.read().decode('utf-8')

    # 打印完整的返回数据
    print(jsondata)
    # 解析json，获取特定的几个字段
    jsonObj = json.loads(jsondata)
    respCode = jsonObj['respCode']
    # 00000 为发送成功
    print("错误码:", respCode)
    respDesc = jsonObj['respDesc']
    print("错误描述:", respDesc)
    # 关闭连接
    conn.close()
    return {"respCode": respCode, "respDesc": respDesc, "validate": validate}


if __name__ == '__main__':
    sendIndustrySms('14796686075')

# 测试
# 18036387467  ls
# 13812790420  James
# 15779789559 sx
# to可以是一个或者多个号码，若是多个号码，以英文逗号分开
# to = '14796686075'
# 短信内容 smsContent
# sendIndustrySms(to,smsContent)
