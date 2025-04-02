import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================

data = pd.read_csv('data_premier.csv')  

# Display the first 5 rows
print(data.head())

# Basic statistical summary
print(data.describe())


# =============================================


# Visualize the relationship between goals and assists
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Goals', y='Assists', data=data)
plt.title('Goals vs Assists')
plt.xlabel('Goals')
plt.ylabel('Assists')
plt.show()

# =============================================

selected_columns = ['Goals', 'Assists', 'Penalties scored', 'Appearances', 'Shots']

# Calculate the correlation matrix
correlation_matrix = data[selected_columns].corr()

# Visualize the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
            linewidths=0.5, cbar_kws={"shrink": .8}, annot_kws={"size": 10})

plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(rotation=0, fontsize=12)

plt.title('Correlation Matrix', fontsize=16)
plt.show()

# =============================================

# Visualize the distribution of the 'Goals' variable
plt.figure(figsize=(10, 6))

sns.histplot(data['Goals'], kde=True, color='blue', bins=20)

plt.title('Distribution of Goals', fontsize=16)
plt.xlabel('Goals', fontsize=12)
plt.ylabel('Number of Players', fontsize=12)

# Adjust the X and Y axis intervals to increase by 25
plt.xticks(np.arange(0, data['Goals'].max() + 25, 25))  # X axis
plt.yticks(np.arange(0, 501, 25))

plt.show()

# =============================================

print(data['Club'].unique())  # Check the correct names here

# Top 5 strongest teams in the Premier League
top_teams = ['Manchester-United', 'Liverpool', 'Manchester-City', 'Chelsea', 'Arsenal']

# Create visualizations for each team
for team in top_teams:
    
    # Filter players of the team
    team_players = data[data['Club'] == team]
    
    # Skip if the team has no data
    if team_players.empty:
        
        print(f"No player data found for {team}.")
        continue
    
    # Fill NaN values with 0 (if any)
    team_players['Goal + Assist Contribution'] = team_players['Goals'] + team_players['Assists']
    team_players['Goal + Assist Contribution'] = team_players['Goal + Assist Contribution'].fillna(0)
    
    # Get player name, goals, and assists contribution
    team_players_stats = team_players[['Name', 'Goals', 'Assists', 'Goal + Assist Contribution']]
    
    # Sort by goal + assist contribution in descending order
    team_players_stats_sorted = team_players_stats.sort_values(by='Goal + Assist Contribution', ascending=False)
    
    # Top 10 players
    print(f"\n{team} Team - Top 10 Players:")
    print(team_players_stats_sorted.head(10))
    

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Goal + Assist Contribution', y='Name', data=team_players_stats_sorted, palette='viridis')
    
    
    plt.title(f'Top {team} Players by Goal + Assist Contribution', fontsize=16)
    plt.xlabel('Goal + Assist Contribution', fontsize=12)
    plt.ylabel('Player', fontsize=12)
    
    # Increase 10
    max_contribution = team_players_stats_sorted['Goal + Assist Contribution'].max()
    
    if max_contribution < 10:
        max_contribution = 10
    
    plt.xticks(np.arange(0, max_contribution + 10, 10))
    
    
    plt.show()

# =============================================

# Calculate goal + assist contributions for teams
team_stats = []

# List of teams
top_teams = ['Manchester-United', 'Liverpool', 'Manchester-City', 'Chelsea', 'Arsenal']

for team in top_teams:
    
    # Get player data for each team
    team_players = data[data['Club'] == team]
    
    # Skip if the team has no data
    if team_players.empty:
        continue
    
    # Fill NaN values with 0 (if any)
    team_players['Goal + Assist Contribution'] = team_players['Goals'] + team_players['Assists']
    team_players['Goal + Assist Contribution'] = team_players['Goal + Assist Contribution'].fillna(0)
    
    # Calculate average goal + assist contribution
    avg_contribution = team_players['Goal + Assist Contribution'].mean()
    
    # Add average goal and assist contributions
    team_stats.append({'Team': team,
                       'Average Goal + Assist Contribution': avg_contribution,
                       'Average Goals': team_players['Goals'].mean(),
                       'Average Assists': team_players['Assists'].mean()})

