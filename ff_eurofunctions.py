import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import dateutil

#FUNCTIONS:
#1. scrapingwikifinal (scrapes Wikipedia data for the finals)
#2. scrapingwikisemi (scrapes Wikipedia data for the semi-finals)
#3. merging (merges scraped data for final and semi-finals)
#4. define_years (user-defined timeframe for scraping)
#5. get_offset_final (find the section in Wikipedia (finals))
#6. get_spanids_semi (find the sections in Wikipedia (semi-finals))
#7. fallbackfinal (get Wikipedia oldid (old URL) when section can't be located)
#8. endyear (determines in which year the latest Eurovision Song Contest took place)

def scrapingwikifinal(allshows):
	print("Good evening Europe !\n")

	#defining the timeframe (user interaction)
	yeartoday = datetime.date.today().year
	if allshows == True:
		years = [*range(1956, yeartoday+1)]
		if 2020 in years:
			years.remove(2020)
	else:
		years = define_years("final")

	escframe = pd.DataFrame()

	for year in years:
		
		#Scraping the Wikipedia page for each ESC
		print("now scraping " + str(year) + "\n")
		
		if year == yeartoday:
			maxyear = endyear()
			if maxyear != yeartoday:
				print("Contest has not yet taken place.")
				break
		
		wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(year)
		
		offset = get_offset_final(wikiurl, year)
        
		if offset == None:
			oldid = fallbackfinal(year)
			offset = get_offset_final(oldid, year)
		
		if offset == None:
			print("Fallback solution not successful. Why me ?")
			continue
		
		offset = offset.parent
		table = offset.find_next_sibling('table')

		#Getting the columns
		wikicolumns = table.find_all('th', scope='col')
		columns = ['Year']
		for columnhead in wikicolumns:
			columnhead = columnhead.get_text().strip()
			columnhead = columnhead.split('[')
			columnhead = columnhead[0]
			columns.append(columnhead)
			
		#Getting the rows
		wikirows = table.find_all('tr')
		del(wikirows[0])
		entryrows = []
		for row in wikirows:
			row1 = row.find_all('th', scope='row')
			row2 = row.find_all('td')
			row = row1 + row2
			entryrow = [year]
			for td in row:
				td = td.text.strip()
				td = td.split('[')
				td = td[0]
				if td[0] == '"':
					td = td.replace('"', '')
				entryrow.append(td)
			entryrows.append(entryrow)
			#print(entryrows)
		newdata = pd.DataFrame(data=entryrows, columns=columns)
		escframe = pd.concat([escframe, newdata], ignore_index=True)

	#Clean up 1956
	if 1956 in years:
		reihen56 = escframe.Year == 1956
		escframe.loc[reihen56,'Place'] = 0
		escframe.loc[reihen56,'Points'] = -1
		refrain = escframe.loc[(escframe['Year'] == 1956) & (escframe['Song'] == 'Refrain')]
		escframe.loc[refrain.index[0], 'Place'] = 1

	#North Macedonia = Macedonia
	macedonia = escframe.loc[escframe['Country'] == 'North Macedonia']
	if macedonia.empty == False:
		northmacedonia = escframe.Country == 'North Macedonia'
		escframe.loc[northmacedonia,'Country'] = 'Macedonia'

	#save
	escframe.to_csv('data/eurotable_final.csv')
	
	print(escframe)
	print("Data was saved in data/eurotable_final.csv\n")
	print("Done. Save your kisses for me.\n")

def scrapingwikisemi(allshows):
	
	#defining the timeframe (user interaction)	
	yeartoday = datetime.date.today().year
	if allshows == True:
		years = [*range(2004, yeartoday+1)]
		if 2020 in years:
			years.remove(2020)
	else:
		years = define_years("semi")

	escframe = pd.DataFrame()

	print("Europe, start scraping...now !\n")
	for year in years:
		
		#Scraping the Wikipedia page
		print("now scraping semifinal(s) " + str(year) + "\n")

		if year == yeartoday:
			maxyear = endyear()
			if maxyear != yeartoday:
				print("Contest has not yet taken place.")
				break

		wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(year)
		
		spanids, soup = get_spanids_semi(wikiurl, year)
		
		for spanid in spanids:
			
			offset = soup.find('span', id=spanid)
			if offset == None:
				print('Relevant content not found on Wikipedia. Try back-up solution.\n')
				index = spanids.index(spanid)
				wikiurl = fallbackfinal(year)
				spanids, soup = get_spanids_semi(wikiurl, year)
				spanid = spanids[index]
				offset = soup.find('span', id=spanid)
				
			if offset == None:
				print("Fallback solution not successful. Why me ?")
				continue
			
			offset = offset.parent
			table = offset.find_next_sibling('table')

			#columns
			wikicolumns = table.find_all('th', scope='col')
			columns = ['Year', 'SF']
			
			for columnhead in wikicolumns:
				columnhead = columnhead.get_text().strip()
				#remove annotations
				columnhead = columnhead.split('[')
				columnhead = columnhead[0]
				columns.append(columnhead)
			columns[2] = 'SF_Order'
			columns[7] = 'SF_Place'
			columns[8] = 'SF_Points'

			#rows
			wikirows = table.find_all('tr')
			del(wikirows[0])
			entryrows = []
			for row in wikirows:
				row1 = row.find_all('th', scope='row')
				row2 = row.find_all('td')
				row = row1 + row2
				if 2003 < year < 2008:
					SFvalue = 'SF'
				else:
					SFvalue = spanid[-1]
				entryrow = [year, SFvalue]
				for td in row:
					td = td.text.strip()
					td = td.split('[')
					td = td[0]
					if td[0] == '"':
						td = td.replace('"', '')
					entryrow.append(td)
				entryrows.append(entryrow)
				#print(entryrows)
			newdata = pd.DataFrame(data=entryrows, columns=columns)
			escframe = escframe.append(newdata)

	#North Macedonia = Macedonia
	macedonia = escframe.loc[escframe['Country'] == 'North Macedonia']
	if macedonia.empty == False:
		northmacedonia = escframe.Country == 'North Macedonia'
		escframe.loc[northmacedonia,'Country'] = 'Macedonia'

	#save
	escframe.to_csv('data/eurotable_semi.csv')

	print(escframe)
	print("Data was saved in data/eurotable_semi.csv\n")
	print("Done. I'm in love with a fairytale.\n")

