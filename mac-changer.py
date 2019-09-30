#!/usr/bin/env python

import subprocess
import optparse
import re
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

#parse arguments
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="interface")
	parser.add_option("-m", "--mac", dest="mac", help="Spoof MAC Address") 
	(options, arguments) = parser.parse_args()
		
	if not options.interface:
		parser.error("An Interface is required")	
	if not options.mac:
		parser.error("A MAC Address is required")	
	return options

#change mac	
def change_mac(interface, mac):
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", mac])
	subprocess.call(["ifconfig", interface, "up"])

#get current mac
def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])

	search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	if search_result:
		return search_result.group(0)
	else:
		print colored("[-]could not read MAC Address", "yellow")

options = get_arguments()
change_mac(options.interface, options.mac)
current_mac = get_current_mac(options.interface)

if not current_mac == options.mac:
	print colored("MAC Address changed successfully", "green")
	print("New MAC Address: " + str(current_mac))
else:
	print colored("MAC Address  failed  to change", "yellow")