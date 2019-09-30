#!/usr/bin/env python

import scapy.all as scapy
import optparse
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

#function to parse on terminal.....
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="Target IP range") 
	(options, arguments) = parser.parse_args()
		
	if not options.target:
		parser.error("An IP Address is reqiured")	
	
	return options

#scanner
def scanner(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	response = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	
	print("IP\t\t\tMAC Address\n...........................................")
	clients_list = []
	for element in response:
		client_dict = {"ip": element[1].psrc + element[1].hwsrc}
		clients_list.append(client_dict)		
		print(element[1].psrc + "\t\t" + element[1].hwsrc + "\n")
	#print (clients_list)
options = get_arguments()
scanner(options.target)