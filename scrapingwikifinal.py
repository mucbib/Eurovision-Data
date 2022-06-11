import requests
from bs4 import BeautifulSoup
import pandas as pd

jahre = [*range(2019, 2021)]
if 2020 in jahre:
	jahre.remove(2020)

escframe = pd.DataFrame()

for jahr in jahre:
	
	print("now scraping " + str(jahr) + "\n")

	wikiurl = 'https://en.wikipedia.org/wiki/Eurovision_Song_Contest_' + str(jahr)

	source = requests.get(wikiurl)
	content = source.content

	text = source.text
	soup = BeautifulSoup(text, 'lxml')
	
	if jahr < 1958:
		spanid = 'Participants_and_results'
	elif jahr > 2003:
		spanid = 'Final'
	else:
		spanid = 'Results'
	offset = soup.find('span', id=spanid)
	if offset == None:
		offset = soup.find('span', id='Participants_and_results')
		if offset == None:
			offset = soup.find('span', id='Results')
			if offset == None:
				print('Wikipedia-Abschnitt nicht gefunden.')
	#print(offset)
	offset = offset.parent
	table = offset.find_next_sibling('table')

	#columns
	columns = table.find_all('th', scope='col')
	spalten = ['Year']
	for bezeichnung in columns:
		bezeichnung = bezeichnung.get_text().strip()
		bezeichnung = bezeichnung.split('[')
		bezeichnung = bezeichnung[0]
		spalten.append(bezeichnung)
		#print(spalten)
	spalten[1] = 'Draw'
	spalten[5] = 'Language'

	#rows
	rows = table.find_all('tr')
	del(rows[0])
	zeilen = []
	for row in rows:
		row1 = row.find_all('th', scope='row')
		row2 = row.find_all('td')
		row = row1 + row2
		zeile = [jahr]
		for td in row:
			td = td.text.strip()
			td = td.split('[')
			td = td[0]
			if td[0] == '"':
				td = td.replace('"', '')
			zeile.append(td)
		zeilen.append(zeile)
		#print(zeilen)
	neuedaten = pd.DataFrame(data=zeilen, columns=spalten)
	escframe = pd.concat([escframe, neuedaten], ignore_index=True)

#1956 bereinigen
if 1956 in jahre:
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


#abspeichern	
#escframe.to_csv('eurotable_final.csv')
print(escframe.head(30))
