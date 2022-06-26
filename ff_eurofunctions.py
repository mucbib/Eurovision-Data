import requests
from bs4 import BeautifulSoup
import pandas as pd

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
