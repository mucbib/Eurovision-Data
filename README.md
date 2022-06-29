# WHAT IT IS ABOUT
This project aims to provide the possibility to get data about all the entries in the history of the Eurovision Song Contest, by using a web scraper that lets you download and extract relevant data from the Wikipedia articles on each Eurovision Song Contest.

# HOW IT WORKS
Once a start year and end year defined, the scraper gets the HTML file of each Eurovision Song Contest's Wikipedia page, extracts data about all entries and saves them to CSV files in the directory "data".

Start and end year are defined by user input when running `scrapingwikifinal.py`and `scrapingwikisemi.py` in the terminal.

For peculiarities on the data output, see the readme.md file in the folder "data".

# HOW TO USE IT
Download the files and save them in a folder. The code is written in Python.

REQUIREMENTS to be installed before you run the files: Python (obviously), and the following Python modules: 
pandas, requests, bs4, datetime

Then go to your command line/terminal, navigate to the folder where you saved the files, and run `python3 scrapingwikifinal.py`. The program will ask you to set a start and end year. If you enter 1956 and 2022 as start and end years, for example, the program will get the data for the contests from 1956 to 2003, plus the finals from 2004-2022, and save them in "eurotable_final.csv" in the folder "data".

For the data on the semi-finals, run `python3 scrapingwikisemi.py`. Note that the earliest possible start year is 2004 for the semi-finals but as a true Eurovision fan you should know that anyway :-P. Data from the semi-finals will be saved in "eurotable_semi.csv".

In order to combine the data from semi-finals and finals in one table, and have basically ALL entries of Eurovision history, finally run `python3 merging.py` after having run the two scraping files. The results will be saved in "totaldata.csv".

# HELP! IT DOESN'T WORK
If you can't run the code, if the code is broken or if you just want to download all Eurovision data as a CSV file without doing all this strange nerd stuff, go to the folder "data" and download `totaldata_1956-2022.csv`. You'll be happy.
And, btw, if you spot any error/misfunction/ugly code, let me know !

# FUTURE PLANS FOR THIS REPOSITORY
- make it more usable by executing only one main file
- scrape more data, possibly data about the voting, host city, lyrics etc. possibly including data from eurovisionworld.com, Wikidata and/or other websites

# LICENCE
See the LICENCE file.
