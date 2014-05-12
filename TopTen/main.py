import os
import pysftp
import sys


if __name__ == "__main__":
    serverid = 0
    IPAddressDict = {}
    hitsDict = {}
#     Collect top ten results from each server
    for line in open('ConfigServers', 'r'):
        line = line.strip() 
        h, usr, pwd, logFilePath = line.split()
        serverid += 1
        print 'Connecting ' + ' ' + h
        try:
            srv = pysftp.Connection(host=h, username=usr, password=pwd)
        except:
            print 'Could Not connect to '+h
            continue
        srv.put('TopTen.py')
        command = 'python TopTen.py ' + logFilePath
        # Execute the script on the server
        srv.execute(command)
        # Download the file from the remote server
        print sys.argv[1] + '/result_' + str(serverid)
        print srv.listdir()
        srv.get('TopTenIPResult', sys.argv[1] + '/result_' + str(serverid))
        srv.execute('rm TopTen.py')
        srv.execute('rm TopTenIPResult')
        # Closes the connection
        srv.close()
    
#     Create a map of results collected from all the servers
    for resultId in range(1, serverid + 1):
        filename = sys.argv[1] + '/result_' + str(resultId)
        for line in open(filename, 'r'):
            line = line.strip() 
            ip, counts, hits = line.split()
            if ip in IPAddressDict:
                IPAddressDict[ip] += counts
                hitsDict[ip] += hits
            else:
                IPAddressDict[ip] = counts
                hitsDict[ip] = hits
        
        try:
            os.remove(filename)
        except OSError:
            pass
    
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
