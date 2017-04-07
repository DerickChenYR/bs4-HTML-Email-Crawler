#emailworm_tablecrawl

import urllib.request
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import csv



start_time = datetime.now()

urls_queue = set()
n = 0

#example website
url = "http://www.iccmalaysia.org.my/Membership-@-Member_List.aspx"

component = urlparse(url)
base_url = component.scheme + '://' + component.netloc + '/'

req = urllib.request.Request(url, headers={'User-Agent':'Magic Browser'})
con = urllib.request.urlopen(req)

soup = BeautifulSoup(con, 'html.parser')

#find all links in url
for a in soup.find_all('a', href=True):

	#convert all links to absolute url
	if a['href'].startswith(base_url) == True:
		urls_queue.add(a['href'])
	elif a['href'].startswith('Member_Detail.aspx') == True:
		full_url = urljoin(base_url, a['href'])
		urls_queue.add(full_url)

print (urls_queue)

#lists to store variables 
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
		if company_name != None:
			A.append(company_name.string)
		else:
			A.append("NIL")

		telephone = table.find('span', attrs={"id":"ctl00_cpContent_lbl_Telephone"})
		if telephone != None:
			B.append(telephone.string)
		else:
			B.append("NIL")

		email = table.find('span', attrs={"id":"ctl00_cpContent_lbl_Email"})
		if email != None:
			C.append(email.string)
		else:
			C.append("NIL")		


	except Exception as e:
		print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
		print (format(sys.exc_info()[-1].tb_lineno))

		
#check if lists have same number of entries to ensure they correctly correspond to sister cells in csv file
print (len(A))
print (len(B))
print (len(C))

out = [[ ] for x in
       range(len(A)+1)]

while n < len(A):

	out[n].append(A[n])
	out[n].append(B[n])
	out[n].append(C[n])
	n += 1

	
#write to CSV
with open ("ICC Malaysia Contacts.csv", "a", newline="") as result_file:
	wr = csv.writer(result_file, dialect = "excel" )
	for i in out:
		wr.writerows([i])

print ("\nRecorded.")
print (datetime.now()- start_time)



