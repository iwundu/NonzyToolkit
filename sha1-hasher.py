#!/usr/bin/env python
from termcolor import colored
import hashlib, optparse, pyfiglet

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-s", "--sha1", dest="sha1", help="sha1 hash")
	parser.add_option("-p", "--password", dest="password", help="passwordlist") 
	(options, arguments) = parser.parse_args()
		
	if not options.sha1:
		parser.error("sha1 hash is required")	
	if not options.password:
		parser.error("passwordlist is required")	
	return options

options = get_arguments()
sha1_hash = options.sha1
pass_list = options.password

for password in pass_list.split('\n'):
	hash_guess = hashlib.sha1(bytes(password)).hexdigest()
	if hash_guess == sha1_hash:
		print(colored("[+] The Password is " + str(password), 'green'))
		quit()
	else:
		print(colored("[+] Password guess " + str(password) + " does not match, trying next....", 'red'))

print("Password not in passwordlist")