# Convert team stats to a DataFrame
team_stats_df = pd.DataFrame(team_stats)

# Comparison of goal + assist contributions between teams
plt.figure(figsize=(10, 6))
sns.barplot(x='Team', y='Average Goal + Assist Contribution', data=team_stats_df)


plt.title('Average Goal + Assist Contribution Comparison Between Teams', fontsize=16)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Average Goal + Assist Contribution', fontsize=12)


plt.show()


team_stats_df.set_index('Team')[['Average Goals', 'Average Assists']].plot(kind='bar', figsize=(10, 6))

plt.title('Average Goals and Assists Comparison Between Teams', fontsize=16)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Average Goals/Assists', fontsize=12)
plt.xticks(rotation=15, ha="right", fontsize=12)
plt.show()

# =============================================

# Calculate goal and assist contributions
data['Goal + Assist Contribution'] = data['Goals'] + data['Assists']


position_stats = data.groupby('Position').agg(
    Average_Goals=('Goals', 'mean'),
    Average_Assists=('Assists', 'mean'),
    Average_Contribution=('Goal + Assist Contribution', 'mean')
).reset_index()

# Goal and assist contributions by position
plt.figure(figsize=(12, 6))

# Show goal and assist contributions 
sns.barplot(x='Position', y='Average_Goals', data=position_stats, color='blue', label='Goals', alpha=0.7)
sns.barplot(x='Position', y='Average_Assists', data=position_stats, color='green', label='Assists', alpha=0.7)


plt.title('Average Goal and Assist Contributions by Position', fontsize=16)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Average Contribution', fontsize=12)
plt.legend(title='Contributions')

plt.show()

# =============================================

# Load Premier League data
data = pd.read_csv('data_premier.csv')

# Check the columns for fouls, yellow cards, and red cards
print(data[['Name', 'Fouls', 'Yellow cards', 'Red cards']].head())

# Top 10 players with most fouls
top_faul_players = data[['Name', 'Fouls', 'Yellow cards', 'Red cards']].sort_values(by='Fouls', ascending=False).head(10)


fig, ax = plt.subplots(figsize=(10, 6))


top_faul_players.set_index('Name')[['Fouls', 'Yellow cards', 'Red cards']].plot(kind='bar', ax=ax, width=0.8)

# Set the Y axis ticks with intervals of 25
plt.yticks(np.arange(0, top_faul_players[['Fouls', 'Yellow cards', 'Red cards']].max().max() + 25, 25))

# Add semi-transparent horizontal lines for every 25 units on the Y axis
for y in np.arange(0, top_faul_players[['Fouls', 'Yellow cards', 'Red cards']].max().max() + 25, 25):
    ax.axhline(y=y, color='gray', linestyle='--', alpha=0.3)


plt.title('Top 10 Players with Most Fouls, Yellow and Red Cards', fontsize=16)
plt.xlabel('Player', fontsize=12)
plt.ylabel('Count', fontsize=12)


plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(fontsize=12)


plt.tight_layout()
plt.show()

# =============================================

# Load Premier League data
data = pd.read_csv('data_premier.csv')

# Check goalkeepers and their save numbers
goalkeepers_data = data[data['Position'] == 'Goalkeeper'][['Name', 'Saves']]


top_10_goalkeepers = goalkeepers_data.sort_values(by='Saves', ascending=False).head(10)

# Top 10 goalkeepers with the most saves
plt.figure(figsize=(20, 8))
plt.barh(top_10_goalkeepers['Name'], top_10_goalkeepers['Saves'], color='skyblue')

# Add transparent lines every 25 intervals on the X-axis
plt.grid(axis='x', color='gray', linestyle='--', alpha=0.3)  # Lines for the X-axis
plt.xticks(np.arange(0, top_10_goalkeepers['Saves'].max() + 25, 25))  # Set X-axis increments by 25


plt.title('Top 10 Goalkeepers with Most Saves in Premier League', fontsize=16)
plt.xlabel('Saves', fontsize=12)
plt.ylabel('Goalkeeper', fontsize=12)


plt.tight_layout()
plt.show()






