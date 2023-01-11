import pandas as pd

# I need to define this variable because these are teams that have been in leagues with the same names
# as the ones I'm interested in, but they're not actually the same league. Lotta Scotland, Ukraine, Russia
var_bleh = ["Rapid Wien", "RB Salzburg", "Hibernian", "Alloa Athletic", "Ayr United", "Ufa", "St Mirren", "SK Dnipro-1", "Dynamo Kyiv", "Rubin Kazan", "Zenit", "CSKA Moscow", "Loko Moscow", "Shakhtar", "Anzhi", "Aberdeen", "Zorya Luhansk", "Dundee United", "Hibernian", "Celtic", "Motherwell", "Independiente", "LDU de Quito", "Austria Wien", "Falkirk", "Met Donetsk", "Rangers", "Inverness CT", "Hamilton", "Dundee", "Spartak Moscow", "Gretna", "Rubin Kazan"]

# I have to do this awkward workaround for current season minutes for two reasons
# One is that the old version counted players' 2022/23 loan spells outside the PL as 'current season mins'
# The other is that I was using 'current season' to filter the 2017/18 version, which was stupid
player_seasons_df_2223 = pd.read_csv('./epl_championship_relationship/epl_players_all_seasons_2223_2023_01_10.csv')
current_season_df = player_seasons_df_2223[
    (player_seasons_df_2223['season_year'] == 2022) & (player_seasons_df_2223['season_division'] == "Premier League")][
    ['player_name', 'team_name', 'season_minutes']].rename(columns={"season_minutes": "real_current_season_mins"})
player_seasons_df_2223 = player_seasons_df_2223.merge(current_season_df)
player_seasons_df_2223 = player_seasons_df_2223[player_seasons_df_2223['season_year'] < 2022]

player_seasons_df_1718 = pd.read_csv('./epl_championship_relationship/epl_players_all_seasons_1718_2023_01_10.csv')
current_season_df = player_seasons_df_1718[
    (player_seasons_df_1718['season_year'] == 2017) & (player_seasons_df_1718['season_division'] == "Premier League")][
    ['player_name', 'team_name', 'season_minutes']].rename(columns={"season_minutes": "real_current_season_mins"})
player_seasons_df_1718 = player_seasons_df_1718.merge(current_season_df)
player_seasons_df_1718 = player_seasons_df_1718[player_seasons_df_1718['season_year'] < 2017]

# Let's say that, for the current season, I'm only interested in players who've played 5 full games (450 minutes)
# I think this makes sense because players who aren't playing aren't really active players and might be very old
relevant_players_df_2223 = player_seasons_df_2223.copy()
relevant_players_df_2223 = relevant_players_df_2223[relevant_players_df_2223['real_current_season_mins'] >= 450]
# print("Number of players: ", len(relevant_players_df_2223['player_name'].unique()))
# 295

# Previous seasons, no filters
# Filter out the stupid same-league-name teams
overall_player_seasons_2223 = (
    relevant_players_df_2223[~(relevant_players_df_2223['season_team'].isin(var_bleh))]
    .groupby(['season_division', 'season_div_level'])['season_minutes']
    .agg(['sum', 'count'])
    .sort_values('sum', ascending=False)
)
# Championship is the second-most, but outnumbered by La Liga and Ligue 1 combined.
# And that's _before_ we apply any filtering

# I should come back and look at what Championship+League One+League Two vs Big Five says
overall_pyramid_2223 = (
        overall_player_seasons_2223['count'][('Championship', 2)] +
        overall_player_seasons_2223['count'][('League One', 3)] +
        overall_player_seasons_2223['count'][('League Two', 4)]
)
overall_big_five_2223 = (
        overall_player_seasons_2223['count'][('La Liga', 1)] +
        overall_player_seasons_2223['count'][('Ligue 1', 1)] +
        overall_player_seasons_2223['count'][('Bundesliga', 1)] +
        overall_player_seasons_2223['count'][('Serie A', 1)]
)
# Rest of Big Five (545), EFL pyramid (513)

overall_pyramid_2223_mins = (
        overall_player_seasons_2223['sum'][('Championship', 2)] +
        overall_player_seasons_2223['sum'][('League One', 3)] +
        overall_player_seasons_2223['sum'][('League Two', 4)]
)
overall_big_five_2223_mins = (
        overall_player_seasons_2223['sum'][('La Liga', 1)] +
        overall_player_seasons_2223['sum'][('Ligue 1', 1)] +
        overall_player_seasons_2223['sum'][('Bundesliga', 1)] +
        overall_player_seasons_2223['sum'][('Serie A', 1)]
)
# Rest of Big Five (892,626), EFL pyramid (992,614)

