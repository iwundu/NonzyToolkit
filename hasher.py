#!/usr/bin/env python

import hashlib
import pyfiglet
import optparse
from termcolor import colored

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-f", "--file", dest="file", help="Hash File") 
	(options, arguments) = parser.parse_args()
		
	if not options.file:
		parser.error("Hash File is required")	
	return options

options = get_arguments()
hashvalue = options.file

hash_obj1 = hashlib.md5()
hash_obj1.update(hashvalue.encode())
print colored("MD5 Hash: " + hash_obj1.hexdigest(), "yellow")

hash_obj2 = hashlib.sha1()
hash_obj2.update(hashvalue.encode())
print colored("SHA1 Hash: " + hash_obj2.hexdigest(), "yellow")

hash_obj3 = hashlib.sha224()
hash_obj3.update(hashvalue.encode())
print colored("SHA224 Hash: " + hash_obj3.hexdigest(), "yellow")

hash_obj4 = hashlib.sha256()
hash_obj4.update(hashvalue.encode())
print colored("SHA256 Hash: " + hash_obj4.hexdigest(), "yellow")

hash_obj5 = hashlib.sha512()
hash_obj5.update(hashvalue.encode())
print colored("SHA512 Hash: " + hash_obj5.hexdigest(), "yellow")