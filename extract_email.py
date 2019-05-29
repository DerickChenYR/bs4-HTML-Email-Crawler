import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import csv
import time
from random import randint


TARGET_URL= 'www.example.com/page_with_email_addresses'
start_time = datetime.now()


#Initialise script, find relative links from target pages
def init():

	
	url_process_queue = set()

	url_process_queue.add(TARGET_URL)

	#breaking down TARGET_URL
	component = urlparse(TARGET_URL)

	base_url= component.scheme + '://' + component.netloc

	page = urllib.request.urlopen(TARGET_URL).read()

	#find all urls/links on that page
	#URL: scheme://netloc/path;parameters?query#fragment
	for a in BeautifulSoup(page, 'html.parser').find_all('a', href=True):

		if a['href'].startswith(base_url) == True:
			url_process_queue.add(a['href'])
		elif a['href'].startswith('/') == True:
			full_url= urljoin(base_url, a['href'])
			url_process_queue.add(full_url)
		
	print ("\nA total of %i links found...\n" %len(url_process_queue))

	process_url_queue(url_process_queue)




#crawl for emails in associated links too
def process_url_queue(url_process_queue):

	emails_found = set()

	for i in url_process_queue:

		#Display current page
		print ("Scraping: %s" % i)
		try:
			page2 = urllib.request.urlopen(i).read()

		except Exception:
			print (Exception)
			continue	
		
		#Use re to find all email addresses
		found_email = re.findall(r'[\w\.,]+@[\w\.,]+\.\w+', str(page2))
		if found_email != "":
			emails_found.update(found_email)

		time.sleep(randint(10,13))

	write_output(emails_found)



#convert list to CSV writable format
def write_output(emails_found):

	n = 0

	out = [[ ] for x in range(len(emails_found))]
	email_list = list(emails_found)

	while n < len(email_list):

		out[n].append(email_list[n])
		n += 1

	with open ("output_emails.csv", "a", newline="") as result_file:
		wr = csv.writer(result_file, dialect = "excel" )
		for i in out:
			wr.writerows([i])

	print ("Scraping Completed for {}".format(TARGET_URL))
	print ("Time Elapsed: " + str(datetime.now() - start_time))





if __name__ == '__main__':
	init()





#not crawling imbed elements e.g. forms