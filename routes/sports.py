from sanic import Blueprint
from sanic.request import Request
from db import db_get_all_entries, db_add_sport, db_update, db_search
from models import Sport
from utils import generate_slug, error_response, list_response, update_response, create_response

sport_bp = Blueprint('sports', url_prefix='/sport')


# unnecessary, but lists all sports
@sport_bp.route('/', methods=['GET'])
async def get_sports(request: Request):
    sports = db_get_all_entries('sports')
    return list_response(sports)


@sport_bp.route('/', methods=['POST'])
async def add_sport(request: Request):
    data = request.json
    slug = generate_slug(data['Name'])
    active = False  #Set sport to inactive by default
    sport = Sport(
        Name=data['Name'],
        Slug=slug,
        Active=active
    )
    sport_id = db_add_sport(sport)
    return create_response(sport_id)


@sport_bp.route('/<sport_id:int>', methods=['PATCH'])
async def update_sport(request: Request, sport_id: int):
    data = request.json
    slug = generate_slug(data['Name'])
    rowcount = db_update('sports', sport_id, name=data.get('Name'), slug=slug, active=data.get('Active'))
    if rowcount == 0:
        return error_response('Sport not found')
    return update_response(sport_id)


# Doesn't work for multiple queries yet
@sport_bp.route('/search', methods=['POST'])
async def search_sports(request: Request):
    data = request.json
    sports = db_search('sports', **data)
    return list_response(sports)
