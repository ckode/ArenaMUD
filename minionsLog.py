



def Logit(LogData):
    try:
        f = open("Minions.log", 'a')
    except:
        print "Failed to open logfile!"
        
    f.write(LogData + "\n")
    f.close()
