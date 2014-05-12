import apache_log_parser
from datetime import datetime
import dateutil.tz
import sys


# Convert Apache time format to datatime object
def my_apachetime(s):
    month_map = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
        'Aug':8, 'Sep': 9, 'Oct':10, 'Nov': 11, 'Dec': 12}
    s = s[1:-1]
    hour = (int(s[21:-2])) * 60 * 60
    minutes = int(s[-2:]) * 60

    if hour < 0:
        minutes *= -1

    tzinfo = dateutil.tz.tzoffset(None, (hour + minutes))
    return datetime(int(s[7:11]), month_map[s[3:6]], int(s[0:2]), \
         int(s[12:14]), int(s[15:17]), int(s[18:20]), 0, tzinfo) 

if __name__ == "__main__":
    parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")
    IPAddressDict = {}
    HitDict = {}
    for line in  open(sys.argv[1], 'r'):
        try:
            log_data = parser(line.strip())
            timeRec = log_data['time_recieved']
            time_delta = (datetime.now(dateutil.tz.tzlocal()) - my_apachetime(timeRec))
            if time_delta.days == 0 and time_delta.seconds < 3601:
                ip = log_data['remote_host']
                if ip in IPAddressDict:
                    IPAddressDict[ip] += 1
                else:
                    IPAddressDict[ip] = 1
                if int(log_data['status']) == 200:
                    if ip in HitDict:
                        HitDict[ip] += 1
                    else:
                        HitDict[ip] = 1
        except Exception: 
            pass
    
    count = 0
    resultsFile = open('TopTenIPResult', 'w+')
    print ('ipAddress' + '\t' + 'count' + '\t' + 'hits' + '\t' + 'hitRate')
    for ip in sorted(IPAddressDict, key=IPAddressDict.get, reverse=True):
        if ip in HitDict:
            resultsFile.write(ip + ' ' + str(IPAddressDict[ip]) + ' ' + str(HitDict[ip]) + '\n')
            print (ip + '\t' + str(IPAddressDict[ip]) + '\t' + str(HitDict[ip])) + '\t' + str(float(HitDict[ip]) / float(IPAddressDict[ip]))
        else:
            resultsFile.write(ip + ' ' + str(IPAddressDict[ip]) + ' 0\n')
            print ip + '\t' + str(IPAddressDict[ip]) + '\t' + str(0) + '\t' + str(0)
        count += 1
        if(count == 10):
            break
