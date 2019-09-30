#!usr/bin/env python
import requests
import re
import urlparse
from BeautifulSoup import BeautifulSoup
import pyfiglet 
from termcolor import colored

banner = pyfiglet.figlet_format("NonzyToolkit")
print colored("=" * 60, "green")
print colored(banner, "yellow")
print colored("=" * 60, "green")

class Scanner:
	def __init__(self, url, ignore_links):
		self.session = requests.Session()
		self.target_url = url
		self.target_links = []
		self.link_to_ignore = ignore_links
	
	def extract_link_from(self, url):
		response = self.session.get(url)
		return re.findall('(?:href=")(.*?)"', response.content)

	def crawler(self, url=None):
		if None:
			url = self.target_url
		
		href_link = self.extract_link_from(url)
		for link in href_link:
			link = urlparse.urljoin(url, link)
			if "#" in link:
				link = link.split("#")[0]
			if self.target_url in link and link not in self.target_links and link not in self.link_to_ignore:
				self.target_links.append(link)
				print colored(link, "green")
				try:
					self.crawler(link)
				except TypeError:
					pass
				print colored("=" * 80, "yellow")

	def extract_form(self, url):
		response = self.session.get(url)
		parsed_html = BeautifulSoup(response.content)
		return parsed_html.findAll("form")

	def submit_form(self, form, value, url):
		action = form.get("action")
		post_url = urlparse.urljoin(target_url, action)
		method = form.get("method")
		post_data = {}
		input_list = form.findAll("input")
		for input in input_list:
			input_name = input.get("name")
			input_type = input.get("type")
			input_value = input.get("value")
			if input_type == "text":
				input_value = value
			post_data[input_name] = input_value
			if method == "post":
				return self.session.post(post_url, data=post_data)
			else:
				return self.session.get(post_url, params=post_data)
	
	def run_scanner(self):
		for link in self.target_link:
			forms = self.extract_form(link)
			for form in forms:
				print colored("[+] Testing all forms in " + link, "green")
			if "=" in link:
				print colored("[+] Testing " + link, "yellow")

	def test_xss_in_form(self, form, url):
		xss_test_script = "<script>alert('xss')</script>"
		response = self.submit_form(form, xss_test_script, url)
		if xss_test_script in response:
			print colored("[+] Input form is vulnerable to XSS attacks", "green")
		else:
			print colored("[+] Input form is not vulnerable to XSS attacks", "yellow")

	def test_xss_in_link(self, url):
		xss_test_script = "<script>alert('xss');</script>"
		url = url.replace("=", "=" + xss_test_script)
		response = self.session.get(url)
		if xss_test_script in response.content:
			print colored("[+] Target URL is vulnerable to XSS attacks", "green")
		else:
			print colored("[+] Target URL is not vulnerable to XSS attacks", "yellow")