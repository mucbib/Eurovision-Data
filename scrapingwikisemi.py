import requests
from bs4 import BeautifulSoup
import pandas as pd
import ff_eurofunctions as eurof

#defining the timeframe and removing 2020 from the list
years = [*range(2004, 2023)]
if 2020 in years:
	years.remove(2020)

escframe = pd.DataFrame()

print("Europe, start scraping...now !\n")
for year in years:
	
	#Scraping the Wikipedia page
	print("now scraping semifinal(s) " + str(year) + "\n")

	wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(year)

	spanids, soup = eurof.get_spanids_semi(wikiurl, year)
	
	for spanid in spanids:
		
		offset = soup.find('span', id=spanid)
		if offset == None:
			print('Relevant content not found on Wikipedia. Try back-up solution.\n')
			index = spanids.index(spanid)
			wikiurl = eurof.fallbackfinal(year)
			spanids, soup = eurof.get_spanids_semi(wikiurl, year)
			spanid = spanids[index]
			offset = soup.find('span', id=spanid)
		
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
print("Done. I'm in love with a fairytale.\n")
print(escframe)

	

