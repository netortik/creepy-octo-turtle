import datetime
import sys

start_date=sys.argv[1]

#print start_date 

date=datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date=date + datetime.timedelta(days=7)
end_date = end_date.strftime("%Y-%m-%d")

print end_date
