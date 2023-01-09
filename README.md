# New York City Shooting Incidents 🗽
Project aiming to shed light on the frequency, location and trend over time of shootings occuring in all 5 NYC boroughs (Bronx, Brooklyn, Manhattan, Queens, Staten Island) from 2006 until 2021.

The project includes:

* Streamlit app [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bienerts-nyc-shootings-nyc-shooting-streamlit-l8l4ml.streamlit.app/)
  * In file [NYC_Shooting_Streamlit.py](NYC_Shooting_Streamlit.py)
  * Uses data from NYC_full_with_data.csv which contains
    * [NYPD Shooting Incident Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8) 
    * Enriched by Zip Codes 
    * Enriched by Weather data
* Prediction models
  * Data preparation for prediction models [02_ML_dataprep_prediction_model.py](02_ML_dataprep_prediction_model.py)
  * Prediction models:
    * Predict probability of shooting certain hour on a certain day of the week in a borough 
    * Predict probability of shooting on a certain day of the week in a certain borough 
    * Predict probability of shooting on a certain day of the week in a certain zipcode
    * File [03_ML_prediction_model_1.py](03_ML_prediction_model_1.py)
  * Prediction Models:
    * File [04_ML_prediction_model_2.py](04_ML_prediction_model_2.py)