#merging data from final and semi-finals
def merging():
	print("Merging all data...\n")

	#load and prepare the tables
	finaldata = pd.read_csv('data/eurotable_final.csv')
	finaldata['Order'] = finaldata.Order.astype('Int64')
	finaldata['Place'] = finaldata.Place.astype('Int64')
	finaldata['Points'] = finaldata.Points.astype('Int64')
	finaldata = finaldata.drop(labels="Unnamed: 0", axis=1)

	semidata = pd.read_csv('data/eurotable_semi.csv')
	semidata = semidata.drop(labels="Unnamed: 0", axis=1)
	semidata['SF_Order'] = semidata.SF_Order.astype('Int64')
	semidata['SF_Place'] = semidata.SF_Place.astype('Int64')
	semidata['SF_Points'] = semidata.SF_Points.astype('Int64')

	#merging
	merge_subset = ['Year', 'Country', 'Song', 'Artist', 'Language']
	totaldata = finaldata.merge(semidata, how='outer', on=merge_subset)

	#deduplicating some duplicates from Wikipedia
	duplicate_subset = ['Year', 'Country', 'Artist', 'Song']
	##finding the duplicated rows and putting them apart in two dataframes
	duplicates1 = totaldata[totaldata.duplicated(duplicate_subset, keep='last')]
	duplicates2 = totaldata[totaldata.duplicated(duplicate_subset)]
	##merging the duplicate frames in one, dropping the Language-column in semifinals (duplicates2)
	duplicates1 = duplicates1.drop(['SF', 'SF_Order', 'SF_Points', 'SF_Place'], axis=1)
	duplicates2 = duplicates2.drop(['Language', 'Order', 'Place', 'Points'], axis=1)
	duplicatestotal = duplicates1.merge(duplicates2, how='outer', on=['Year', 'Country', 'Song', 'Artist'])
	#merging the cleaned-up rows everything with the big table and deduplicating, keeping the cleaned-up rows
	totaldata = totaldata.append(duplicatestotal)
	totaldata = totaldata.drop_duplicates(subset=duplicate_subset, keep='last')
	#making everything nice and tidy again
	totaldata = totaldata.sort_values(['Year', 'Order', 'SF', 'SF_Order'])


	#save to CSV
	totaldata.to_csv('data/totaldata.csv')

	print(totaldata)
	print("Data was saved to data/totaldata.csv\n")
	print("Viva la Diva !\n")



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

#Find out what the latest ESC was and take that as the latest possible endpoint
def endyear():
	yeartoday = datetime.date.today().year +1
	datetoday = datetime.date.today()
	
	#take the Wikipedia page of the ESC which is this year
	wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(yeartoday)
	source = requests.get(wikiurl)
	content = source.content

	text = source.text
	soup = BeautifulSoup(text, 'lxml')
	
	#get the infobox and the content of the field "Final"
	offset = soup.find('th', class_='infobox-label', text='Final')
	infobox = offset.find_next_sibling('td', class_='infobox-data')
	finaldate = infobox.text
	
	#parse that text content as a date
	try:
		finaldate = dateutil.parser.parse(finaldate)
	except ValueError: 
		#if parsing fails, assume the contest has not yet taken place (otherwise there should be a date)
		maxyear = yeartoday - 1
	else:
		finaldate = datetime.datetime.date(finaldate)
		if datetoday > finaldate: #if date of the ESC in the past: take this year as latest ESC year
			maxyear = yeartoday
		else:
			maxyear = yeartoday - 1 #else: assume the latest ESC was last year
	return maxyear
