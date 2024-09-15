import requests
import json
import gzip
import shutil
import time
import os
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

# (game-changers, vct-international, vct-challengers)
LEAGUE = "vct-international"

# (2022, 2023, 2024)
YEAR = 2022

BASE_DIRECTORY = "Z:/"

def download_gzip_and_write_to_json(file_name, local_file_path):
    if os.path.isfile(f"{local_file_path}.json"):
        print(f"{local_file_path}.json already exists, skipping download.")
        return False

    # Construct the remote URL (S3 path)
    remote_file = f"{S3_BUCKET_URL}/{file_name}.json.gz"
    print(f"Attempting to download: {remote_file}")  # Log the correct URL

    response = requests.get(remote_file, stream=True)

    # Log the status code for debugging
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)

        # Check if the response content is empty
        if not gzip_bytes.getbuffer().nbytes:
            print(f"No content found for {file_name}.json.gz, skipping.")
            return False

        # Write the file to the local Z: drive
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            with open(f"{local_file_path}.json", 'wb') as output_file:
                shutil.copyfileobj(gzipped_file, output_file)
            print(f"{local_file_path}.json written successfully.")
        return True
    elif response.status_code == 404:
        print(f"File {file_name}.json.gz not found on server (404).")
        return False
    else:
        print(f"Failed to download {file_name}.json.gz, Status Code: {response.status_code}")
        return False


def download_esports_files():
    directory = f"{BASE_DIRECTORY}/{LEAGUE}/esports-data"

    if not os.path.exists(directory):
        os.makedirs(directory)

    esports_data_files = ["leagues", "tournaments", "players", "teams", "mapping_data"]
    
    for file_name in esports_data_files:
        # Remote file name for S3
        remote_file_name = f"{LEAGUE}/esports-data/{file_name}"

        # Local file path where it will be saved
        local_file_path = f"{directory}/{file_name}"

        result = download_gzip_and_write_to_json(remote_file_name, local_file_path)
        if not result:
            print(f"Skipping {file_name}, unable to download or already exists.")


def download_games():
    start_time = time.time()

    # Path to the local mapping file on the Z: drive
    local_mapping_file = f"{BASE_DIRECTORY}/{LEAGUE}/esports-data/mapping_data.json"
    
    # Load the mapping data
    with open(local_mapping_file, "r") as json_file:
        mappings_data = json.load(json_file)

    # Directory for games data
    local_directory = f"{BASE_DIRECTORY}/{LEAGUE}/games/{YEAR}"
    
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    game_counter = 0

    # Loop through each game in the mapping data
    for esports_game in mappings_data:
        platform_game_id = esports_game["platformGameId"]

        # S3 path for the game file
        s3_game_file = f"{LEAGUE}/games/{YEAR}/{platform_game_id}"

        # Local path to save the game file on Z:
        local_game_file = f"{local_directory}/{platform_game_id.replace(':', '_')}"

        print("Local game file: " + local_game_file + "\n")

        response = download_gzip_and_write_to_json(s3_game_file, local_game_file)
        
        if response:
            game_counter += 1
            if game_counter % 10 == 0:
                print(f"----- Processed {game_counter} games, current run time: {round((time.time() - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    download_esports_files()
    download_games()

    print("DONE!!! FINALLY!!!")