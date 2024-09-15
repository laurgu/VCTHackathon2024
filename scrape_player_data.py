import requests
from bs4 import BeautifulSoup

def search_player(player_name):
    # Convert player_name to lowercase for matching
    player_name_lower = player_name.lower()
    
    # Search URL for the player
    search_url = f"https://www.vlr.gg/search/?q={player_name}"
    
    # Send a GET request to the search page
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to search for {player_name}")
        return None
    
    # Parse the HTML content of the search page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links in the search results
    links = soup.find_all('a', class_=lambda x: x and 'wf-module-item' in x and 'search-item' in x, href=True)
    
    # Filter to find the correct link
    for link in links:

        href = link['href']
        if href.count('/') > 0:
            start = href.rfind('/')
            url_player_name = href[start+1:]
            print(url_player_name)
            if url_player_name == player_name_lower:
                player_url = "https://www.vlr.gg" + href
                return player_url
    
    print(f"Player {player_name} not found in search results.")
    return None

def get_player_agent_data(player_url, timespan="90"):

    url = f"{player_url}/?timespan={timespan}d"
    # Send a GET request to the player's page
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    else:
        print("successfully found player page")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    agent_table = soup.find('table', class_='wf-table')  
    
    if not agent_table:
        print("Agent data not found on the player's page.")
        return None
    
        # Extract table rows
    rows = agent_table.find_all('tr')

    # Extract column headers from the first row
    headers = [header.text.strip() for header in agent_table.find_all('th')]

    # List to hold the data
    agent_data = []

    for row in rows[1:]:
        columns = row.find_all('td')

        # Ensure there are enough columns before processing
        if len(columns) < len(headers):
            continue

        # Extract agent name from image in the first column
        img_tag = columns[0].find('img')
        agent_name = img_tag['src'].split('/')[-1].replace('.png', '') if img_tag and 'src' in img_tag.attrs else "unknown"

        # Extract other data using headers
        data = {
            'Agent': agent_name,
        }
        
        for i, header in enumerate(headers[1:], start=1):
            data[header] = columns[i].text.strip()
        
        agent_data.append(data)

    return agent_data
   

player_name = 'tenz'

player_url = search_player(player_name)

if player_url:
    agent_data = get_player_agent_data(player_url)

    if agent_data:
        print(f"Agent Data for {player_name}:")
        for agent in agent_data:
            print(agent)


