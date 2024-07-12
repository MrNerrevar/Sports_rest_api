from sanic import response
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
        with urllib.request.urlopen(url) as result:
            data = json.loads(result.read().decode())
            if data and data.get('teams'):
                return data.get('teams')[0].get('strLogo')
    except Exception as e:
        print(f"Error fetching logo for {team_name}: {e}")
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


def stitch_logos(name: str, fetch=fetch_logos) -> str | None:
    try:
        team_1, team_2 = name.split(' vs ')
    except ValueError:
        return None

    logo_1 = fetch(team_1)
    logo_2 = fetch(team_2)
    logos = f"{logo_1}|{logo_2}" if logo_1 or logo_2 else None
    return logos


def error_response(message):
    return response.json({'error_message': message}, status=404)


def list_response(rows):
    return response.json([dict(row) for row in rows], status=200)


def update_response(response_id):
    return response.json({'id': response_id}, status=200)


def create_response(response_id):
    return response.json({'id': response_id}, status=201)
