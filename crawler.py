#!/usr/bin/env python

import requests, re, urlparse, optparse
from termcolor import colored
import pyfiglet 

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="Target url") 
	(options, arguments) = parser.parse_args()
		
	if not options.target:
		parser.error("Target url is required")	
	return options

options = get_arguments()

target_url = options.target
target_links = []

def extract_links_from(url):
	response = requests.get(url)
	return re.findall('(?:href=")(.*?)"', response.content)
	
def crawl(url):
	href_links = extract_links_from(url)
	for link in href_links:
		link = urlparse.urljoin(url, link)

		if "#" in link:
			link = link.split("#")[0]

		if target_url in link and link not in target_links:
			target_links.append(link)
			print(colored(link, "green"))
			crawl(link)

crawl(target_url)