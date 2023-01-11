import pandas as pd

player_seasons_df_2223 = pd.read_csv('./epl_championship_relationship/epl_players_all_seasons_2223_2023_01_10.csv')
player_seasons_df_2223 = player_seasons_df_2223[player_seasons_df_2223['season_year']<2022]
player_seasons_df_1718 = pd.read_csv('./epl_championship_relationship/epl_players_all_seasons_1718_2023_01_10.csv')
player_seasons_df_1718 = player_seasons_df_1718[player_seasons_df_1718['season_year']<2017]

# Terrific. Realised that I screwed up the 'current season minutes' and it's not an _easy_ fix;
# Players on loan in the current season will have their loan minutes set as their current season minutes
# because it's the last row in their player table. This probably isn't enough to seriously skew
# the analysis but it's enough to be worth an asterisk.


# NB: This figure might be incorrect tbh, it's going purely on the name so if FBref calls two things 'First Division'
# then it'll only show up once
num_divisions = player_seasons_df_2223['season_division'].unique()

# Let's say that, for the current season, I'm only interested in players who've played 5 full games (450 minutes)
# I think this makes sense because players who aren't playing aren't really active players and might be very old
relevant_players_df_2223 = player_seasons_df_2223.copy()
relevant_players_df_2223 = relevant_players_df_2223[relevant_players_df_2223['current_season_minutes'] >= 450]
# Number of players: 326

# Previous seasons, no filters
overall_player_seasons_2223 = (
    relevant_players_df_2223
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
# Rest of Big Five (580), EFL pyramid (535)

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
# Rest of Big Five (946,585), EFL pyramid (1,003,789)

# Filter 1 will be players on teams who aren't newly-promoted, i.e. not Bournemouth, Fulham, or Forest
filter1_df_2223 = relevant_players_df_2223.copy()
filter1_df_2223 = filter1_df_2223[~(filter1_df_2223['team_name'].isin(["Fulham", "Bournemouth", "Nott'ham Forest"]))]

# Previous seasons, no newly-promoted teams
filter1_player_seasons_2223 = (
    filter1_df_2223
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
# Rest of Big Five (845,498), EFL pyramid (681,432)


# 2017/18 players
# Let's say that, for the current season, I'm only interested in players who've played 10 full games (900 minutes)
relevant_players_df_1718 = player_seasons_df_1718.copy()
relevant_players_df_1718 = relevant_players_df_1718[relevant_players_df_1718['current_season_minutes'] >= 450]
# Number of players: 365

# Previous seasons, no filters
overall_player_seasons_1718 = (
    relevant_players_df_1718
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
# Rest of Big Five (516), EFL pyramid (731)

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
# Rest of Big Five (855,035), EFL pyramid (1,321,573)

# Filter 1 will be players on teams who aren't newly-promoted, i.e. not Bournemouth, Fulham, or Forest
filter1_df_1718 = relevant_players_df_1718.copy()
filter1_df_1718 = filter1_df_1718[~(filter1_df_1718['team_name'].isin(["Newcastle Utd", "Huddersfield", "Brighton"]))]

# Previous seasons, no newly-promoted teams
filter1_player_seasons_1718 = (
    filter1_df_1718
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
# Rest of Big Five (768,877), EFL pyramid (1,071,369)
