

log_file = open('log.txt', 'a', encoding='utf-8')

def log(*string):
    [print(a, end='') for a in string]
    print()
    [log_file.write(str(a)) for a in string]
    log_file.write('\n')

def close():
    log_file.close()

