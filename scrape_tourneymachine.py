import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

def scrape_page(xpath, age_group):

    url = 'https://tourneymachine.com/public/mobile/WebApp/index.aspx?IDTournament=h20240522143500344558863d64bd745'

    driver.get(url)

    divisions = driver.find_element(By.XPATH, '//*[@id="menuDivisions"]')
    divisions.click()

    page = driver.find_element(By.XPATH, xpath)
    page.click()

    # get html from page
    html = driver.page_source

    # create soup object
    soup = BeautifulSoup(html, 'html.parser')

    # search for class col-xs-10
    games = soup.find_all('div', class_='col-xs-10')
    times = soup.find_all('div', class_='col-xs-2')
    fields = soup.find_all('div', class_='scheduleLocation')

    # create empty list to store game info
    game_info = pd.DataFrame(columns=['Age Group', 'Game Number', 'Away', 'Home', 'Date', 'Time', 'Field'])

    # loop through games and extract info
    for game, time, field in zip(games, times, fields):
        element_1 = game.find('h5', class_='scheduleTeam1')
        element_2 = game.find('h5', class_='scheduleTeam2')

        game_id = element_1['id']
        game_num = game_id.split('-')[2]

        team_1 = element_1.find('div').text
        team_2 = element_2.find('div').text

        element = time.find('h5')

        date, time = element.get_text(separator='<br>').split('<br>')

        field_element = field.find('p')
        field = field_element.text

        cur_info = pd.DataFrame([[age_group, game_num, team_1, team_2, date, time, field]], columns=['Age Group', 'Game Number', 'Away', 'Home', 'Date', 'Time', 'Field'])

        game_info = pd.concat([game_info, cur_info])

    return game_info

u18 = scrape_page('//*[@id="divisions-team-31"]', 'U18')
u16 = scrape_page('//*[@id="divisions-team-10"]', 'U16')
u14 = scrape_page('//*[@id="divisions-team-1"]', 'U14')

game_info = pd.concat([u18, u16, u14])

game_info.to_csv('game_info.csv', index=False)