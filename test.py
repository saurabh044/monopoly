from MenuBox import MenuBox
from MenuBox2 import MenuBox2


def isPalindrome(s):
    if len(s) == 1:
        return False
    if len(s) == 2:
        if s[0] == s[1]:
            return True
        else:
            return False
    if len(s) == 3:
        if s[0] == s[2]:
            return True
        else:
            return False
    if len(s) % 2 == 0:
        for i in range(len(s) / 2):
            if s[i] != s[len(s)-i-1]:
                return False
        return True
    else:
        for i in range((len(s) - 1) / 2):
            if s[i] != s[len(s)-i-1]:
                return False
        return True

def playwithwords(s):
    out = {}
    for k in range(len(s)):
        for i in range(len(s)-k):
            test_string = s[k:(i+k+1)]
            #print "%s" % test_string
            if isPalindrome(test_string):
                print "%s-%d-%d" % (test_string, k, i+k)
                if len(out) > 0:
                    if k < out[maxlenkey(out)][1]:
                        if len(test_string) > len(maxlenkey(out)):
                            out[test_string] = (k, i + k)
                    else:
                        out[test_string] = (k, i + k)
                else:
                    out[test_string] = (k, i + k)

    print max2lenkeys(out)
    return len(max2lenkeys(out)[0]) * len(max2lenkeys(out)[1])

def maxlenkey(x):
    l = 0
    key = 0
    if len(x) > 0:
        for i in x.keys():
            if l < len(i):
                l = len(i)
                key = i
        return key
    else:
        return ""

def max2lenkeys(x):
    if len(x) == 0:
        return ("", "")
    elif len(x) == 1:
        return (x.keys()[0])
    elif len(x) == 2:
        return x.keys()[0], x.keys()[1]
    else:
        fe = maxlenkey(x)
        se = ""
        for i in x:
            if i != fe:
                if len(se) < len(i):
                    se = i
        return fe, se

s = "dbcbcbededadecbcdecbaeadcecada"
b = "012345678901234567890123456789"
for k in range(len(s)):
    for i in range(len(s)-k):
        test_string = s[k:(i+1+k)]
        #print "%s" % test_string
result = playwithwords(s)
print "Result = %d" % result



