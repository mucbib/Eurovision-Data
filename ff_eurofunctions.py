import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

#define timeframe to scrape (interaction with user)
def define_years(modus):
	if modus == "semi":
		beginning = 2004
	else:
		beginning = 1956
	
	yeartoday = datetime.date.today().year
	#defining the timeframe and removing 2020 from the list
	print(f"From which contests do you want to get data ?\nPlease enter a start year ({beginning}-today):\n")
	startvalid = False
	endvalid = False

	while startvalid == False:
		start = input().strip()
		if start.isnumeric() == False:
			print("Please enter a valid year !")
			continue
		start = int(start)
		if not beginning <= start <= yeartoday:
			print(f"Year must be between {beginning} and today !")
			continue
		startvalid = True

	print("\nThank you ! Now please enter an end year (between your start year and today):\n")

	while endvalid == False:
		end = input().strip()
		if end.isnumeric() == False:
			print("Please enter a valid year !")
			continue
		end = int(end)
		if not beginning <= end <= yeartoday:
			print(f"Year must be between {beginning} and today !")
			continue
		if end < start:
			print("Ehm...your end year should be higher than your start year.")
			continue
		endvalid = True
		#end has to be augmented so that the range-function (later used) delivers the correct year
		end = end + 1

	print("\nMerci chérie !\n")

	#end muss größer als start sein

	years = [*range(start, end)]
	if 2020 in years:
		years.remove(2020)
	
	return years


#Find section in Wikipedia (finals)
def get_offset_final(wikiurl, year):

	source = requests.get(wikiurl)
	content = source.content

	text = source.text
	soup = BeautifulSoup(text, 'lxml')
	
	#Locating the results table in the HTML file
	if year < 2004:
		spanid = 'Participants_and_results'
	else:
		spanid = 'Final'
	offset = soup.find('span', id=spanid)
	return offset

#Find section in Wikipedia (semi-finals)
def get_spanids_semi(wikiurl, year):
	source = requests.get(wikiurl)
	content = source.content

	text = source.text
	soup = BeautifulSoup(text, 'lxml')
	
	#Localising the tables for semi-final 1 and 2
	if 2003 < year < 2008:
		spanids = ['Semi-final']
	else:
		spanids = ['Semi-final_1', 'Semi-final_2']
	return spanids, soup
		


#Fallback option (finals): get an old Wikipedia page that will work
def fallbackfinal(year):
	print("Try back-up solution.")
	#get the CSV file with the oldid-URLs and turn it into a dictionary
	fallbacktable = pd.read_csv('data/oldids_final.csv')
	fallbacktable = fallbacktable.set_index('Year')

	fb_array = fallbacktable.to_dict(orient='index')
	#read the oldid-URL and return it
	oldid = fb_array[year]['oldid']
	return oldid
