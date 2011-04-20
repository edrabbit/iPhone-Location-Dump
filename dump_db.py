import optparse

#Convert an iPhone "epoch" timestamp to unix epoch
def realepoch(iptime):
	import time
	jan1 = 978307200	#GMT time for 2001-01-01 00:00:00
	timest = time.localtime(iptime + jan1) #returns timestruct
	return time.mktime(timest)
	
			
#Take SQLite db, dump out CSV of CellLocation table
def db_dump_celllocation(dbfile):
	from pysqlite2 import dbapi2 as sqlite
	connection = sqlite.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute('SELECT rowid, MCC, MNC, LAC, CI, Timestamp, Latitude, Longitude, HorizontalAccuracy, Altitude, VerticalAccuracy, Speed, Course, Confidence FROM CellLocation')
	results = cursor.fetchall()
	for row in results:
		returnrow = row
		returnrow = returnrow[0:4] + (realepoch(returnrow[4]),) + returnrow[5:]	#fix timestamp into a realepoch time
		print ','.join((str(x) for x in returnrow))

#Take SQLite db, dump out CSV of WifiLocation table
def db_dump_wifilocation(dbfile):
	from pysqlite2 import dbapi2 as sqlite
	connection = sqlite.connect(dbfile)
	cursor = connection.cursor()
	cursor.execute('SELECT rowid, MAC, Timestamp, Latitude, Longitude, HorizontalAccuracy, Altitude, VerticalAccuracy, Speed, Course, Confidence FROM WifiLocation')
	results = cursor.fetchall()
	for row in results:
		returnrow = row
		returnrow = returnrow[0:2] + (realepoch(returnrow[2]),) + returnrow[3:]	#fix timestamp into a realepoch time
		print ','.join((str(x) for x in returnrow))

def main():
	parser = optparse.OptionParser()
	(options, args) = parser.parse_args()
	if len(args) == 0:
		print "USAGE: db_dump.py path_to_consolidated.db"
		print "Will dump out table contents with timestamp converted to unix timestamp"
	elif len(args) == 1:
		db_dump_celllocation(args[0])
		db_dump_wifilocation(args[0])
		
if __name__ == "__main__":
	main()