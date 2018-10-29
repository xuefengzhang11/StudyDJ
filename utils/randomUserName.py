from random import randint


# 获取0-9随机数
def rNum():
    return str(randint(0, 9))


# 获取a-z,A-Z随机字符
def rChar():
    if rNum() <= '4':
        # [a,z]
        char = chr(randint(97, 122))
    else:
        # [A,Z]
        char = chr(randint(65, 90))
    return char


# 生成随机用户名 study_......
def getRandomName():
    res = 'study_'
    for i in range(3):
        res += rNum() + rChar()
    return res
