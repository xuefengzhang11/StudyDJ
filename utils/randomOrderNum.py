import time
def getordernumber():
    return str(int(time.time()*1000))+str(int(time.clock()*1000000))

# if __name__ == '__main__':
#     print(getordernumber())