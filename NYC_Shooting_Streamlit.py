import altair as alt
import folium
import streamlit as st

from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

alt.themes.enable("streamlit")

st.set_page_config(layout="centered", page_title="A wicked challenge - NYC Shooting Incidences", page_icon=":statue_of_liberty:")

st.write("""
# NYC Shooting Incidences - A Wicked Challenge  
### Stefanie Bienert | Christopher Patzanovsky
""")

df = pd.read_csv('NYC_full_with_data.csv')
df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'])
df['date'] = df['OCCUR_DATE'].dt.date
df['hour'] = df['OCCUR_TIME'].dt.hour
df.sort_values(by='OCCUR_DATE', inplace=True)

df.drop_duplicates(inplace=True, keep='first')
df.drop(df[(df['Zipcode'] == 0)].index, inplace=True)
#df.drop(df[(df['OCCUR_DATE'].dt.year == 2020) | (df['OCCUR_DATE'].dt.year == 2021)].index, inplace=True)
#df.drop(df[(df['OCCUR_DATE'].dt.year != 2006)].index, inplace=True)
df.drop_duplicates(subset="INCIDENT_KEY", keep='first', inplace=True)
df = df.reset_index(drop=True)
df = df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

midpoint = (np.average(df['latitude']), np.average(df['longitude']))

tab3, tab4, tab5, tab6, tab7 = st.tabs(['Shootings per year', 'Shootings per month', 'Shootings per day of the week', 'Shootings per hour', 'Shootings per minute'])

tab8, tab9, tab10 = st.tabs(['Temperature vs Shootings', 'Rainfall vs Shootings', 'Snowfall vs Shootings'])

tab1, tab2 = st.tabs(['Shootings per Borough', 'Fatal/Non-fatal shootings'])

with tab3:
    df_year = df.copy()
    region_options3 = df_year['BORO'].unique().tolist()
    region3 = st.multiselect('Select Region', region_options3, ['MANHATTAN'], key=30)
    df_year = df_year[df_year['BORO'].isin(region3)]
    df_year = df_year.rename(columns={'OCCUR_DATE': 'Year'})
    year_crosstab = pd.crosstab(df_year['Year'].dt.year, df_year['BORO'])

    fig3 = px.line(year_crosstab)
    st.write(fig3)

with tab4:
    df_month = df.copy()
    year_options4 = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    #year4 = st.selectbox('Select Year', year_options4, 0, key=40)
    year4 = st.slider('Select Year', 2006, 2021, 2021, key=40)

    region_options4 = df_month['BORO'].unique().tolist()
    region4 = st.multiselect('Select Region', region_options4, ['MANHATTAN'], key=41)
    df_month = df_month[df_month['BORO'].isin(region4)]
    df_month = df_month[df_month['OCCUR_DATE'].dt.year == year4]
    df_month['Month'] = df_month['OCCUR_DATE'].dt.month
    df_month = df_month.sort_values('Month')
    df_month['Month'] = df_month['Month'].replace(1, 'JAN')
    df_month['Month'] = df_month['Month'].replace(2, 'FEB')
    df_month['Month'] = df_month['Month'].replace(3, 'MAR')
    df_month['Month'] = df_month['Month'].replace(4, 'APR')
    df_month['Month'] = df_month['Month'].replace(5, 'MAY')
    df_month['Month'] = df_month['Month'].replace(6, 'JUN')
    df_month['Month'] = df_month['Month'].replace(7, 'JUL')
    df_month['Month'] = df_month['Month'].replace(8, 'AUG')
    df_month['Month'] = df_month['Month'].replace(9, 'SEP')
    df_month['Month'] = df_month['Month'].replace(10, 'OCT')
    df_month['Month'] = df_month['Month'].replace(11, 'NOV')
    df_month['Month'] = df_month['Month'].replace(12, 'DEC')
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    #df_month = df_month.rename(columns={'OCCUR_DATE': 'Month'})
    month_crosstab = pd.crosstab(df_month['Month'], df_month['BORO'])
    month_crosstab = month_crosstab.reindex(months, axis="rows")
    fig4 = px.line(month_crosstab)
    st.write(fig4)


