import datetime
start_time = datetime.datetime.strptime('10:20', '%H:%M').time()
stop_time = datetime.datetime.now().time()

date = datetime.date(1, 1, 1)
datetime1 = datetime.datetime.combine(date, start_time)
datetime2 = datetime.datetime.combine(date, stop_time)
time_elapsed = datetime2 - datetime1
print(time_elapsed > datetime.timedelta(minutes=15))

print(datetime.datetime.today().date())