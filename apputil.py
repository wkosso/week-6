
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Get the API token from the .env file
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]


class Genius:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_artist(self, search_term):
        # Search Genius for the artist name
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        search_response = requests.get(
            "https://api.genius.com/search",
            headers=headers,
            params={"q": search_term}
        )
        search_data = search_response.json()

        # Extract the primary artist ID from the first hit
        first_hit = search_data["response"]["hits"][0]
        artist_id = first_hit["result"]["primary_artist"]["id"]

        # Request information about the artist
        artist_url = f"https://api.genius.com/artists/{artist_id}"
        artist_response = requests.get(
            artist_url,
            headers=headers
        )

        # Return the full JSON response as a dictionary
        return artist_response.json()

    def get_artists(self, search_terms):
        rows = []

        for search_term in search_terms:
            artist_data = self.get_artist(search_term)
            artist = artist_data["response"]["artist"]

            rows.append({
                "search_term": search_term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(
            rows,
            columns=[
                "search_term",
                "artist_name",
                "artist_id",
                "followers_count"
            ]
        )


# Create the Genius object
genius = Genius(access_token=ACCESS_TOKEN)

# Example: retrieve information for four artists
artists_df = genius.get_artists(["Rihanna", "Tycho", "Seal", "U2"])
artists_df
