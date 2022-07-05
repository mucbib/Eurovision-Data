# WHAT IT IS ABOUT
This project aims to provide the possibility to get data about all the entries in the history of the Eurovision Song Contest, by using a web scraper that lets you download and extract relevant data from the Wikipedia articles on each Eurovision Song Contest.

# HOW IT WORKS
Once a start year and end year defined, the scraper gets the HTML file of each Eurovision Song Contest's Wikipedia page, extracts data about all entries and saves them to CSV files in the directory "data".

Start and end year can be defined by user input when running `main.py` in the terminal.

For peculiarities on the data output, see the readme.md file in the folder "data".

# HOW TO USE IT
Download the files and save them in a folder. The code is written in Python.

REQUIREMENTS to be installed before you run the files: Python (obviously), and the following Python modules: 
pandas, requests, bs4, lxml.

Then go to your command line/terminal, navigate to the folder where you saved the files, and run `python3 main.py`:
- The program will ask you if you want to download all available data (option 1). If you answer by typing "yes", all data will be scraped and saved in `data/totaldata.csv`. The simplest and most convenient way to get ALL data without much fuss.
- If you answer "no", you can customize the output by choosing whether to get data only for the finals (1956-today), or only for the semi-finals (2004-today), or for both. At each step, you can define your own start and end years. Data will be saved in `data/eurotable_final.csv`and `data/eurotable_semi.csv`.
- If you choose to scrape data both from semi-finals and finals, you will be asked if you want to merge the results in one big table. The output will be saved in `data/totaldata.csv`.

You can also scrape data individually and more manually by running separately the files `python3 scrapingwikifinal.py`, `python3 scrapingwikisemi.py` and finally `python3 merging.py`.

# HELP! IT DOESN'T WORK
If you can't run the code, if the code is broken or if you just want to download all Eurovision data as a CSV file without doing all this strange nerd stuff, go to the folder "data" and download `totaldata_1956-2022.csv`. You'll be happy.
And, btw, if you spot any error/misfunction/ugly code, let me know !

# FUTURE PLANS FOR THIS REPOSITORY
- scrape more data, possibly data about the voting, host city, lyrics etc. possibly including data from eurovisionworld.com, Wikidata and/or other websites

# LICENCE
See the LICENCE file.
