from random import shuffle
def makecode(index):
    #Check that code is in range 0 - 99
    return "%04d" % (index*100 + (index+66)%100)

def validate(code):
    if len(code) != 4:
        return -1
    try:
        a = int(float(code[:2]))
        b = int(float(code[2:]))
        if (a+66)%100 == b:
            return a
        else:
            return -1
    except:
        return -1


codes = range(100)
shuffle(codes)
for c in codes:
    c = "=\""+makecode(c)+"\""
    print c

#fake = "1298"
#print fake, validate(fake)