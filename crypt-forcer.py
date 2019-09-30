#!/usr/bin/env python
import optparse
import crypt
from termcolor import colored
import pyfiglet

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-p", "--password_list", dest="password_list", help="password list")
	parser.add_option("-w", "--wordlist", dest="wordlist", help="wordlist") 
	(options, arguments) = parser.parse_args()
		
	if not options.wordlist:
		parser.error("A wordlist is required")	
	if not options.password_list:
		parser.error("A password list is required")	
	return options

options = get_arguments()

def crack_pass(crypt_word):
	salt = crypt_word[0:2]
	dictionary = open(options.wordlist, "r")
	for word in dictionary.readlines():
		word = word.strip('\n')
		crack_pass = crypt.crypt(word, salt)
		if (crypt_word == crack_pass):
			print colored("[+] Found Password: " + word, "green")
			return

def main():
	pass_file = open(options.password_list, "r")
	for line in pass_file.readlines():
		if ":" in line:
			user = line.split(":")[0]
			crypt_word = line.split(":")[1].strip(" ").strip("\n")
			print colored("[*] Cracking Password For: " + user, "yellow")
			crack_pass(crypt_word)

	print colored("[-] Password Not Found", "red")

main()