# Filter 1 will be players on teams who aren't newly-promoted, i.e. not Bournemouth, Fulham, or Forest
filter1_df_2223 = relevant_players_df_2223.copy()
filter1_df_2223 = filter1_df_2223[~(filter1_df_2223['team_name'].isin(["Fulham", "Bournemouth", "Nott'ham Forest"]))]

# Previous seasons, no newly-promoted teams
# Filter out the stupid same-league-name teams
filter1_player_seasons_2223 = (
    filter1_df_2223[~(filter1_df_2223['season_team'].isin(var_bleh))]
    .groupby(['season_division', 'season_div_level'])['season_minutes']
    .agg(['sum', 'count'])
    .sort_values('sum', ascending=False)
)
# Championship is still second-most, but this time it's very close to La Liga and easily outnumbered by
# La Liga plus Ligue 1

# I should come back and look at what Championship+League One+League Two vs Big Five says
filter1_pyramid_2223 = (
        filter1_player_seasons_2223['sum'][('Championship', 2)] +
        filter1_player_seasons_2223['sum'][('League One', 3)] +
        filter1_player_seasons_2223['sum'][('League Two', 4)]
)
filter1_big_five_2223 = (
        filter1_player_seasons_2223['sum'][('La Liga', 1)] +
        filter1_player_seasons_2223['sum'][('Ligue 1', 1)] +
        filter1_player_seasons_2223['sum'][('Bundesliga', 1)] +
        filter1_player_seasons_2223['sum'][('Serie A', 1)]
)
# Rest of Big Five (791777), EFL pyramid (675,482)


# 2017/18 players
# Let's say that, for the current season, I'm only interested in players who've played 10 full games (900 minutes)
relevant_players_df_1718 = player_seasons_df_1718.copy()
relevant_players_df_1718 = relevant_players_df_1718[relevant_players_df_1718['real_current_season_mins'] >= 1000]
# print("Number of players: ", len(relevant_players_df_1718['player_name'].unique()))
# 316

# Previous seasons, no filters
# Filter out the stupid same-league-name teams
overall_player_seasons_1718 = (
    relevant_players_df_1718[~(relevant_players_df_1718['season_team'].isin(var_bleh))]
    .groupby(['season_division', 'season_div_level'])['season_minutes']
    .agg(['sum', 'count'])
    .sort_values('sum', ascending=False)
)
# Championship is the second-most, but outnumbered by La Liga and Ligue 1 combined.
# And that's _before_ we apply any filtering

# I should come back and look at what Championship+League One+League Two vs Big Five says
overall_pyramid_1718 = (
        overall_player_seasons_1718['count'][('Championship', 2)] +
        overall_player_seasons_1718['count'][('League One', 3)] +
        overall_player_seasons_1718['count'][('League Two', 4)]
)
overall_big_five_1718 = (
        overall_player_seasons_1718['count'][('La Liga', 1)] +
        overall_player_seasons_1718['count'][('Ligue 1', 1)] +
        overall_player_seasons_1718['count'][('Bundesliga', 1)] +
        overall_player_seasons_1718['count'][('Serie A', 1)]
)
# Rest of Big Five (491), EFL pyramid (646)

overall_pyramid_1718_mins = (
        overall_player_seasons_1718['sum'][('Championship', 2)] +
        overall_player_seasons_1718['sum'][('League One', 3)] +
        overall_player_seasons_1718['sum'][('League Two', 4)]
)
overall_big_five_1718_mins = (
        overall_player_seasons_1718['sum'][('La Liga', 1)] +
        overall_player_seasons_1718['sum'][('Ligue 1', 1)] +
        overall_player_seasons_1718['sum'][('Bundesliga', 1)] +
        overall_player_seasons_1718['sum'][('Serie A', 1)]
)
# Rest of Big Five (834,967), EFL pyramid (1,204,860)

# Filter 1 will be players on teams who aren't newly-promoted, i.e. not Bournemouth, Fulham, or Forest
filter1_df_1718 = relevant_players_df_1718.copy()
filter1_df_1718 = filter1_df_1718[~(filter1_df_1718['team_name'].isin(["Newcastle Utd", "Huddersfield", "Brighton"]))]

