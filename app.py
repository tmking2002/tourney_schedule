import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import requests

url = st.text_input('Enter the URL of the tournament:')

if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    division_links = pd.DataFrame()

    teams_df = pd.DataFrame()

    for link in links:
        if ('Division.aspx' in str(link)) and ('division' in link.text.lower()):
            division_link = 'https://tourneymachine.com/Public/Results/' + str(link['href'])
            division_name = link.text
            division_links = pd.concat([division_links, pd.DataFrame([[division_name, division_link]], columns=['Division', 'Link'])])

    if len(division_links) == 0:
        st.markdown('<div style="color: red;">Invalid URL.</div>', unsafe_allow_html=True)
        st.markdown('<div style="color: red;">(Has to be tourneymachine.com/Public/Results/Division.aspx...)</div>', unsafe_allow_html=True)
        st.stop()

    for division, division_link in zip(division_links['Division'], division_links['Link']):
        response = requests.get(division_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            if 'Team.aspx' in str(link):
                team_name = link.text
                teams_df = pd.concat([teams_df, pd.DataFrame([[team_name, division]], columns=['Team', 'Division'])])
                

    st.dataframe(teams_df.reset_index(drop=True), use_container_width=True)