import urllib2
import re
import time
import datetime
from BeautifulSoup import BeautifulSoup

# hard code all the monitoring site in a dict
def init():
	return {
	'KING\'S PARK': 'NA,NA',
	'WONG CHUK HANG': 'NA,NA',
	'TA KWU LING': 'NA,NA',
	'LAU FAU SHAN': 'NA,NA',
	'TAI PO': 'NA,NA',
	'SHA TIN': 'NA,NA',
	'TUEN MUN': 'NA,NA',
	'TSEUNG KWAN O': 'NA,NA',
	'SAI KUNG': 'NA,NA',
	'CHEUNG CHAU': 'NA,NA',
	'CHEK LAP KOK': 'NA,NA',
	'TSING YI': 'NA,NA',
	'SHEK KONG': 'NA,NA',
	'TSUEN WAN HO KOON': 'NA,NA',
	'TSUEN WAN SHING MUN VALLEY': 'NA,NA',
	'TSUEN WAN': 'NA,NA',
	'HONG KONG PARK': 'NA,NA',
	'SHAU KEI WAN': 'NA,NA',
	'KOWLOON CITY': 'NA,NA',
	'HAPPY VALLEY': 'NA,NA',
	'WONG TAI SIN': 'NA,NA',
	'STANLEY': 'NA,NA',
	'KWUN TONG': 'NA,NA',
	'SHAM SHUI PO': 'NA,NA'
	}

# open url until ok
def openurluntilok(url):
	try:
		return urllib2.urlopen(url)
	except urllib2.URLError:
		print "waiting"
		time.sleep(2)
		waitCounter += 1
		return openurluntilok(url)
	else:
		print "wtf!?break!"
		return None

# gen date
def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

# open a file for store data
f = open('weather-data.csv', 'w')
noMatchCounter = 0
waitCounter = 0
leapYear = [2004,2008,2012]

# define regx pattern
prog = re.compile(r'^((?:\w+\W)+) +(\d*\.\d*) C +(\d*\.\d*) C', re.M)
progMax = re.compile(r'Maximum Air Temperature\s*(\d+\.\d+) C', re.M|re.I)
progMin = re.compile(r'Minimum Air Temperature\s*(\d+\.\d+) C', re.M|re.I)
# store the temp data for everday
defaultData = init() 

# finish the csv header
header = "DATE,HKO_MAX,HKO_MIN," + ','.join('%s MIN,%s MAX' % (x,x) for x in defaultData.keys()) + '\n'
f.write(header)


start_date = datetime.date(2000,1,1)
end_date = datetime.date.today()
# loop all the date
for single_date in daterange(start_date, end_date):
	y = single_date.year
	m = single_date.month
	d = single_date.day

	# convert to str
	ystr = str(y)
	mstr = str(m).zfill(2)
	dstr = str(d).zfill(2)
	timestamp = single_date.strftime('%Y-%m-%d')

	# open url
	print "Getting data for " + timestamp
	url = "http://www.hko.gov.hk/cgi-bin/hko/yes.pl?year=" + ystr + "&month=" + mstr + "&day=" + dstr + "&language=english"
	page = openurluntilok(url)

	# get the data
	soup = BeautifulSoup(page).findAll('pre')

	# check list empty or not
	if soup:
		# find the data
		rawData = soup[0].contents[0]
		matches = prog.findall(rawData)
		matchMax = progMax.search(rawData)
		matchMin = progMin.search(rawData)

		# convert them to row data
		if matches and matchMax and matchMin:
			for match in matches:
				key = match[0].upper().strip().strip('\t')
				value = match[1] + ',' + match[2]
				defaultData[key] = value
			row = timestamp + ',' + matchMax.group(1) + ',' + matchMin.group(1) + ',' + ','.join('%s' % x for x in defaultData.values()) + '\n'
			# write row to file
			f.write(row)
		else:
			print "No match even have data!!"
			raise "No match"
	else:
		print "No match!!"
		noMatchCounter += 1

	defaultData = init()
	# end for

# finish and close the file
f.close()
print "We are finish:)"
print "Total number of fail:" + str(noMatchCounter)
print "Total number of wait:" + str(waitCounter)
