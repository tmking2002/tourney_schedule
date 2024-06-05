import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title('Tournament Schedule')

tourney = st.selectbox('Select Tournament', ['PGF Show Me The Money Showcase'])

if tourney == 'PGF Show Me The Money Showcase':

    data = pd.read_csv('game_info.csv')

    age_group = st.multiselect('Select Age Group', data['Age Group'].unique())

    filtered_data = data[data['Age Group'].isin(age_group)]

    teams = pd.concat([filtered_data['Away'], filtered_data['Home']])
    teams = teams.unique()
    teams = sorted(teams)

    teams = st.multiselect('Select Teams', teams)

    filtered_data = filtered_data[(filtered_data['Away'].isin(teams)) | (filtered_data['Home'].isin(teams))]

    filtered_data['Time'] = pd.to_datetime(filtered_data['Date'] + '/24 ' + filtered_data['Time'])
    filtered_data = filtered_data[filtered_data['Time'] > pd.Timestamp.now()]

    filtered_data = filtered_data[['Age Group', 'Away', 'Home', 'Time', 'Field']]

    filtered_data['Time'] = filtered_data['Time'].dt.strftime('%m/%d/%Y %I:%M %p')
    filtered_data = filtered_data.sort_values(by='Time')

    st.table(filtered_data)