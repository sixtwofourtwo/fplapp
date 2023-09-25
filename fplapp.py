# # This Fantasy Premier League project was/is inspired by an article published by Paul Corcoran's on Medium 
# "A data driven approach to become a better FPL manager" - https://blog.devgenius.io/using-data-to-become-a-better-fpl-manager-2c4d178d6107"
# The idea is to scrape data from the Fantasy Premier League API and generate a Streamlit tool to present the data in tabular form

# Use this code to transform the locally-saved CSVs into a StreamLit app 

# Load packages
import streamlit as st
import pandas as pd
from PIL import Image

# Load favicon
im = Image.open("favicon.png")

def read_csv(filename):
    df = pd.read_csv(filename)
    if 'total_points' in df.columns:
        df = df.sort_values(by='total_points', ascending=False)
    return df

# Define the file names
file_names = {
    'Individual Team Data': 'teams.csv',
    'Goalkeepers': 'goalkeepers.csv',
    'Defenders': 'defenders.csv',
    'Midfielders': 'midfielders.csv',
    'Forwards': 'forwards.csv',
}

def app():
    st.set_page_config(page_title='FPL Data App', layout='wide', page_icon=im)
    st.title('2023-24 Fantasy Premier League Data App')
    st.markdown("Use the individual tabs to explore the Fantasy Premier League data - the app data was last updated on 25-09-2023.")
    
    # Create tabs for each file
    tabs = st.tabs(list(file_names.keys()))
    for i, tab_name in enumerate(file_names.keys()):
        with tabs[i]:
            st.title(tab_name)
            df = read_csv(file_names[tab_name])

            # Get the list of columns to display
            columns = st.multiselect('Select columns to display:', list(df.columns), default=list(df.columns))
            # Filter the dataframe to display only the selected columns
            filtered_df = df[columns]

            if tab_name != 'Individual Team Data':
                # Add a text input widget to filter by player name
                player_name = st.text_input('Enter player name:', key=f"{tab_name}_player_name")
                filtered_df1 = filtered_df[filtered_df['player'].str.contains(player_name, case=False)]
            else:
                filtered_df1 = filtered_df

            if tab_name != 'Individual Team Data':
                # Add a text input widget to filter by team name
                team_name = st.text_input('Enter team name:', key=f"{tab_name}_team_name")
                filtered_df2 = filtered_df1[filtered_df1['team'].str.contains(team_name, case=False)]
            else:
                filtered_df2 = filtered_df1

            # Display the filtered dataframe
            st.dataframe(filtered_df2)

if __name__ == '__main__':
    app()
