import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
# import plotly.graph_objects as go

bat = pd.read_csv("bat.csv")
bowl = pd.read_csv("bowl.csv")
point = {"6s": 2, "50": 8, "100": 16, "200": 32, "Wkts": 25, "4W": 8, "5W": 16, "10W": 32}

match_types = ['IPL', 'ODI', 'T20', 'Test']
teams = [team.title() for team in list(bat['Team'].unique())]
sort_types = ['Batting', 'Bowling', 'Overall']

def make_my_dream11(match_type, team1, team2, batsman, bowlers):
    bat_df = bat[bat['Type'] == match_type]
    bowl_df = bowl[bowl['Type'] == match_type]

    bat_data = bat_df[(bat_df['Team'] == team1) | (bat_df['Team'] == team2)]
    bowl_data = bowl_df[(bowl_df['Team'] == team1) | (bowl_df['Team'] == team2)]

    bat_data = bat_data[['Runs', 'SR', '4s', '6s', '50', '100', '200', 'Player', 'Team']]
    bowl_data = bowl_data[['Wkts', 'Econ', '5W', '10W', 'Player']]

    players = pd.merge(bat_data, bowl_data, how = 'outer', on = 'Player')
    players['Batting Points'] = players['Runs'] + players['4s'] + players['6s']*point['6s'] + players['50']*point['50'] + players['100']*point['100'] + players['200']*point['200']
    players['Bowling Points'] = players['Wkts']*point['Wkts'] + players['5W']*(point['4W'] + point['5W']) + players['10W']*point['10W']

    players['Overall Points'] = players['Batting Points'] + players['Bowling Points']
    df = players[['Player', 'Team', 'Batting Points', 'Bowling Points', 'Overall Points']]
    
    team = pd.DataFrame([], columns = ['Player', 'Team', 'Batting Points', 'Bowling Points', 'Overall Points'])
    count = 1

    bat_rankings = df.sort_values(by = 'Batting Points', ascending = False)
    # taking top 3 batsman on the basis of batting points
    for i in range(batsman):
        name = bat_rankings.iloc[i]['Player']
        team.loc[count] = bat_rankings.iloc[i]
        df.drop(bat_rankings.loc[bat_rankings['Player'] == name].index, inplace = True)
        count += 1

    bowl_rankings = df.sort_values(by = 'Bowling Points', ascending = False)
    # taking top 3 bowlers on the basis of bowling points
    for i in range(bowlers):
        name = bowl_rankings.iloc[i]['Player']
        team.loc[count] = bowl_rankings.iloc[i]
        df.drop(bowl_rankings.loc[bowl_rankings['Player'] == name].index, inplace = True)
        count += 1

    net_rankings = df.sort_values(by = 'Overall Points', ascending = False)
    # taking rest of the players on the basis of Overall points
    for i in range(11 - batsman - bowlers):
        name = net_rankings.iloc[i]['Player']
        team.loc[count] = net_rankings.iloc[i]
        df.drop(net_rankings.loc[net_rankings['Player'] == name].index, inplace = True)
        count += 1

    return team

st.set_page_config(layout = "wide")

col1 = st.sidebar

st.title("Build your Dream 11 - A Data Web App")

details_expander = st.beta_expander("App Details")
details_expander.markdown("""This app performs simple calculations based on the player's past data of batting and bowling
- **Python Libraries:** *pandas, base64, streamlit*
- **Data Source:** [cricbuzz](https://www.cricbuzz.com)
- **Repository:** [GitHub Link](https://github.com/shivanshsinghal107/build-your-dream11)""")

points_expander = st.beta_expander("Points Distribution")
points_expander.markdown("""
- **Runs:** Total Runs Scored (1 Point)
- **SR:** Batting Strike Rate
- **4s:** No. of fours (1 Point)
- **6s:** No. of Sixes (2 Points)
- **50:** No. of Half Centuries (8 Points)
- **100:** No. of Centuries (16 Points)
- **200:** No. of Double Centuries (32 Points)
- **Wkts:** No. of Wickets taken (25 Points)
- **Econ:** Bowler Economy Rate
- **5W:** No. of times bowler took 5 wickets in a single match (8 Points)
- **10W:** No. of times bowler took 10 wickets in a single match (16 Points)
""")