# Previous seasons, no newly-promoted teams
# Filter out the stupid same-league-name teams
filter1_player_seasons_1718 = (
    filter1_df_1718[~(filter1_df_1718['season_team'].isin(var_bleh))]
    .groupby(['season_division', 'season_div_level'])['season_minutes']
    .agg(['sum', 'count'])
    .sort_values('sum', ascending=False)
)
# Championship is still second-most, but this time it's very close to La Liga and easily outnumbered by
# La Liga plus Ligue 1

# I should come back and look at what Championship+League One+League Two vs Big Five says
filter1_pyramid_1718 = (
        filter1_player_seasons_1718['sum'][('Championship', 2)] +
        filter1_player_seasons_1718['sum'][('League One', 3)] +
        filter1_player_seasons_1718['sum'][('League Two', 4)]
)
filter1_big_five_1718 = (
        filter1_player_seasons_1718['sum'][('La Liga', 1)] +
        filter1_player_seasons_1718['sum'][('Ligue 1', 1)] +
        filter1_player_seasons_1718['sum'][('Bundesliga', 1)] +
        filter1_player_seasons_1718['sum'][('Serie A', 1)]
)
# Rest of Big Five (759,413), EFL pyramid (910,329)

# Could do percentage of all career minutes of the active players
overall_2223_total_mins = overall_player_seasons_2223['sum'].sum()
filter1_2223_total_mins = filter1_player_seasons_2223['sum'].sum()
overall_1718_total_mins = overall_player_seasons_1718['sum'].sum()
filter1_1718_total_mins = filter1_player_seasons_1718['sum'].sum()

overall_2223_big_five_proportion = overall_big_five_2223_mins / overall_2223_total_mins
overall_2223_pyramid_proportion = overall_pyramid_2223_mins / overall_2223_total_mins

filter1_2223_big_five_proportion = filter1_big_five_2223 / filter1_2223_total_mins
filter1_2223_pyramid_proportion = filter1_pyramid_2223 / filter1_2223_total_mins

overall_1718_big_five_proportion = overall_big_five_1718_mins / overall_1718_total_mins
overall_1718_pyramid_proportion = overall_pyramid_1718_mins / overall_1718_total_mins

filter1_1718_big_five_proportion = filter1_big_five_1718 / filter1_1718_total_mins
filter1_1718_pyramid_proportion = filter1_pyramid_1718 / filter1_1718_total_mins

print(f"""
Overall, the EFL's share of Premier League active players' career minutes has gone from 
{round(overall_1718_pyramid_proportion * 100, 2)}% to {round(overall_2223_pyramid_proportion * 100, 2)}%
while the rest of the European Big Five's share has gone from {round(overall_1718_big_five_proportion * 100, 2)}%
to {round(overall_2223_big_five_proportion * 100, 2)}%  
""")
print(f"""
If you do the same thing but removing newly-promoted teams, the EFL's share has gone from 
{round(filter1_1718_pyramid_proportion * 100, 2)}% to {round(filter1_2223_pyramid_proportion * 100, 2)}%
while the rest of the European Big Five's share has gone from {round(filter1_1718_big_five_proportion * 100, 2)}%
to {round(filter1_2223_big_five_proportion * 100, 2)}% 
""")

# Check whether players have played in Pyramid/Big Five
players_pyramid_2223 = (
    relevant_players_df_2223[
        ~(relevant_players_df_2223['season_team'].isin(var_bleh)) &
        (relevant_players_df_2223['season_division'].isin(['Championship', 'League One', 'League Two']))
    ].groupby(['player_name', 'team_name']).count()
)
# 128
players_pyramid_1718 = (
    relevant_players_df_1718[
        ~(relevant_players_df_1718['season_team'].isin(var_bleh)) &
        (relevant_players_df_1718['season_division'].isin(['Championship', 'League One', 'League Two']))
    ].groupby(['player_name', 'team_name']).count()
)
# 154

players_big_five_2223 = (
    relevant_players_df_2223[
        ~(relevant_players_df_2223['season_team'].isin(var_bleh)) &
        (relevant_players_df_2223['season_division'].isin(['Serie A', 'Bundesliga', 'La Liga', "Ligue 1"]))
    ].groupby(['player_name', 'team_name']).count()
)
# 124
players_big_five_1718 = (
    relevant_players_df_1718[
        ~(relevant_players_df_1718['season_team'].isin(var_bleh)) &
        (relevant_players_df_1718['season_division'].isin(['Serie A', 'Bundesliga', 'La Liga', "Ligue 1"]))
        ].groupby(['player_name', 'team_name']).count()
)
# 115
