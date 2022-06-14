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
totaldata = finaldata.merge(semidata, how='outer', on=['Year', 'Country', 'Song', 'Artist', 'Language'])
#save to CSV
totaldata.to_csv('totaldata.csv')

print("Viva la Diva !\n")
print(totaldata)

