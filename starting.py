import pandas as pd
import matplotlib.pyplot as plt

#####
#Data from Stanford Open Policing project, interpretation from a lesson by DataCamp.com
#####

####Importing Hartford Connecticut csv from desktop and saving as hc
hc = pd.read_csv(r'C:\Users\"!!!CHANGE TO YOUR C-DRIVE USERNAME!!!"\Desktop\ct_hartford_2019_08_13.csv')

####Evaluating the data and determining what to drop
hc.isnull().sum()
hc.shape

####Dropping columns deemed unnecessary
hc.drop(['search_basis', 'contraband_found', 'raw_intervention_disposition_code', 'raw_search_authorization_code', 'department_name', 'type'], axis='columns', inplace=True)
hc.columns

####Changing arrest made to a boolean
hc['arrest_made'] = hc['arrest_made'].astype('bool')
hc.dtypes

####Combining date and time into one column, converting to datetime and setting date_and_time as index
combined = hc.date.str.cat(hc.time, sep=' ')
hc['date_and_time'] = pd.to_datetime(combined)
hc.set_index('date_and_time', inplace=True)

####Analysis of the traffic stop, the outcome || Normalize outputs percentages instead of int's
hc.outcome.value_counts()
hc.outcome.value_counts(normalize=True)


####Creating DataFrames for males and females that were stopped for speeding use and printing the outcomes
####Finding an answer to "Does gender affect the outcome of a traffic stop?"
female_and_speeding = hc[(hc.subject_sex == 'female') & (hc.reason_for_stop == 'Moving Violation')]
male_and_speeding = hc[(hc.subject_sex == 'male') & (hc.reason_for_stop == 'Moving Violation')]
female_and_speeding.outcome.value_counts(normalize=True)
male_and_speeding.outcome.value_counts(normalize=True)

####Finding an answer to "Does gender affect who's vehicle is searched?"
hc.groupby('subject_sex').search_conducted.mean()
hc.groupby(['subject_sex', 'outcome']).search_conducted.mean()

####Visualizing "Does time of day affect arrest date?"
hourly_arrest_rate = hc.groupby(hc.index.hour).arrest_made.mean()
hourly_arrest_rate.plot()
plt.xlabel('Hour')
plt.ylabel('Arrest Rate')
plt.title('Arrest Rate by Time of Day')
#plt.show()


####Visualizing "What outcomes are in the southern district?"
all_zones = pd.crosstab(hc.district, hc.outcome)
south_zone = all_zones.loc['SOUTH END':'SOUTH WEST']
south_zone.plot(kind='bar', stacked=True)
#plt.show()



