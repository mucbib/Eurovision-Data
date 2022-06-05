import requests
from bs4 import BeautifulSoup
import pandas as pd

jahre = [*range(1956, 2023)]
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
	
	if jahr == 1956:
		spanid = 'Participants_and_results'
	elif jahr > 2003:
		spanid = 'Final'
	else:
		spanid = 'Results'
	offset = soup.find('span', id=spanid)
	if offset == None:
		offset = soup.find('span', id='Participants_and_results')
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
	escframe = escframe.append(neuedaten)
escframe.to_csv('eurotable.csv')
print(escframe.head(20))

	

