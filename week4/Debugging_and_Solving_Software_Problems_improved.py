#!/usr/bin/env python3


import csv
import datetime
import requests


FILE_URL = "https://storage.googleapis.com/gwg-hol-assets/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def get_date_employees_dictionary(url):
    data = get_file_lines(url)
    reader = csv.reader(data[1:])
    date_employees_dic = {}
    for row in reader:
        row_date = row[3]
        if row_date in date_employees_dic.keys():
            date_employees_dic[row_date].append("{} {}".format(row[0], row[1]))
        else:
            date_employees_dic[row_date] = ["{} {}".format(row[0],row[1])]
    return date_employees_dic


def get_same_or_newer(start_date, url):
    """Returns the employees that started on the given date, or the closest one."""


    # We want all employees that started at the same date or the closest newer
    # date. To calculate that, we go through all the data and find the
    # employees that started on the smallest date that's equal or bigger than
    # the given start date.
    min_date = datetime.datetime.today()
    min_date_employees = []
    date_employees_dic = get_date_employees_dictionary(url)

        # date_employees_dic[row_date] = row[4]
        # If this date is smaller than the one we're looking for,
        # we skip this row
    for row_date_str, employee in date_employees_dic.items():
        row_date = datetime.datetime.strptime(row_date_str, "%Y-%m-%d")
        if row_date < start_date:
            continue

        # If this date is smaller than the current minimum,
        # we pick it as the new minimum, resetting the list of
        # employees at the minimal date.
        if row_date < min_date:
            min_date = row_date
            min_date_employees = []

        # If this date is the same as the current minimum,
        # we add the employee in this row to the list of
        # employees at the minimal date.
        if row_date == min_date:
            min_date_employees.append("{}".format(date_employees_dic[row_date_str]))

    return min_date, min_date_employees

def list_newer(start_date):
    start_date, employees = get_same_or_newer(start_date,FILE_URL)
    date_employees_dic = get_date_employees_dictionary(FILE_URL)
    if start_date < datetime.datetime.today():
        for date_str, employee in date_employees_dic.items():
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date > start_date:
                print("Started on {}: {}".format(date.strftime("%b %d, %Y"), employee))

        # Now move the date to the next one
        # start_date = start_date + datetime.timedelta(days=1)

def main():
    start_date = get_start_date()
    list_newer(start_date)


# def main():
#     print(get_date_employees_dictionary(FILE_URL))

# def main():
#     start_date = get_start_date()
#     min_date, min_date_employees = get_same_or_newer(start_date)
#     print("Minimum date is: {}, the min_date_employees are:{}".format(min_date,min_date_employees))
if __name__ == "__main__":
    main()
