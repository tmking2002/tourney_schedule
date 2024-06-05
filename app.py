import streamlit as st
import pandas as pd
import plotly.graph_objects as go

tourney = st.selectbox('Select Tournament', ['PGF Show Me The Money Showcase'])



if tourney == 'PGF Show Me The Money Showcase':

    data = pd.read_csv('game_info.csv')

    age_group = st.multiselect('Select Age Group', data['Age Group'].unique())

    filtered_data = data[data['Age Group'].isin(age_group)]

    teams = pd.concat([filtered_data['Away'], filtered_data['Home']])
    teams = teams.unique()
    teams = sorted(teams)

    teams = st.multiselect('Select Team', teams)

    filtered_data = filtered_data[(filtered_data['Away'].isin(teams)) | (filtered_data['Home'].isin(teams))]
    filtered_data['Time'] = pd.to_datetime(filtered_data['Date'] + '/24 ' + filtered_data['Time'])
    filtered_data = filtered_data[['Age Group', 'Away', 'Home', 'Time', 'Field']]

    filtered_data['Time'] = filtered_data['Time'].dt.strftime('%m/%d/%Y %I:%M %p')
    filtered_data = filtered_data.sort_values(by='Time')

    if not filtered_data.empty:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(filtered_data.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[filtered_data[col] for col in filtered_data.columns],
                    fill_color='white',
                    align='left'))
        ])
        
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected filters.")