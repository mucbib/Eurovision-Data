This folder contains ready-to-use data files in CSV format. Each file contains data about the Eurovision Song Contests from 1956 to 2022 - without 2020.

## CONTENTS
eurotable_final_1956-2022.csv contains data about the finals from 1956 to 2022.

eurotable_semi_2004-2022.csv contains data about the semi-finals from 2004 (when they were introduced) to 2022.

For each competing entry, these two tables give the running order, country, artist, song, language, place and points. 
The table on the semi-finals give also the information in which semi-final the entry was performed (column "SF"): value "1" or "2"; for the years 2004-2007, when only one semi-final took place, the value is "SF".

totaldata_1956-2022.csv gives you all the data from the two previous tables combined.

## PECULARITIES
On the data for 1956:
There were no points awarded, and the places of the entries have never been revealed, except for the winner. All entries for 1956 have therefore "-1" as value in the column "Points" (that is in order to distinguish them from real Nulpointers). All entries, except "Refrain", have the value "0" in the column "Place".

On 2020:
Due to Covid-19, the Eurovisiong Song Contest did not take place in 2020, therefore data from this year is not included here.

On North Macedonia:
FYROM/Macedonia/North Macedonia is one country but has competed under different names throughout Eurovision history. The country name used here is simply "Macedonia".
