# WHAT IT IS ABOUT
This project aims to provide the possibility to get data about all the entries in the history of the Eurovision Song Contest, by using a web scraper that lets you download and extract relevant data from the Wikipedia articles on each Eurovision Song Contest.

# HOW IT WORKS
Once a start year and end year defined, the scraper gets the HTML file of each Eurovision Song Contest's Wikipedia page, extracts data about all entries and saves them to CSV files.

To define your own start and end year, go to the files "scrapingwikifinal.py" and "scrapingwikisemi.py" and change the line 5:

`years = [*range(1956, 2023)]`

For example, `years = [*range(2014,2022)]` will give you the data for the contests between 2014 and 2021(!).

For peculiarities on the data output, see the readme.md file in the folder "data".

# HOW TO USE IT
Download the files and save them in a folder. The code is written in Python.

REQUIREMENTS to be installed before you run the files: Python (obviously), and the following Python modules: 
pandas, requests, bs4

Then go to your command line/terminal, navigate to the folder where you saved the files, and run `python3 scrapingwikifinal.py`. This will get the data for the contests from 1956 to 2003, plus the finals from 2004-2022, and save them in "eurotable_final.csv".
For the data on the semi-finals from 2004-2022, run `python3 scrapingwikisemi.py`.
For combine the data from semi-finals and finals in one table, and have basically ALL entries of Eurovision history, finally run `python3 merging.py` after having run the two scraping files.

# HELP! IT DOESN'T WORK
If you can't run the code, if the code is broken or if you just want to download all Eurovision data as a CSV file without doing all this strange nerd stuff, go to the folder "data" and download `totaldata_1956-2022.csv`. You'll be happy.
And, btw, if you spot any error/misfunction/ugly code, let me know !

# FUTURE PLANS FOR THIS REPOSITORY
- include a fallback option in case scraping Wikipedia doesn't work correctly anymore.
- make it more usable by including an option to enter start and end years via the command line, and executing only one main file
- scrape more data, possibly data about the voting, host city, lyrics etc. possibly including data from eurovisionworld.com, Wikidata and/or other websites

# LICENCE
See the LICENCE file.
