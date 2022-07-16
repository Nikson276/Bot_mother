import datetime


now = datetime.datetime.now()

print(now)

str_now = now.strftime('%H:%M:%S')  # ('%Y-%m-%d %H:%M:%S') - YY-MM-DD HH-MM-SS

print(str_now)