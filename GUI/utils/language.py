
def is_chinese(uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False
        
def is_number(uchar):
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
        else:
            return False
        
def is_alphabet(uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False
        
def is_other(uchar):
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
            return True
        else:
            return False
