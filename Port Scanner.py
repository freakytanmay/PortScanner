#!/usr/bin/python

import socket,sys,time,datetime,argparse,os
from time import sleep
flag = 0  
os.system('clear') 

if(sys.argv[1]):
	host=sys.argv[1]
else:
	print("Incorrect Input. Enter Host name")
	sys.exit(2)

ip = socket.gethostbyname(host) # Converts the host name into IP address 
 
# check if both starting port and ending port is defined. If not defined,scan over most popular TCP ports. 
if (sys.argv[2]) and (sys.argv[3]) :
	start_port = int(sys.argv[2])
	end_port = int(sys.argv[3])
else:
	# In this case, the script will scan the most common ports.
	flag = 1
 
open_ports = []  # This list is used to hold the open ports
 
common_ports = {
	
 	'20': 'FTP',
	'21': 'FTP',
	'22': 'SSH',
	'23': 'TELNET',
	'25': 'SMTP',
	'53': 'DNS',
	'69': 'TFTP',
	'80': 'HTTP',
	'109': 'POP2',
	'110': 'POP3',
	'123': 'NTP',
	'137': 'NETBIOS-NS',
	'138': 'NETBIOS-DGM',
	'139': 'NETBIOS-SSN',
	'143': 'IMAP',
	'156': 'SQL-SERVER',
	'389': 'LDAP',
	'443': 'HTTPS',
	'546': 'DHCP-CLIENT',
	'547': 'DHCP-SERVER',
	'995': 'POP3-SSL',
	'993': 'IMAP-SSL',
	'2086': 'WHM/CPANEL',
	'2087': 'WHM/CPANEL',
	'2082': 'CPANEL',
	'2083': 'CPANEL',
	'3306': 'MYSQL',
	'8443': 'PLESK',
	'10000': 'VIRTUALMIN/WEBMIN'
}
 
starting_time = time.time() 
#print "+" * 100 
#print "\t Port Scanner..!!!"
#print "+" * 100
 
if (flag): 
	print "User didn't enter ports. Scanning for most common ports on %s" % (host)
else:
	print "Scanning %s from port %s - %s: " % (host, start_port, end_port)
print "Scanning started at %s" %(time.strftime("%H:%M:%S %p"))
  
#  connect to a port and check if it is open or closed
def scan_port(host, port):

	# host : the IP to scan
	# port : the port number to connect
	result = 1
	try:
		# Creating a socket 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Setting socket timeout so that the socket does not wait forever to complete  a connection
		sock.settimeout(1)

		# Connect to the socket ,if the connection was successful, that means the port is open, and the output will be zero
		return_code = sock.connect_ex((host, port))	
		if return_code == 0:
			result = return_code 
		# close the socket
		sock.close() 

	except Exception, e:
		pass
 
	return result 
 

def get_service(port):
	port = str(port) 
	if port in common_ports: 
		return common_ports[port] 
	else:
		return 0

# start from here 

try:
	print "Scanning"
	
    #sleep(0.2)
	print " \n Connecting to Port: ",
 
	if flag: # The flag is set, means the user did not give any port range
		for p in sorted(common_ports):  
			#sys.stdout.flush() 
			p = int(p)
			print p,	
			# connect to the port
			response = scan_port(host, p) 
			if response == 0: # The port is open
				open_ports.append(p) 
			#if not p == end_port:
			#sys.stdout.write('\b' * len(str(p))) # to clear the port number displayed
	else:
		
		# scan through the range 
		for p in range(start_port, end_port+1):
		    #sys.stdout.flush()
			print p,
			response = scan_port(host, p) 
			if response == 0: # Port is open
				open_ports.append(p) 
			if not p == end_port:
				sys.stdout.write('\b' * len(str(p)))
 
	print "\nScanning completed at %s" %(time.strftime("%I:%M:%S %p"))
	stop_time = time.time()
	total_time = stop_time - starting_time # 
	print "%" * 100
	print "\tScan Report: %s" %(host)
	print "%" * 100

	total_time = total_time / 60
	print "Scan Took %s Minutes" %(total_time)
		
	print("No of open ports: %d" %(len(open_ports)))
	if open_ports: 
		print "Open Ports: "
		for i in sorted(open_ports):
			service = get_service(i)
			if not service: 
				service = "Unknown service"
			print "\t%s %s: Open" % (i, service)
	else:
		
		print "No open ports found"
 
except KeyboardInterrupt: 
	print "User Interruption. Exiting "		
	sys.exit(1)
