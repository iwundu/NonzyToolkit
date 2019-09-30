#!/usr/bin/env python

import requests
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
	parser.add_option("-u", "--url", dest="url", help="url") 
	(options, arguments) = parser.parse_args()
		
	if not options.url:
		parser.error("A url is reqiured")	
	
	return options
def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

options = get_arguments()

download(options.url)
print colored("[+]File Downloaded Successfully!", "green")
