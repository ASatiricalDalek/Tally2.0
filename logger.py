from datetime import datetime

def writeTallyLog(logEntry):
    today = datetime.now()
    log = open('/var/log/tally2/debug.log', 'a+')
    log.write(str(today) + '  -  ')
    log.write(logEntry + '\n')
    log.write('\n')
    log.close()
    