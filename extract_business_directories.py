#Extracts email addresses from specified webpages

import urllib.request
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import csv
import time
from random import randint
import requests


OUTPUT_URL = []
OUTPUT_LINKEDIN = []
INPUT_URL = []
INPUT_FILE = "input_example.csv"
OUTPUT_FILE = "output_example.csv"


headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931'}

#Attach proxy if any, format - "https://"+"202.138.249.12:8080"
#When the value of http_proxy is set to none, no proxy is attached.
http_proxy  = None
proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
            }

#In this example, the inputs are company pages in business directories, outputs are the actual company websites
OUTPUT_URL = []
INPUT_URL = []





#Input file should cnotain a list of urls
def read_targets():
	try:
		with open (INPUT_FILE, 'r', encoding='mac-roman') as csvfile:
			reader = csv.reader(csvfile, delimiter=",")
			for row in reader:
				url = row[5]
				if url!="Company Website":
					INPUT_URL.append(url)
		print ("Target Count - {}".format(len(INPUT_URL)))
	except FileNotFoundError:
		print ("Error, input file not found.")



def write_output():
	with open (OUTPUT_FILE, 'w',newline='') as csvfile:
		fieldnames = ["COMPANY URL", "LINKEDIN URL"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 

		writer.writeheader()
		x = 0
		while x <  len(OUTPUT_LINKEDIN):

				#Write in data from abovementioned lists by index, entry by entry.
				#Each entry is written to a new row
				writer.writerow({
					"INPUT URL": INPUT_URL[x],
					"COMPANY URL": OUTPUT_URL[x],


						})

				x += 1






def find_company_url():

	count = 1
	for url in INPUT_URL:

		count += 1
		

		if count % 100:
			try:
				write_output()
			except:
				pass

		component = urlparse(url)
		base_url = component.scheme + '://' + component.netloc + '/'

		#Use Request library to establish connections and get the page content
		try:
			if http_proxy:
				result = requests.get(url, headers = headers, proxies = proxyDict)
			else:
				result = requests.get(url, headers = headers)

			if result.status_code == 403:
				#Request denied, slow down or use proxy.
				print ("Connected unsuccessful. Error 403")
				write_output()
				return
		except:
			print ("Requests connection failed.")
			write_output()
			return

		con = result.content


		soup = BeautifulSoup(con, 'html.parser')

		#find all links in url
		for a in soup.find_all('a', href=True):

			### DEPENDING ON PAGE LAYOUT, MODIFY ACCORDINGLY ###
			rel = a.get("rel")
			try:
				if rel[0] == "nofollow":
					company_link = (a.get("href"))
					if company_link not in OUTPUT_URL:
						print (company_link)
						OUTPUT_URL.append(company_link)

						break

			except:
				pass

			### END VARIABLE SECTION ###

		time.sleep(randint(10,13))








def main():

	start_time = datetime.now()
	read_targets()
	find_company_url()
	write_output()
	print ("Time Elapsed: " + str(datetime.now() - start_time))

if __name__ == '__main__':
	main()