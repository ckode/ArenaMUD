



def Logit(LogData):
    try:
        f = open("ArenaMUD.log", 'a')
    except:
        print "Failed to open logfile!"

    f.write(LogData + "\n")
    f.close()
