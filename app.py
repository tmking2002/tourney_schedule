import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title('Tournament Schedule')

tourney = st.sidebar.selectbox('Select Tournament', ['PGF Show Me The Money Showcase'])

if tourney == 'PGF Show Me The Money Showcase':

    data = pd.read_csv('game_info.csv')

    default_age_group = ['U16', 'U18']

    age_group = st.sidebar.multiselect('Select Age Group', data['Age Group'].unique(), default=default_age_group)

    filtered_data = data[data['Age Group'].isin(age_group)]

    teams = pd.concat([filtered_data['Away'], filtered_data['Home']])
    teams = teams.unique()
    teams = sorted(teams)

    default_teams = ['Athletics Gold Tamborra-Freeman', 'Atlanta Vipers 07- Maldonado', 'Birmingham Thunderbolts Premier 2025 Kemp', 'D1vision Softball 16U National', 
                     'EC Bullets 18U Gold - Schnute', 'GA Bombers 16U National', 'GA Impact Taylor', 'GA Impact Premier - Maher', 'Impact - Caymol', 'Impact Caymol - Sullivan',
                     'Hotshots National ATL', 'Impact Gold Jazz', 'Nationals - 16U - Sars', 'TAMPA MUSTANGS RENE 18U', 'Tampa Mustangs Seymour', 'Tri-State Thunder Gold',
                     'Team North Carolina Bowman', 'Unity Meadows/Johnson', 'Birmingham Thunderbolts 18 Premier', 'Team NC Baylog / Tracy', 'Unity 16U - Slezak', 
                     'Tennessee Mojo 2025-Gregory']

    teams = st.sidebar.multiselect('Select Teams', teams, default=default_teams)

    filtered_data = filtered_data[(filtered_data['Away'].isin(teams)) | (filtered_data['Home'].isin(teams))]

    filtered_data['Time'] = pd.to_datetime(filtered_data['Date'] + '/24 ' + filtered_data['Time'])
    filtered_data = filtered_data[filtered_data['Time'] > pd.Timestamp.now()]

    date_times = filtered_data['Time'].unique()
    date_times = ["All"] + list(date_times)  # Add "All" to the list of options

    # Display the multiselect widget
    selected_date_times = st.sidebar.multiselect('Select Date/Time', date_times, default=["All"])

    # Check if "All" is selected
    if "All" in selected_date_times:
        # If "All" is selected, show all date/times
        filtered_data = filtered_data
    else:
        # Otherwise, filter the DataFrame based on selected date/times
        filtered_data = filtered_data[filtered_data['Time'].isin(selected_date_times)]

    filtered_data = filtered_data[['Home', 'Away', 'Time', 'Field']]

    filtered_data['Time'] = filtered_data['Time'].dt.strftime('%m/%d/%Y %I:%M %p')
    filtered_data = filtered_data.sort_values(by='Time').drop_duplicates()

    st.write(
        """
        <style>
        table {
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Function to apply bold formatting to selected teams
    def apply_formatting(team, selected_teams):
        return team if team not in selected_teams else f"<b>{team}</b>"

    # Apply formatting to 'Home' and 'Away' columns
    filtered_data['Home'] = filtered_data['Home'].apply(lambda x: apply_formatting(x, teams))
    filtered_data['Away'] = filtered_data['Away'].apply(lambda x: apply_formatting(x, teams))

    st.write(filtered_data.to_html(escape=False), unsafe_allow_html=True)