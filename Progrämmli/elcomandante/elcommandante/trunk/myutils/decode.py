"""
    decode function, takes an string which contains the scpi/timestamp encoded data
    and returns a list of  time scpi-command type message, and the data-string
    example: 
    data = '127272 :PROG:START 5"
    returns
        time = 127272
        coms = [PROG,START]
        message = 5
        typ = c
        command = :PROG:START 5
        
    if a value is not present, it is filled with 'unknown' or in case of time with -1
"""
def decode(data):
    #type: (q)uestion, (a)nswer or (c)ommand
    dataArray=data.split(' ')
#    print dataArray
    if len(dataArray)==0 or (len(dataArray)==1 and dataArray[0]==''):
        time = -1
        coms =[]
        dataArray =''
        typ = 'c'
        msg = ''
        command = ''
    elif len(dataArray)>0:
        if is_number(dataArray[0]):
            time = dataArray[0] 
            if len(data.split(' ',1))>1:
                command = data.split(' ',1)[1]
            else:
                command = data
                print data
            dataArray=dataArray[1:]
        else:
            time = -1
            command = data
        if len(dataArray)==2:
            coms, msg = dataArray
        elif len(dataArray)==1 and dataArray[0].find(':')==0:
            coms = dataArray[0]
            msg = 'unknown'
        else:
            coms = 'unknown'
            msg = dataArray
        if len(coms)>0:
            if coms[0] != ':':
                coms=':unknown'
                typ='u'
        if coms.find('?') != -1:
            typ='q'
            coms=coms.replace('?','')
        elif coms.find('!') != -1:
            typ='a'
            coms=coms.replace('!','')
        else:
            typ='c'
        coms=coms.upper()
    if len(coms)>0:
        coms=coms[1:].split(':')#don't take the first :
    return time, coms, typ, msg, command

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
