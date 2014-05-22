TopTenIP
========

Get top ten source IP addresses and their corresponding hit rates

<p>A script which determines the top 10 most common source IP addresses, and their hit rates, for a fleet of 1000 web servers within the last hour.</p>
<p> Following are the assumptions:</p>
 - Web servers are locally writing access logs in the Apache Combined Log Format (http://httpd.apache.org/docs/current/logs.html#combined).
 - Web servers are accessible by ssh.
 - Scripts are to be run on a base Red Hat or CentOs equivalent Linux Server.
 - Using Python 2.7
 - Control server has pysftp package installed for ssh
 - ConfigServers file has a list of all the servers in the format: ServerAddress username password access.log_location
 - All the servers have apache-log-parser package installed for parsing Apache Combined Log Format
 - If any log entry is not in the given format, then it is ignored
 - Command to execute the script: python main.py <Path_To_Data_Folder>
