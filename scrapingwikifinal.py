import requests
from bs4 import BeautifulSoup
import pandas as pd
import ff_eurofunctions as eurof

print("Good evening Europe !\n")

#defining the timeframe and removing 2020 from the list
years = [*range(1956, 2023)]
if 2020 in years:
	years.remove(2020)

escframe = pd.DataFrame()

for year in years:
	
	#Scraping the Wikipedia page for each ESC
	print("now scraping " + str(year) + "\n")

	wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(year)
	
	offset = eurof.get_offset_final(wikiurl, year)
	
	if offset == None:
		oldid = eurof.fallbackfinal(year)
		offset = eurof.get_offset_final(oldid, year)
	
	if offset == None:
		print("Fallback solution not successful. Why me ?")
	
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
print("Done. Save your kisses for me.\n")
print(escframe)
