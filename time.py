import schedule


def job(a):
    print(a)


schedule.every().saturday.at('01:19').do(job, 5)
while True:
    schedule.run_pending()