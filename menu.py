#!/usr/bin/env python

# Author: Will Dey '23

import requests
from bs4 import BeautifulSoup
from datetime import date

def ul_to_string(ul):
  return_value = ""
  for li in ul.find_all('li', recursive=False):
    return_value += '  * ' + li.get_text(strip=True) + '\n'
  return return_value

today = '{today:%A} {today:%B} {today.day}'.format(today=date.today())

page = requests.get('https://dining.harvard.edu/campus-dining/undergraduate-dining/weeks-menu')
if page.status_code != 200:
  print("Received code " + page.status_code + " while trying to load HUDS website.")
  exit(1)

soup = BeautifulSoup(page.content, 'html.parser')
main_content = soup.find_all(class_='region-three-25-50-25-second')[0]
menu = main_content.table
for row in menu.find_all('tr'):
  day, lunch, dinner = row.find_all('td', recursive=False)
  if day.get_text(strip=True).startswith(today):
    print("Today's HUDS menu:")
    print(" Lunch:")
    print(ul_to_string(lunch.ul))
    print(" Dinner:")
    print(ul_to_string(dinner.ul))
