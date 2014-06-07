import urllib2
import re
from BeautifulSoup import BeautifulSoup

url = "http://www.hko.gov.hk/cgi-bin/hko/yes.pl?year=2003&month=09&day=08&language=english"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
rawData = str(soup.findAll('pre')[0].contents[0])
print rawData
prog = re.compile(r'^((?:\w+\W)+) +(\d*\.\d*) C +(\d*\.\d*) C', re.M)
m = prog.findall(rawData)
if m:
	for match in m:
		print match
		# fp.write('\n'.join('%s %s' % x for x in mylist))
else:
	print "No match!!"