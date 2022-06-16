import pandas as pd

print("Merging all data...\n")

finaldata = pd.read_csv('eurotable_final.csv')
finaldata['Order'] = finaldata.Order.astype('Int64')
finaldata['Place'] = finaldata.Place.astype('Int64')
finaldata['Points'] = finaldata.Points.astype('Int64')
finaldata = finaldata.drop(labels="Unnamed: 0", axis=1)

semidata = pd.read_csv('eurotable_semi.csv')
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
totaldata.to_csv('totaldata.csv')
print("Viva la Diva !\n")
print(totaldata)

