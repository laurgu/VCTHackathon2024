import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=90d"

def get_agents(img_tags):
    # Extract agent names from the 'src' attribute
    return [tag['src'].split('/')[-1].replace('.png', '') for tag in img_tags if 'src' in tag.attrs]

def get_stats_data():
    # Make a request to the URL
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Failed to retrieve data from {URL}")
        return  # Return early if the request fails

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    stat_table = soup.find('table', class_='wf-table mod-stats mod-scroll')  

    if stat_table is None:
        print("No table found on the page.")
        return

    # Get the table rows
    rows = stat_table.find_all('tr')

    # Extract headers from the table
    headers = [header.text.strip() for header in stat_table.find_all('th')]

    stats = []

    # Loop through the rows, skipping the header row
    for row in rows[1:]:  # Limit to 2 rows for testing
        columns = row.find_all('td')

        if len(columns) < len(headers):
            continue  # Skip rows with missing data
            
        # Initialize a dictionary for each player's data
        data = {}

        # Extract team acronym
        team_div = columns[0].find('div', class_='stats-player-country')
        team = team_div.text.strip() if team_div else None

        # Skip players with no team for now
        if team is None or "":
            continue

        # Extract data from other columns using headers
        for i, header in enumerate(headers[2:], start=2):
            data[header] = columns[i].text.strip()
        
        # Extract player name
        player_name_div = columns[0].find('div', class_='text-of')
        player_name = player_name_div.text.strip() if player_name_div else "Unknown Player"
        
        # Extract agent images and names
        img_tags = columns[1].find_all('img')
        agents = get_agents(img_tags)

        # Store the special columns and update with the existing data
        data.update({
            'Player': player_name,
            'Agents': agents
        })

        stats.append(data)

    return stats

def save_stats_to_json(stats, filepath):
    # Save the stats to a JSON file at the given filepath
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    stats = get_stats_data()
    filepath = 'Z:/stats_data.json'
    save_stats_to_json(stats, filepath)
