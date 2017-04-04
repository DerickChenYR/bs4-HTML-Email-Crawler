#emailworm_tablecrawl

import urllib.request
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import csv
import sys


start_time = datetime.now()

urls_queue = set()
n = 0

url = "http://www.iccmalaysia.org.my/Membership-@-Member_List.aspx"

component = urlparse(url)
base_url = component.scheme + '://' + component.netloc + '/'

req = urllib.request.Request(url, headers={'User-Agent':'Magic Browser'})
con = urllib.request.urlopen(req)

soup = BeautifulSoup(con, 'html.parser')

#how to crawl the other pages with data on the table on the same html link????

for a in soup.find_all('a', href=True):

	#convert all links to absolute url
	if a['href'].startswith(base_url) == True:
		urls_queue.add(a['href'])
	elif a['href'].startswith('Member_Detail.aspx') == True:
		full_url = urljoin(base_url, a['href'])
		urls_queue.add(full_url)

print (urls_queue)

A= []
B= []
C= []

for i in urls_queue:

	print ("crawling %s" %i)
	req = urllib.request.Request(i, headers={'User-Agent':'Magic Browser'})
	con = urllib.request.urlopen(req)

	soup = BeautifulSoup(con, 'html.parser')
	#find the target table via class
	table = soup.find('table', attrs={'class':'memberDetails'})
	
	try:
		#find relevant lines and add them to lists
		company_name = table.find('span', attrs={"id":"ctl00_cpContent_lbl_CompanyName"})
		A.append(company_name.string)

		telephone = table.find('span', attrs={"id":"ctl00_cpContent_lbl_Telephone"})
		B.append(telephone.string)

		email = table.find('span', attrs={"id":"ctl00_cpContent_lbl_Email"})
		C.append(email.string)

	except Exception as e:
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
		print (format(sys.exc_info()[-1].tb_lineno))

		#if error message returns on line XX:
		if format(sys.exc_info()[-1].tb_lineno) == "55":
			A.append("NIL")
			print ("A")
		elif format(sys.exc_info()[-1].tb_lineno) == "58":
			B.append("NIL")
			print ("B")
		elif format(sys.exc_info()[-1].tb_lineno) == "61":
			C.append("NIL")
			print ("C")
		else:
			
			#exception handling is wrong
			print ("wrong code!")
		continue	

print (len(A))
print (len(B))
print (len(C))

out = [[ ] for x in range(len(A)+1)]



while n < len(A):

	out[n].append(A[n])
	out[n].append(B[n])
	out[n].append(C[n])
	n += 1



with open ("ICC Malaysia Contacts.csv", "a", newline="") as result_file:
	wr = csv.writer(result_file, dialect = "excel" )
	for i in out:
		wr.writerows([i])

print ("\nRecorded.")
print (datetime.now()- start_time)





#for table scrapping https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
