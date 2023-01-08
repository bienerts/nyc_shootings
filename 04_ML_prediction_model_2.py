import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split    # Import train_test_split function
from sklearn import metrics

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

df = pd.read_csv('NYC_full_with_data copy.csv')

df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'])
df['day_of_week'] = df['OCCUR_DATE'].dt.dayofweek
df['month'] = df['OCCUR_DATE'].dt.month
df['hour'] = df['OCCUR_TIME'].dt.hour
df.drop_duplicates(inplace=True)
df.drop(df[(df['Zipcode'] == 0)].index, inplace=True)
df.drop(df[(df['OCCUR_DATE'].dt.year == 2020) | (df['OCCUR_DATE'].dt.year == 2021)].index, inplace=True)
df.drop_duplicates(subset="INCIDENT_KEY", keep='first', inplace=True)
df = df.reset_index(drop=True)



# give categorical features numerical values to help ML algorithm
fatality = {False: 0, True: 1}
df['fatality'] = df['STATISTICAL_MURDER_FLAG'].map(fatality)

age = {'<18': 0, '18-24': 1, '25-44': 2, '45-64': 3, '65+': 4, 'UNKNOWN': 5}
df['victim_age'] = df['VIC_AGE_GROUP'].map(age)

sex = {'M': 0, 'F': 1, 'U': 2}
df['victim_sex'] = df['VIC_SEX'].map(sex)

race = {'BLACK': 0, 'BLACK HISPANIC': 1, 'WHITE HISPANIC': 2, 'ASIAN / PACIFIC ISLANDER': 3, 'WHITE': 4, 'AMERICAN INDIAN/ALASKAN NATIVE': 5, 'UNKNOWN': 6}
df['victim_race'] = df['VIC_RACE'].map(race)

'''
Two types of dataframes are used for ML:
- one with only the entries that contain all the information on the shooter which allows for prediction of the shooter's age, gender and sex
- the complete one, which will be used for all other predictions (e.g. zipcode, borough, etc.)
'''

# Data manipulation to clean dataframe to include only entries with full information on the shooter
df_with_shooter = df.copy()
df_with_shooter = df_with_shooter[df_with_shooter['PERP_AGE_GROUP'].notna()]
df_with_shooter = df_with_shooter[df_with_shooter['PERP_SEX'].notna()]
df_with_shooter = df_with_shooter[df_with_shooter['PERP_RACE'].notna()]
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_AGE_GROUP'] == 'UNKNOWN')].index, inplace=True)
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_AGE_GROUP'] == '224')].index, inplace=True)
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_AGE_GROUP'] == '940')].index, inplace=True)
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_AGE_GROUP'] == '1020')].index, inplace=True)
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_SEX'] == 'U')].index, inplace=True)
df_with_shooter.drop(df_with_shooter[(df_with_shooter['PERP_RACE'] == 'UNKNOWN')].index, inplace=True)
df_with_shooter = df_with_shooter.reset_index(drop=True)
df_with_shooter['shooter_age'] = df_with_shooter['PERP_AGE_GROUP'].map(age)
df_with_shooter['shooter_sex'] = df_with_shooter['PERP_SEX'].map(sex)
df_with_shooter['shooter_race'] = df_with_shooter['PERP_RACE'].map(race)



features_with_shooters = ['day_of_week', 'month', 'hour', 'fatality', 'victim_age', 'victim_sex',
       'shooter_race', 'shooter_age', 'shooter_sex']

features = ['day_of_week', 'month', 'hour', 'fatality', 'victim_age', 'victim_sex', 'BORO']

'''
The following code is an example of how to call the ML prediction. The dataframe can be changed to whichever is wanted. The to-be-predicted feature can be exchanged customly.
Here, both decision tree as well as KNN is used, with multiple iterations being tried to find the best.
'''
X = df[features]
X = pd.get_dummies(X)
y = df['victim_race']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

for i in range(1,8):

    clf = DecisionTreeClassifier(max_depth=i)

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

print("_________")
for j in range(1,31):

    clf2 = KNeighborsClassifier(n_neighbors=j)

    # Train Decision Tree Classifer
    clf2 = clf2.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf2.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
