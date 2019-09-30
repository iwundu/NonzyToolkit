#!usr/bin/env python
import requests
import optparse
import pyfiglet 
from termcolor import colored

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-w", "--wordlist", dest="wordlist", help="wordlist")
	parser.add_option("-u", "--url", dest="url", help="url")
	
	(options, arguments) = parser.parse_args()
		
	if not options.wordlist:
		parser.error("A wordlist is required")	
	if not options.url:
		parser.error("A url is required")	
	return options

def request(url):
	try:
		return requests.get(url)
	except requests.exceptions.ConnectionError:
		pass

options = get_arguments()
target_url = options.url
wordlist_location = options.wordlist

with open(wordlist_location, "r") as wordlist_file:
	for line in wordlist_file:
		word = line.strip()
		sub_domain = word + "." + target_url
		response = request(sub_domain)
		if  response:
			print colored("[+] Discovered sub-domain ==> " + sub_domain, "green")

	print colored("[-] No match in wordlist", "red")