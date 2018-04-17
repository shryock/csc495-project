logFile = open('log.txt', 'a', encoding='utf-8')

def log(*string, printLog=True):
    if printLog:
        [print(a, end='') for a in string]
        print()
    [logFile.write(str(a)) for a in string]
    logFile.write('\n')

def close():
    logFile.close()
