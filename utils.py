import builtins
import urllib.request
import urllib.parse
import json


def generate_slug(name):
    return name.lower().replace(" ", "-")


# Method to fetch the logo for teams via the sportsdb search url and querying for the strLogo value
def fetch_logos(team_name: str) -> str:
    base_url = 'https://www.thesportsdb.com/api/v1/json/3/searchteams.php'
    query = urllib.parse.urlencode({'t': team_name})
    url = f"{base_url}?{query}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data and data.get('teams'):
                return data.get('teams')[0].get('strLogo')
    except Exception as e:
        print(f"Error fetching logo for team {team_name}: {e}")
        return ''

    return ''


# Handy method to force correct value types
def as_value(value, wildcard=False):
    match type(value):
        case builtins.bool:
            return "1" if value else "0"
        case builtins.int:
            return f"{value}"
        case builtins.float:
            return f"{value:.2f}"
        case _ if wildcard:
            return f"'%{value}%'"
        case _:
            return f"'{value}'"
