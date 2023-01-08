import pandas as pd

'''
Dataframe manipulation:
- change data and time of shooting incidence to datetime format for easier access later on
- create new columns for the date and hour of the shooting
- drop all duplicate entries if there are any
- drop all entries with a zipcode equal to 0, which would be entries that could not be localized and therefore could be faulty
- drop all entries form 2020 and 2021 as the Covid years were chosen not to be included in the Machine Learning algorithm
- drop all entries with duplicate incident keys, these are shootings with either multiple shooters or multiple victims, which for this case was chosen to be counted as one shooting
- reset index of the dataframe
'''

df = pd.read_csv('NYC_full_with_data.csv')

df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'])

df['date'] = df['OCCUR_DATE'].dt.date
df['hour'] = df['OCCUR_TIME'].dt.hour

df.sort_values(by='OCCUR_DATE', inplace=True)
df.drop_duplicates(inplace=True, keep='first')

df.drop(df[(df['Zipcode'] == 0)].index, inplace=True)

df.drop(df[(df['OCCUR_DATE'].dt.year == 2020) | (df['OCCUR_DATE'].dt.year == 2021)].index, inplace=True)

df.drop_duplicates(subset="INCIDENT_KEY", keep='first', inplace=True)
df = df.reset_index(drop=True)


'''
The following code are three functions to retrieve CSVs which will be used to predict the probability of a shooting happening either for each day of the week per borough, every hour for each day of the week per borough, or each day of the week per zipcode.
Due to the fact that the original CSV only shows shooting incidences, a new dataframe had to be created that takes every timepoint (which definition can be changed as mentioned above, either for every individual hour or only for the dates) for all the boroughs/zipcodes.
This results in every entry of the dataframe containing a value that shows that there either was or wasn't a shooting incident at that exact timepoint, which then allows for a prediction of shooting incident happening at a certain time.
'''

# Get a CSV with an entry for every hour and every date between 2006 and 2019 for each borough
def get_every_day_and_every_hour_per_boro_csv():

    boros = df.BORO.unique().tolist()   # find all unique boroughs

    # create a new df with all hours for every date between 2006 and 2019
    dates = pd.date_range(start='2006-01-01', end='2020-01-01', freq='h', normalize=True).tolist()
    new_df = pd.DataFrame({'date': []})
    new_df = new_df.assign(date=dates)
    new_df.drop(index=new_df.index[-1], axis=0, inplace=True)
    new_df['calendar_date'] = new_df['date'].dt.date
    new_df['hour'] = new_df['date'].dt.hour
    new_df['day_of_week'] = new_df['date'].dt.dayofweek
    new_df['shooting'] = 0  # set all shooting incidents to 0 as default, which will be overwritten later on should there have been a shooting
    new_df['boro'] = boros[0]   # set all boroughs to the first entry in the list

    # overwrite all entries for the first borough for which there has been a shooting incident at that exact time
    for i in range(len(df)):
        if df['BORO'][i] == boros[0]:
            index_value = new_df[
                (new_df['calendar_date'] == df['date'][i]) & (new_df['hour'] == df['hour'][i])].index.values

            new_df.at[index_value[0], 'shooting'] = 1

    boros.pop(0)    # drop the first borough from the list

    # create a new dataframe for the next entry in the list and repeat the steps for the first dataframe
    # once done, concatenate the new dataframe to the first one, this will in the end give a dataframe containing all the hours and dates for every borough
    for i in boros:
        temp_df = pd.DataFrame({'date': []})
        temp_df = temp_df.assign(date=dates)
        temp_df.drop(index=temp_df.index[-1], axis=0, inplace=True)
        temp_df['calendar_date'] = temp_df['date'].dt.date
        temp_df['hour'] = temp_df['date'].dt.hour
        temp_df['day_of_week'] = temp_df['date'].dt.dayofweek
        temp_df['shooting'] = 0
        temp_df['boro'] = i
        for j in range(len(df)):
            if df['BORO'][j] == i:
                index_value = temp_df[
                    (temp_df['calendar_date'] == df['date'][j]) & (temp_df['hour'] == df['hour'][j])].index.values

                temp_df.at[index_value[0], 'shooting'] = 1
        frames = [new_df, temp_df]
        new_df = pd.concat(frames)

    new_df.to_csv('NYC_boro_every_day_every_hour.csv')


