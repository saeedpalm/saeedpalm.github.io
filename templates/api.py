from espn_api.football import League
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ESPNFantasyFootballClient:
    def __init__(self):
        self.league_id = os.environ.get('ESPN_LEAGUE_ID')
        self.swid = os.environ.get('ESPN_SWID')
        self.espn_s2 = os.environ.get('ESPN_S2')
        self.year = datetime.now().year

        if not all([self.league_id, self.swid, self.espn_s2]):
            raise ValueError("Missing required ESPN API credentials")

        try:
            self.league = League(league_id=self.league_id, year=self.year, swid=self.swid, espn_s2=self.espn_s2)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to ESPN API: {str(e)}")

        self.teams = self.league.teams

    def display_teams(self):
        for team in self.teams:
            print(f"Team: {team.team_name}")

# Example usage
if __name__ == "__main__":
    try:
        client = ESPNFantasyFootballClient()
        print("Successfully connected to ESPN API")
        client.display_teams()  # Display the teams after a successful connection
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except ConnectionError as ce:
        print(f"ConnectionError: {ce}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