with tab5:
    df_day = df.copy()
    region_options5 = df_day['BORO'].unique().tolist()
    region5 = st.multiselect('Select Region', region_options5, ['MANHATTAN'], key=50)
    df_day['OCCUR_TIME'] = pd.to_datetime(df_day['OCCUR_TIME'])
    df_day['OCCUR_DATE'] = pd.to_datetime(df_day['OCCUR_DATE'])
    df_day['Day of the week'] = df_day['OCCUR_DATE'].dt.dayofweek
    df_day = df_day.sort_values('Day of the week')
    df_day['Day of the week'] = df_day['Day of the week'].replace(0, 'MON')
    df_day['Day of the week'] = df_day['Day of the week'].replace(1, 'TUE')
    df_day['Day of the week'] = df_day['Day of the week'].replace(2, 'WED')
    df_day['Day of the week'] = df_day['Day of the week'].replace(3, 'THU')
    df_day['Day of the week'] = df_day['Day of the week'].replace(4, 'FRI')
    df_day['Day of the week'] = df_day['Day of the week'].replace(5, 'SAT')
    df_day['Day of the week'] = df_day['Day of the week'].replace(6, 'SUN')
    df_day = df_day[df_day['BORO'].isin(region5)]
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    weekday_cross_tab = pd.crosstab(df_day['Day of the week'], df_day['BORO'])
    weekday_cross_tab = weekday_cross_tab.reindex(days, axis="rows")


    fig5 = px.line(weekday_cross_tab)
    st.write(fig5)

with tab6:
    df_minute = df.copy()
    region_options6 = df_minute['BORO'].unique().tolist()
    region6 = st.multiselect('Select Region', region_options6, ['MANHATTAN'], key=60)
    df_minute['OCCUR_TIME'] = pd.to_datetime(df_minute['OCCUR_TIME'])
    df_minute = df_minute[df_minute['BORO'].isin(region6)]
    minute_crosstab = pd.crosstab(df_minute['OCCUR_TIME'].dt.hour, df_minute['BORO'])
    fig6 = px.line(minute_crosstab)
    st.write(fig6)

with tab7:
    df_hour = df.copy()

    #year_options4 = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    #year4 = st.selectbox('Select Year', year_options4, 0, key=60)

    year_display7 = (
    "All", '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021')
    year_options7 = list(range(len(year_display7)))
    year_value7 = st.selectbox("Select Year", year_options7, format_func=lambda x: year_display7[x], key=70)

    if year_value7 == 0:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year != 3000]
    if year_value7 == 1:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2006]
    if year_value7 == 2:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2007]
    if year_value7 == 3:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2008]
    if year_value7 == 4:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2009]
    if year_value7 == 5:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2010]
    if year_value7 == 6:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2011]
    if year_value7 == 7:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2012]
    if year_value7 == 8:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2013]
    if year_value7 == 9:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2014]
    if year_value7 == 10:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2015]
    if year_value7 == 11:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2016]
    if year_value7 == 12:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2017]
    if year_value7 == 13:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2018]
    if year_value7 == 14:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2019]
    if year_value7 == 15:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2020]
    if year_value7 == 16:
        df_hour = df_hour[df_hour['OCCUR_DATE'].dt.year == 2021]

    region_options7 = df_hour['BORO'].unique().tolist()
    region7 = st.selectbox('Select Region', region_options7, 0, key=71)

    df_hour['OCCUR_TIME'] = pd.to_datetime(df_hour['OCCUR_TIME'])
    #df_hour = df_hour[df_hour['BORO'].isin(region7)]
    df_hour = df_hour[df_hour['BORO'] == region7]
    hour_cross_tab = pd.crosstab(df_hour['OCCUR_TIME'], df_hour['BORO'])

    fig7 = px.bar(hour_cross_tab)
    st.write(fig7)

with tab8:
    df_temp = df.copy()
    region_options8 = df_temp['BORO'].unique().tolist()
    region8 = st.selectbox('Select Region', region_options8, 0, key=80)
    df_temp = df_temp[df_temp['BORO'] == region8]
    temp_crosstab = pd.crosstab(df_temp['TEMP'], df_temp['BORO'])
    fig8 = px.bar(temp_crosstab)
    st.write(fig8)

with tab9:
    df_rain = df.copy()
    region_options9 = df_rain['BORO'].unique().tolist()
    region9 = st.selectbox('Select Region', region_options9, 0, key=90)
    df_rain = df_rain[df_rain['BORO'] == region9]
    rain_crosstab = pd.crosstab(df_rain['PRCP'], df_rain['BORO'])
    fig9 = px.bar(rain_crosstab)
    st.write(fig9)

with tab10:
    df_snow = df.copy()
    region_options10 = df_snow['BORO'].unique().tolist()
    region10 = st.selectbox('Select Region', region_options10, 0, key=100)
    df_snow = df_snow[df_snow['BORO'] == region10]
    snow_crosstab = pd.crosstab(df_snow['SNOW'], df_snow['BORO'])
    fig10 = px.bar(snow_crosstab)
    st.write(fig10)



