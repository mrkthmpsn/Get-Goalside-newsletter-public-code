import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Scrape Premier League + get team links
FBREF_ROOT = "https://fbref.com"

# epl_fbref_url = FBREF_ROOT + "/en/comps/9/Premier-League-Stats"
epl_fbref_url = FBREF_ROOT + "/en/comps/9/2017-2018/2017-2018-Premier-League-Stats"
epl_tree = requests.get(epl_fbref_url)
epl_soup = BeautifulSoup(epl_tree.content, "html.parser")

epl_table = epl_soup.findAll('table')[2]
epl_rows = epl_table.findAll('tr')
var1 = []
for i in epl_rows[2:]:
    var1.append({'team_name': i.findNext('a').text, 'slug': i.findNext('a').get('href')})

# Scrape team links and get player links
player_fbref_ids = []
its_the_players_here = []
for team_var in var1:
    team_url = FBREF_ROOT + team_var['slug']

    team_tree = requests.get(team_url)
    team_soup = BeautifulSoup(team_tree.content, "html.parser")

    team_table = team_soup.findChild('table')
    team_rows = team_table.findAll('tr')[2:-2]

    for player_row in team_rows:
        player_link = player_row.find('th').find('a')
        player_fbref_id = player_row.find('th')['data-append-csv']
        if player_fbref_id not in player_fbref_ids:
            its_the_players_here.append(
                {
                    "player_name": player_link.text,
                    "player_slug": player_link['href'],
                    "team_name": team_var['team_name'],
                    "player_fbref_id": player_fbref_id
                }
            )

    print(f"{team_var['team_name']} IS DONE")
    time.sleep(3.14)

# Turn the list of players into a csv to store and go back to later
players_team_df = pd.DataFrame(its_the_players_here)
players_team_df.to_csv('./epl_championship_relationship/epl_1718_players_2023_01_08.csv', index=False)

# Second step
players_team_df = pd.read_csv('./epl_championship_relationship/epl_2223_players_2023_01_07.csv')

player_team_seasons_df = pd.DataFrame(
    columns=["player_name", "team_name", "current_season_minutes", "season_year", "season_age", "season_team",
             "season_division", "season_div_level",
             "season_minutes"])


def get_100_rows(player_team_seasons_df, players_team_df_section):
    for _, player_row in players_team_df_section.iterrows():
        # Scrape players to get information
        player_url = FBREF_ROOT + player_row['player_slug']
        player_tree = requests.get(player_url)
        player_soup = BeautifulSoup(player_tree.content, "html.parser")

        player_table = player_soup.find('table', {"id": "stats_standard_dom_lg"})
        if player_table is None:
            continue
        player_rows = player_table.findAll('tr', {"id": "stats"})

        player_seasons = []

        # What do I want from the players?
        # I want their previous clubs, league, age, and minutes played
        # That should give me some data on who came through
        # Each row in an eventual df would have the player info, their current team, and their info each season
        for season_row in player_rows:
            season_year = int(season_row.find("th").text[0:4])
            season_age = season_row.find("td", {"data-stat": "age"}).text
            if season_age == '':
                continue
            season_age = int(season_age)
            season_team = season_row.find("td", {"data-stat": "team"}).text
            season_division = season_row.find("td", {"data-stat": "comp_level"}).find("a").text
            season_div_level = season_row.find("td", {"data-stat": "comp_level"}).find("span").text[0]
            if season_div_level == "J":
                continue
            season_div_level = int(season_div_level)
            season_minutes = season_row.find("td", {"data-stat": "minutes"})
            season_minutes_gk = season_row.find("td", {"data-stat": "gk_minutes"})
            if (season_minutes is None or season_minutes.text == "") and (
                    season_minutes_gk is None or season_minutes_gk.text == ""):
                season_minutes = 0
            elif season_minutes is not None:
                season_minutes = int(season_minutes.text.replace(",", ""))
            else:
                season_minutes = int(season_minutes_gk.text.replace(",", ""))

            player_seasons.append({"season_year": season_year, "season_age": season_age, "season_team": season_team,
                                   "season_division": season_division, "season_div_level": season_div_level,
                                   "season_minutes": season_minutes})

        player_seasons_df = pd.DataFrame(player_seasons)
        player_seasons_df['player_name'] = player_row['player_name']
        player_seasons_df['team_name'] = player_row['team_name']

        player_current_season_minutes = player_rows[-1].find('td', {'data-stat': 'minutes'})
        player_current_season_minutes_gk = player_rows[-1].find('td', {'data-stat': 'gk_minutes'})
        if (player_current_season_minutes is None or player_current_season_minutes.text == "") and (
                player_current_season_minutes_gk is None or player_current_season_minutes_gk.text == ""):
            player_current_season_minutes = 0
        elif player_current_season_minutes is not None:
            player_current_season_minutes = int(player_current_season_minutes.get('csk', 0))
        else:
            player_current_season_minutes = int(player_current_season_minutes_gk.get('csk', 0))

        player_seasons_df['current_season_minutes'] = player_current_season_minutes

        player_team_seasons_df = pd.concat([player_team_seasons_df, player_seasons_df])
        print(player_row['player_name'], player_row['team_name'])
        time.sleep((random.random()) * 6)

    print("All done!")
    return player_team_seasons_df


# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[0:50])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[50:100])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[100:150])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[150:200])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[200:250])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[250:300])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[300:350])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[350:400])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[400:450])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[450:500])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[500:550])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[550:600])
# player_team_seasons_df = get_100_rows(player_team_seasons_df, players_team_df[600:])

# player_team_seasons_df.to_csv('./epl_championship_relationship/epl_players_all_seasons_2223_2023_01_10.csv', index=False)
