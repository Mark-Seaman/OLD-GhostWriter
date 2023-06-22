from calendar import day_abbr, monthrange, weekday
from datetime import datetime, timedelta
from os.path import getmtime
from pathlib import Path

from django.utils.timezone import localdate, make_aware

# ------------------------------
# Command Interpreter

def days_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd == 'list':
            days_list(args)
        elif cmd == 'month':
            days_month(args)
        elif cmd == 'today':
            print(today())
        elif cmd == 'weeks':
            days_weeks(args[0])
        else:
            days_help(args)
    else:
        days_help()


def days_help(args=None):
    print('''
        days Command

        usage: x days COMMAND

        COMMAND:

            list    - list the document files
            month   - list the days in a month
            today   - show the date for today
            weeks   - list the Mondays for N weeks
        ''')


# ------------------------------
# Functions

def is_old(path):
    if not Path(path).exists():
        return True
    modified = datetime.fromtimestamp(getmtime(path))
    now = datetime.now()
    return (now - modified).days > 1


# Convert from a time record to string
def date_str(t):
    return t.strftime("%Y-%m-%d")


# Format like   Tue, 03-11
def day_str(t):
    return t.strftime("%a, %m-%d")


# Return a date from 48 hours ago
def days_ago(date, days):
    return date_str(date-timedelta(days=days))


# Day of the week
def day_name(year, month, day):
    return day_abbr[weekday(year, month, day)]


# Calculate the days I've lived
def my_age_in_days():
    birth_date = to_date('1959-09-01')
    today = datetime.now()
    days = today - birth_date
    return days.days


# Enumerate days for the previous week
def days_list(args):
    if args:
        days = int(args[0])
    else:
        days = 7
    if args[1:]:
        today = to_date(args[1])
    else:
        today = datetime.today()

    print('Days: %d, To: %s' % (days, day_str(today)))

    for d in enumerate_days(today, days):
        print(day_str(to_date(d)))


def list_summer(start='2020-05-01', num_weeks=20):
    dates = []
    d = to_date(start)
    for w in range(num_weeks*7):
        date = d + timedelta(days=w)
        if date.weekday() < 5:
            dates.append(date.strftime("%a, %Y-%m-%d"))
    return dates


def list_unc_schedule(start='2020-08-24', num_weeks=15):
    def add_date(week, day):
        dates.append(
            (week + 1, (d + timedelta(days=day)).strftime("%a, %Y-%m-%d")))

    dates = []
    d = to_date(start)
    for w in range(num_weeks):
        if w != 2:
            add_date(w if w != 14 else 13, 7 * w)
        if w != 13:
            add_date(w if w != 14 else 13, 7 * w + 2)
        if w != 13:
            add_date(w if w != 14 else 13, 7 * w + 4)
    return dates


def list_mwf(start='2020-08-24', num_weeks=14):
    dates = []
    d = to_date(start)
    for w in range(num_weeks):
        dates.append((d + timedelta(days=7*w)).strftime("%a, %Y-%m-%d"))
        dates.append((d + timedelta(days=7*w+2)).strftime("%a, %Y-%m-%d"))
        dates.append((d + timedelta(days=7*w+4)).strftime("%a, %Y-%m-%d"))
    return dates


#  days of this month
def days_month(args):
    start = datetime.today() + timedelta(days=31 - datetime.today().day)
    for d in enumerate_days(start, 31):
        print(d)


# Save the Mondays in a file for some number of weeks
def days_weeks(start, num_weeks):

    def days_ahead(date, days):
        day = date + timedelta(days=days)
        return day

    def weekly_schedule(start, weeks):
        start = to_date(start)
        for w in range(weeks):
            print('\nWeek %s\n' % (w+1))

            for d in range(7):
                day = day_str(days_ahead(start, w*7+d))
                print(day)

    weekly_schedule(start, num_weeks)


# Convert a string to a timezone aware date
def due_date(due):
    return make_aware(datetime.strptime(due, "%Y-%m-%d"))


# List all of the days before today
def enumerate_days(today, days):
    return [days_ago(today, days-d-1) for d in range(days)]


# List all the days in the month
def enumerate_month(year, month):
    # print("\n\n%s %s\n" % (month_name[month], year))
    num_days = monthrange(year, month)[1]
    return ['%04d-%02d-%02d' % (year, month, d + 1) for d in range(num_days)]


# # List all the days in the month
# def enumerate_month_days(year, month):
#     num_days = monthrange(year, month)[1]
#     return [for d in range(num_days)]
#         x = ' %s, %04d-%02d-%02d' % (day_name(year, month, d + 1), year, month, d + 1)
#         print(x)


# Convert from string to ctime object (example format 9/1/1959)
def parse_date(s):
    return datetime.strptime(s, "%m/%d/%Y")


# List the last several days
def recent_dates(days=4, start=None):
    if not start:
        start = datetime.today()
    return [days_ago(start, days - d - 1) for d in range(days)]


# Convert from string to ctime object  (example format 1959-09-01)
def to_date(s):
    return datetime.strptime(s, "%Y-%m-%d")


# Convert from string to ctime object  (example format Tue, 09-01)
def to_day(s):
    return datetime.strptime(s, "%a, %m-%d")


# Today's date as string
def today():
    return date_str(localdate())


# Return a date for 24 hours from now
def tomorrow(date, days=1):
    return yesterday(date, -days)


# Return a date from 24 hours ago
def yesterday(date, days=1):
    return date-timedelta(days=days)
