



def Logit(LogData):
    try:
        f = open("Minions.log", 'a')
    except:
        print "Failed to open logfile!"
        
    f.write(LogData + "\r\n")
    f.close()
    