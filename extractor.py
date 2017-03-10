import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import csv

start_time = datetime.now()

urls_queue = set()
email_set= set()
n = 0

url = '			'
urls_queue.add(url)

#breaking down url 
component = urlparse(url)

print (component)

base_url = component.scheme + '://' + component.netloc

page = urllib.request.urlopen(url).read()

#find all urls on that page
#URL: scheme://netloc/path;parameters?query#fragment
for a in BeautifulSoup(page, 'html.parser').find_all('a', href=True):

	if a['href'].startswith(base_url) == True:
		urls_queue.add(a['href'])
	elif a['href'].startswith('/') == True:
		full_url = urljoin(base_url, a['href'])
		urls_queue.add(full_url)
	
print ("\nA total of %i links found..." %len(urls_queue))
print (urls_queue)
print ("")


#crawl for emails

for i in urls_queue:

	print ("Crawling: %s" % i)
	try:
		page2 = urllib.request.urlopen(i).read()

	except Exception:
		print (Exception)
		continue	
	
	found_email = re.findall(r'[\w\.,]+@[\w\.,]+\.\w+', str(page2))
	if found_email != "":
		email_set.update(found_email)

#convert list to CSV writable format

out = [[ ] for x in range(len(email_set))]
email_list = list(email_set)

while n < len(email_list):

	out[n].append(email_list[n])
	n += 1

with open ("emails.csv", "a", newline="") as result_file:
	wr = csv.writer(result_file, dialect = "excel" )
	for i in out:
		wr.writerows([i])

print ("")
print (email_list)
print (datetime.now() - start_time)










#not crawling imbed elements e.g. forms

#success - http://www.treetops.com.sg/contact-us.html, http://www.matrade.gov.my/en/malaysian-exporters/showcasing-malaysia-export/directory/malaysian-services-directory


#http://www.airlineupdate.com/content_subscription/mro/index/malaysia.htm returns error 403 forbidden
#http://stackoverflow.com/questions/3336549/pythons-urllib2-why-do-i-get-error-403-when-i-urlopen-a-wikipedia-page


