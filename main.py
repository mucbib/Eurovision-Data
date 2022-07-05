import time
import random
import ff_eurofunctions as eurof

#Introduction
print("Ta ta-tarara ta taaa taa (imagine the music of Charpentier's 'Te Deum' right now)...\n")
time.sleep(3)
print("Welcome to mucbib Eurovision-Data, a web scraper which lets you download and save data from the Eurovision Song Contest.\n")
print("This program is licensed under MIT. See https://github.com/mucbib/Eurovision-Data for more information.\n")
time.sleep(5)
cities = ['London', 'Turin', 'Tel Aviv', 'Rotterdam', 'Lisbon', 'Kyiv', 'Stockholm', 'Vienna', 'Dublin', 'Copenhagen', 'Belgrade', 'Baku']
randomcity = random.choice(cities)
print(f"Okay, {randomcity}, are you ready ?\n")
time.sleep(2)
#User interaction: definition of what to scrape
print("Do you want to download all data from all contests from 1956 until today, including semi-finals ? (enter 'yes')")
print("Or do you want to set your own preferences (years and shows) ? (in that case enter 'no' or your favourite song by Carola).")
answer = input("yes/no: ").strip().lower()

#if yes: scrape everything
if answer == 'yes' or answer == 'y':
	eurof.scrapingwikifinal(all=True)
	time.sleep(1)
	eurof.scrapingwikisemi(all=True)
	time.sleep(1)
	eurof.merging()	
else:
	#if no: customized scraping
	print("Set your preferences. Step 1:")
	print("Do you want to get data for contests between 1956 and 2003 and/or the finals after 2004 ? (enter 'yes')")
	both = 0
	answerfinal = input("yes/no: ").strip().lower()
	if answerfinal == 'yes' or answerfinal == 'y':		
		eurof.scrapingwikifinal(False)
		both = both + 1

	time.sleep(1)
	
	print("Step 2: Do you want to get data for semi-finals ? (enter 'yes')")
	answersemi = input("yes/no: ").strip().lower()
	if answersemi == 'yes' or answersemi == 'y':
		eurof.scrapingwikisemi()
		both = both + 1
	time.sleep(1)

	#if the user has chosen to scrape both data from semi-finals and finals, ask if the two tables should be merged
	if both == 2:
		print("Do you want to merge the results from semi-finals and finals in one table ?")
		answermerge = input("yes/no: ").strip().lower()
		if answermerge == 'yes' or answermerge == 'y':
			eurof.merging()

print("End of program. Good night Europe !")
