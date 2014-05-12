import pysftp
import sys


serverid = 0
IPAddressDict = {}
hitsDict = {}
for line in open('ConfigServers', 'r'):
    line = line.strip() 
    h, usr, pwd, logFilePath = line.split()
    serverid += 1
    print 'Connecting ' + ' ' + h
    srv = pysftp.Connection(host=h, username=usr, password=pwd)
    srv.put('__init__.py')
    command = 'python __init__.py ' + logFilePath
    # Execute the script on the server
    srv.execute(command)
    # Download the file from the remote server
    srv.get('TopTenIPResult', sys.argv[1] + '/result_' + str(serverid))
    # Closes the connection
    srv.close()

for resultId in range(1, serverid + 1):
    for line in open(sys.argv[1] + '/result_' + str(resultId), 'r'):
        line = line.strip() 
        ip, counts, hits = line.split()
        if ip in IPAddressDict:
            IPAddressDict[ip] += counts
            hitsDict[ip] += hits
        else:
            IPAddressDict[ip] = counts
            hitsDict[ip] = hits

# Output the final result to console
count = 0
print ('ipAddress' + '\t' + 'count' + '\t' + 'hits' + '\t' + 'hitRate')
for ip in sorted(IPAddressDict, key=IPAddressDict.get, reverse=True):
    if ip in hitsDict:
        print (ip + '\t' + str(IPAddressDict[ip]) + '\t' + str(hitsDict[ip])) + '\t' + str(float(hitsDict[ip]) / float(IPAddressDict[ip]))
    else:
        print ip + '\t' + str(IPAddressDict[ip]) + '\t' + str(0) + '\t' + str(0)
    count += 1
    if(count == 10):
        break
