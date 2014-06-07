import urllib2
import re
import time
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
	except URLError:
		print "waiting"
		time.sleep(2)
		openurluntilok(url)
	else:
		print "wtf!?break!"
		return None

# open a file for store data
f = open('weather-data.csv', 'w')
noMatchCounter = 0
leapYear = [2004,2008,2012]

# define regx pattern
prog = re.compile(r'^((?:\w+\W)+) +(\d*\.\d*) C +(\d*\.\d*) C', re.M)
progmax = re.compile(r'Maximum Air Temperature\s*(\d+\.\d+) C', re.M|re.I)
progmin = re.compile(r'Minimum Air Temperature\s*(\d+\.\d+) C', re.M|re.I)

defaultData = init() # store the temp data for everday

# finish the csv header
header = "DATE,HKO_MAX,HKO_MIN," + ','.join('%s MIN,%s MAX' % (x,x) for x in defaultData.keys()) + '\n'
f.write(header)

# loop all the date
for y in range(2001,2015):
	for m in range(1,13):
		for d in range(1,32):

			# check month and leap year
			if (m==2 and ((d > 28 and y not in leapYear) or (d > 29 and y in leapYear))):
				break
			elif (m in [4,6,9,11] and d > 30):
				break

			# convert to str
			ystr = str(y)
			mstr = str(m).zfill(2)
			dstr = str(d).zfill(2)

			# open url
			timestamp = ystr + mstr + dstr
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
				matchMax = progmax.search(rawData)
				matchMin = progmin.search(rawData)

				# convert them to row data
				if matches and matchMax and matchMin:
					for match in matches:
						key = match[0].upper().strip().strip('\t')
						value = match[1] + ',' + match[2]
						defaultData[key] = value
					row = timestamp + ',' + matchMax.group(1) + ',' + matchMin.group(1) + ',' + ','.join('%s' % x for x in defaultData.values()) + '\n'
				else:
					print "No match even have data!!"
			else:
				print "No match!!"
				noMatchCounter += 1
				row = timestamp + ',NA,NA,' + ','.join('%s' % x for x in defaultData.values()) + '\n'

			# write row to file
			f.write(row)
			defaultData = init()

# finish and close the file
f.close()
print "Total number of fail:" + str(noMatchCounter)