col1.header("User Input Features")
selected_type = col1.selectbox('Match Type', match_types, index = 2)
team1 = col1.selectbox('Team 1', teams)
team2 = col1.selectbox('Team 2', teams[1:], index = 2)
sort_type = col1.selectbox('Sort by', sort_types)
batsman = col1.slider('No. of Batsman', 1, 9, 3)
bowlers = col1.slider('No. of Bowlers', 1, (11-batsman), 2)

col1.write("** Rest of the players will be selected based on their overall performances")

# load data of the team players
def load_data(match_type, team1, team2, sort_type):
    bat_df = bat[bat['Type'] == match_type]
    bowl_df = bowl[bowl['Type'] == match_type]

    bat_data = bat_df[(bat_df['Team'] == team1) | (bat_df['Team'] == team2)]
    bowl_data = bowl_df[(bowl_df['Team'] == team1) | (bowl_df['Team'] == team2)]

    bat_data = bat_data[['Runs', 'SR', '4s', '6s', '50', '100', '200', 'Player', 'Team']]
    bowl_data = bowl_data[['Wkts', 'Econ', '5W', '10W', 'Player']]

    players = pd.merge(bat_data, bowl_data, how = 'outer', on = 'Player')
    players['Batting Points'] = players['Runs'] + players['4s'] + players['6s']*point['6s'] + players['50']*point['50'] + players['100']*point['100'] + players['200']*point['200']
    players['Bowling Points'] = players['Wkts']*point['Wkts'] + players['5W']*(point['4W'] + point['5W']) + players['10W']*point['10W']

    players['Overall Points'] = players['Batting Points'] + players['Bowling Points']
    players = players[['Player', 'Team', 'Runs', 'SR', '4s', '6s', '50', '100', '200', 'Batting Points', 'Wkts', 'Econ', '5W', '10W', 'Bowling Points', 'Overall Points']]
    players = players.sort_values(by = f"{sort_type} Points", ascending = False).reset_index(drop = True)
    
    return players

# players = make_my_dream11(selected_type, team1, team2, batsman, bowlers)
# st.header("DREAM 11")
# players_str = ""
# for i in range(len(players)):
#     if i % 3 == 0 and i > 0:
#         st.write(players_str)
#         players_str = ""
#     players_str += f"{players.iloc[i]['Player']}, "

# st.write(players_str[:-2])

players_stats = load_data(selected_type, team1, team2, sort_type)

st.markdown(f"## **{selected_type} Players Stats of selected Teams**")
st.dataframe(players_stats)

def file_download(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV file</a>'
    return href

st.markdown(file_download(players_stats), unsafe_allow_html = True)

players = make_my_dream11(selected_type, team1, team2, batsman, bowlers)
st.markdown("## **Playing 11 Performance Chart**")

plt.style.use("ggplot")
plt.figure(figsize = (15, 5))
plt.subplots_adjust(top = 1, bottom = 0)
plt.barh(players['Player'], players['Batting Points'], label = 'Batting')
plt.barh(players['Player'], players['Bowling Points'], label = 'Bowling')
plt.legend(loc = 'best')
ax = plt.axes()
ax.invert_yaxis()
st.pyplot(plt)

st.markdown("[GitHub Link](https://github.com/shivanshsinghal107/build-your-dream11)")

# g1 = go.Bar(x = players['Player'], y = players['Batting Points'], name = 'batting')
# g2 = go.Bar(x = players['Player'], y = players['Bowling Points'], name = 'bowling')
# data = [g1, g2]
# layout = go.Layout(barmode = 'group', width = 1500, height = 600)
# fig = go.Figure(data = data, layout = layout)
# st.plotly_chart(fig)