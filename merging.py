import pandas as pd

#finaldata = pd.read_csv('eurotable_final.csv', dtype={'Place': int})
finaldata = pd.read_csv('eurotable_final.csv')
finaldata['Draw'] = finaldata.Draw.astype('Int64')
finaldata['Place'] = finaldata.Place.astype('Int64')
finaldata['Points'] = finaldata.Points.astype('Int64')
finaldata = finaldata.drop(labels="Unnamed: 0", axis=1)

#print(finaldata)
semidata = pd.read_csv('eurotable_semi.csv')
semidata = semidata.drop(labels="Unnamed: 0", axis=1)
semidata['SF_Draw'] = semidata.SF_Draw.astype('Int64')
semidata['SF_Place'] = semidata.SF_Place.astype('Int64')
semidata['SF_Points'] = semidata.SF_Points.astype('Int64')

totaldata = finaldata.merge(semidata, how='outer', on=['Year', 'Country', 'Song', 'Artist', 'Language'])
totaldata.to_csv('totaldata.csv')
print(totaldata)