with tab1:

    year_options = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    year = st.selectbox('Select Year', year_options, 0)
    #df = df[df['OCCUR_DATE'].dt.year == year]




    month_display = ("All", "January", 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month_options = list(range(len(month_display)))
    month_value = st.selectbox("Select Month", month_options, format_func=lambda x: month_display[x], key=2)


    #region_options = df['BORO'].unique().tolist()
    #region = st.multiselect('Select Region', region_options, ['MANHATTAN'])
    #df = df[df['BORO'].isin(region)]
    df_manhattan = df.copy()
    df_manhattan.drop(df_manhattan[(df_manhattan['BORO'] != 'MANHATTAN')].index, inplace=True)
    df_queens = df.copy()
    df_queens.drop(df_queens[(df_queens['BORO'] != 'QUEENS')].index, inplace=True)
    df_bronx = df.copy()
    df_bronx.drop(df_bronx[(df_bronx['BORO'] != 'BRONX')].index, inplace=True)
    df_brooklyn = df.copy()
    df_brooklyn.drop(df_brooklyn[(df_brooklyn['BORO'] != 'BROOKLYN')].index, inplace=True)
    df_staten = df.copy()
    df_staten.drop(df_staten[(df_staten['BORO'] != 'STATEN ISLAND')].index, inplace=True)

    df_manhattan = df_manhattan[df_manhattan['OCCUR_DATE'].dt.year == year]
    df_queens = df_queens[df_queens['OCCUR_DATE'].dt.year == year]
    df_bronx = df_bronx[df_bronx['OCCUR_DATE'].dt.year == year]
    df_brooklyn = df_brooklyn[df_brooklyn['OCCUR_DATE'].dt.year == year]
    df_staten = df_staten[df_staten['OCCUR_DATE'].dt.year == year]

    if month_value == 0:
        df_manhattan = df_manhattan[df_manhattan['OCCUR_DATE'].dt.month != 13]
        df_queens = df_queens[df_queens['OCCUR_DATE'].dt.month != 13]
        df_bronx = df_bronx[df_bronx['OCCUR_DATE'].dt.month != 13]
        df_brooklyn = df_brooklyn[df_brooklyn['OCCUR_DATE'].dt.month != 13]
        df_staten = df_staten[df_staten['OCCUR_DATE'].dt.month != 13]
    else:
        df_manhattan = df_manhattan[df_manhattan['OCCUR_DATE'].dt.month == month_value]
        df_queens = df_queens[df_queens['OCCUR_DATE'].dt.month == month_value]
        df_bronx = df_bronx[df_bronx['OCCUR_DATE'].dt.month == month_value]
        df_brooklyn = df_brooklyn[df_brooklyn['OCCUR_DATE'].dt.month == month_value]
        df_staten = df_staten[df_staten['OCCUR_DATE'].dt.month == month_value]





    map_fs1 = folium.Map(location=midpoint, zoom_start=10)

    df_manhattan.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='red', fill=True,
                                       fill_opacity=0.8).add_to(map_fs1), axis=1)

    df_queens.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='blue', fill=True,
                                       fill_opacity=0.8).add_to(map_fs1), axis=1)

    df_bronx.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='green', fill=True,
                                       fill_opacity=0.8).add_to(map_fs1), axis=1)

    df_brooklyn.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='purple', fill=True,
                                       fill_opacity=0.8).add_to(map_fs1), axis=1)

    df_staten.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='black', fill=True,
                                       fill_opacity=0.8).add_to(map_fs1), axis=1)


    st_data = st_folium(map_fs1, width=732)

with tab2:

    df_nonfatal = df.copy()
    df_nonfatal.drop(df_nonfatal[(df_nonfatal['STATISTICAL_MURDER_FLAG'] == True)].index, inplace=True)

    df_fatal = df.copy()
    df_fatal.drop(df_fatal[(df_fatal['STATISTICAL_MURDER_FLAG'] == False)].index, inplace=True)


    year_options2 = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    year2 = st.selectbox('Select Year', year_options2, 0, key=3)


    month_display2 = ("All", "January", 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    month_options2 = list(range(len(month_display2)))
    month_value2 = st.selectbox("Select Month", month_options2, format_func=lambda x: month_display2[x], key=4)

    df_nonfatal = df_nonfatal[df_nonfatal['OCCUR_DATE'].dt.year == year2]
    df_fatal = df_fatal[df_fatal['OCCUR_DATE'].dt.year == year2]


    if month_value2 == 0:
        df_nonfatal = df_nonfatal[df_nonfatal['OCCUR_DATE'].dt.month != 13]
        df_fatal = df_fatal[df_fatal['OCCUR_DATE'].dt.month != 13]
    else:
        df_nonfatal = df_nonfatal[df_nonfatal['OCCUR_DATE'].dt.month == month_value2]
        df_fatal = df_fatal[df_fatal['OCCUR_DATE'].dt.month == month_value2]


    map_fs2 = folium.Map(location=midpoint, zoom_start=10)

    df_nonfatal.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='blue', fill=True,
                                       fill_opacity=0.8).add_to(map_fs2), axis=1)

    df_fatal.apply(lambda row: folium.Circle(location=[row["latitude"], row["longitude"]],
                                       radius=100, color='red', fill=True,
                                       fill_opacity=0.8).add_to(map_fs2), axis=1)



    st_data = st_folium(map_fs2, width=725)