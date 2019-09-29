def is_number(string):
    try:
        for uchar in string:
            if '\u0030' <= uchar<='\u0039':
                pass
            else:
                return False
        return True
    except Exception as e:
            print (e)
            print (string)