# Get a CSV with an entry for date between 2006 and 2019 for each borough
def get_every_day_per_boro_csv():
    boros = df.BORO.unique().tolist()   # find all unique boroughs

    # create a new df with for every date between 2006 and 2019
    dates = pd.date_range(start='2006-01-01', end='2019-12-31', normalize=True).tolist()
    new_df = pd.DataFrame({'date': []})
    new_df = new_df.assign(date=dates)
    new_df['calendar_date'] = new_df['date'].dt.date
    new_df['day_of_week'] = new_df['date'].dt.dayofweek
    new_df['shooting'] = 0  # set all shooting incidents to 0 as default, which will be overwritten later on should there have been a shooting
    new_df['boro'] = boros[0]   # set all boroughs to the first entry in the list

    # overwrite all entries for the first borough for which there has been a shooting incident at that exact time
    for i in range(len(df)):
        if df['BORO'][i] == boros[0]:
            index_value = new_df[(new_df['calendar_date'] == df['date'][i])].index.values

            new_df.at[index_value[0], 'shooting'] = 1

    boros.pop(0)    # drop the first borough from the list


    # create a new dataframe for the next entry in the list and repeat the steps for the first dataframe
    # once done, concatenate the new dataframe to the first one, this will in the end give a dataframe containing all the dates for every borough
    for i in boros:
        temp_df = pd.DataFrame({'date': []})
        temp_df = temp_df.assign(date=dates)
        temp_df['calendar_date'] = temp_df['date'].dt.date
        temp_df['day_of_week'] = temp_df['date'].dt.dayofweek
        temp_df['shooting'] = 0
        temp_df['boro'] = i
        for j in range(len(df)):
            if df['BORO'][j] == i:
                index_value = temp_df[
                    (temp_df['calendar_date'] == df['date'][j])].index.values

                temp_df.at[index_value[0], 'shooting'] = 1
        frames = [new_df, temp_df]
        new_df = pd.concat(frames)


    new_df.to_csv('NYC_boro_every_day.csv')


# Get a CSV with an entry for date between 2006 and 2019 for each zipcode
def get_every_day_per_zipcode_csv():
    zipcodes = df.Zipcode.unique().tolist()     # find all unique boroughs

    # create a new df with for every date between 2006 and 2019
    dates = pd.date_range(start='2006-01-01', end='2019-12-31', normalize=True).tolist()
    new_df = pd.DataFrame({'date': []})
    new_df = new_df.assign(date=dates)
    new_df['calendar_date'] = new_df['date'].dt.date
    new_df['day_of_week'] = new_df['date'].dt.dayofweek
    new_df['shooting'] = 0  # set all shooting incidents to 0 as default, which will be overwritten later on should there have been a shooting
    new_df['Zipcode'] = 10452   # set all zipcodes to the first entry in the list

    # overwrite all entries for the first zipcode for which there has been a shooting incident at that exact time
    for i in range(len(df)):
        if df['Zipcode'][i] == 10452:
            index_value = new_df[(new_df['calendar_date'] == df['date'][i])].index.values

            new_df.at[index_value[0], 'shooting'] = 1

    zipcodes.pop(0)     # drop the first zipcode from the list

    # create a new dataframe for the next entry in the list and repeat the steps for the first dataframe
    # once done, concatenate the new dataframe to the first one, this will in the end give a dataframe containing all the dates for every zipcode
    for i in zipcodes:
        temp_df = pd.DataFrame({'date': []})
        temp_df = temp_df.assign(date=dates)
        temp_df['calendar_date'] = temp_df['date'].dt.date
        temp_df['day_of_week'] = temp_df['date'].dt.dayofweek
        temp_df['shooting'] = 0
        temp_df['Zipcode'] = i
        for j in range(len(df)):
            if df['Zipcode'][j] == i:
                index_value = temp_df[
                    (temp_df['calendar_date'] == df['date'][j])].index.values

                temp_df.at[index_value[0], 'shooting'] = 1
        frames = [new_df, temp_df]
        new_df = pd.concat(frames)

    new_df.to_csv('NYC_every_day_every_hour.csv')
