#!/usr/bin/env python

from termcolor import colored
import hashlib, optparse,pyfiglet

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-w", "--wordlist", dest="wordlist", help="wordlist")
	parser.add_option("-m", "--md5_hash", dest="md5_hash", help="Md5 Hash") 
	(options, arguments) = parser.parse_args()
		
	if not options.wordlist:
		parser.error("wordlist is required")	
	if not options.md5_hash:
		parser.error("Md5 Hash is required")	
	return options

options = get_arguments()

def try_open(wordlist):
	global pass_file
	try:
		pass_file = open(wordlist, "r")
	except:
		print("[-] No Such File At That Path!")
		quit()

pass_hash = options.md5_hash
wordlist = options.wordlist
try_open(wordlist)

for word in pass_file:
 	print(colored("[-] Trying: " + word.strip("\n"), 'yellow'))
 	enc_wrd = word.encode('utf-8')
 	md5digest = hashlib.md5(enc_wrd.strip()).hexdigest()

 	if md5digest == pass_hash:
 		print(colored("[+] Password Found: " + word, 'green'))
 		exit(0)

print("[-] Password Not In List!")