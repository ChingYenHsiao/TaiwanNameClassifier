# 判斷一個unicode是否為中文
#http://www.wangmingkuo.com/python/python%E4%B8%AD%E5%88%A4%E6%96%AD%E5%AD%97%E7%AC%A6%E6%98%AF%E5%90%A6%E6%98%AF%E6%B1%89%E5%AD%97%E3%80%81%E5%AD%97%E6%AF%8D%E4%BB%A5%E5%8F%8A%E6%95%B0%E5%AD%97/
def is_chinese(string): 
    #print (string)
    try:
        for uchar in string:
            if '\u4e00' <= uchar<='\u9fff':
                pass
            else:
                return False
        return True
    except Exception as e:
            print (e)
            print (string)