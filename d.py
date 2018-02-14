from datetime import datetime
import calendar

d = datetime.utcnow()
print d 
unixtime = calendar.timegm(d.utctimetuple())
print unixtime


d = '2018-02-13 12:50:24.350675'
unixtime = calendar.timegm(d)
print unixtime 

