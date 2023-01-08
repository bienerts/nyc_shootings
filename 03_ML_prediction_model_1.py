import pandas as pd
from sklearn.tree import DecisionTreeClassifier         # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split    # Import train_test_split function
from sklearn import metrics                             # Import scikit-learn metrics module for accuracy calculation
from sklearn.preprocessing import StandardScaler

'''
This file requires data prepared in 02_ML_dataprep_prediction_model.py: 
- NYC_boro_every_day_every_hour.csv to predict probability of shooting certain hour on a certain day of the week in a borough
- NYC_boro_every_day.csv to function to predict probability of shooting on a certain day of the week in a certain borough
- NYC_area_every_day.csv to predict probability of shooting on a certain day of the week in a certain zipcode
'''


# function to predict probability of shooting for a certain hour on a certain day of the week in a certain borough
def get_prob_borough_hour_and_date():
    df = pd.read_csv('NYC_boro_every_day_every_hour.csv')

    features = ['hour', 'day_of_week', 'boro']

    X = df[features]
    X = pd.get_dummies(X)
    y = df['shooting']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = DecisionTreeClassifier()  # Decision Tree was chosen as the best classifier here

    # Train Decision Tree Classifier
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # This shows an example of what could be entered by a user with the probability of a shooting happening as an output
    Xnew = [[3, 0, 0, 1, 0, 0, 0]]
    ynew = clf.predict_proba(Xnew)
    print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))



# function to predict probability of shooting on a certain day of the week in a certain borough
def get_prob_borough_date():
    df = pd.read_csv('NYC_boro_every_day.csv')

    features = ['day_of_week', 'boro']

    X = df[features]
    X = pd.get_dummies(X)
    y = df['shooting']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)
    # print(X_train)
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = DecisionTreeClassifier()  # Decision Tree was chosen as the best classifier here

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # This shows an example of what could be entered by a user with the probability of a shooting happening as an output
    Xnew = [[6, 0, 0, 0, 0, 1]]
    ynew = clf.predict_proba(Xnew)
    print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))


    
# function to predict probability of shooting on a certain day of the week in a certain zipcode
def get_prob_zipcode_date():
    df = pd.read_csv('NYC_area_every_day.csv')

    features = ['day_of_week', 'Zipcode']

    X = df[features]
    X = pd.get_dummies(X)
    y = df['shooting']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)
    # print(X_train)
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = DecisionTreeClassifier()  # Decision Tree was chosen as the best classifier here

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # This shows an example of what could be entered by a user with the probability of a shooting happening as an output
    Xnew = [[5, 10452]]
    ynew = clf.predict_proba(Xnew)
    print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
