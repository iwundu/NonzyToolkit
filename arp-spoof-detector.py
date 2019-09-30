#!/usr/bin/env python

import scapy.all as scapy
import optparse
import pyfiglet 
from termcolor import colored

#banner-text
banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print(" Written By Iwundu Chinonso")
print colored("=" * 60, "green")

#function to parse on terminal.....
def get_arguments():
	parser = optparse.OptionParser("Usage: arp-spoof-detector.py -i <interface>")
	parser.add_option("-i", "--interface", dest="interface", help="interface") 
	(options, arguments) = parser.parse_args()
		
	if not options.interface:
		parser.error("An Interface is reqiured")	
	
	return options

#function to get MAC Address...
def get_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	response = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	return response[0][1].hwsrc


def sniffer(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets)

def process_sniffed_packets(packet):
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
		try:
			real_mac = get_mac(packet[scapy.ARP].psrc)
			response_mac = packet[scapy.ARP].hwsrc

			if real_mac != response_mac:
				print colored("ARP Spoofing detected!", "yellow")
		except IndexError:
			pass

options = get_arguments()
sniffer(options.interface)