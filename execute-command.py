#!/usr/bin/env python

import subprocess
import optparse
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

#parse arguments
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--command", dest="command", help="command")
	(options, arguments) = parser.parse_args()
		
	if not options.command:
		parser.error("An command is required")	
	
	return options

options = get_arguments()

command = options.command
subprocess.Popen(command, shell=True)

#"%SystemRoot%\System32\msg.exe * You have been Hacked"