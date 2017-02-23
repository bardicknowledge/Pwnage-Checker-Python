#HaveIBeenPwned:

import json, csv, sys, time
from urllib import request, parse
from urllib.error import HTTPError, URLError

headers = {"Accept": "application/vnd.haveibeenpwned.v2+json",
	"User-Agent": "Pwnage-Checker-Python"}
uri = "https://haveibeenpwned.com/api/v2/breachedaccount/{0}"

#Output the following: mail, pwnedCount, pwnedDomains, pwnedDates, rawJSON
def prepareRow(mail, pwnedList):
	rowDict = {'email' : mail}
	rowDict['pwnedCount'] = len(pwnedList)
	rowDict['rawJSON'] = pwnedList
	pwnedDomains = []
	pwnedDates = []
	for pwnedItem in pwnedList:
		pwnedDomains.append(pwnedItem['Domain'])
		pwnedDates.append(pwnedItem['BreachDate'])
	rowDict['pwnedDomains'] = '[{0}]'.format(','.join(pwnedDomains))
	rowDict['pwnedDates'] = '[{0}]'.format(','.join(pwnedDates))
	return rowDict
def checkPwned(mail, output=None):
	pwnedRequest = request.Request(uri.format(mail), headers=headers)
	try:
		response = request.urlopen(pwnedRequest)
		pwnedInfo = json.loads(response.read().decode())
		print ("Pwned count for ({0}): {1} ".format(mail, len(pwnedInfo)))
		if (output != None):
			rowVal = prepareRow(mail, pwnedInfo)
			output.writerow(rowVal)
	except HTTPError as err:
		if (err.code == 404):
			print("Pwned count for ({0}): 0".format(mail))
		else:
			print("Error while retrieving data for {0}".format(mail))

if (len(sys.argv) < 2):
	print("Usage: python haveIBeenPwned.py <email>")
	print(" python haveIBeenPwned.py -f <list.csv>")
	sys.exit()
if (sys.argv[1] != '-f'):
	mail = sys.argv[1]
	checkPwned(mail)
else:
	with open(sys.argv[2]) as csvfile:
		csvfileOut = open("output.csv", 'w')
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		fieldNames = ['email', 'pwnedCount', 'pwnedDomains', 'pwnedDates', 'rawJSON']
		csvwriter = csv.DictWriter(csvfileOut, fieldNames)
		csvwriter.writeheader()
		for row in csvreader:
			mail = row[0]
			checkPwned(mail, output=csvwriter)
			time.sleep(2)
