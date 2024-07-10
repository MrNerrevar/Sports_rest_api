from sanic import Blueprint, response
from sanic.request import Request
from db import db_get_sports, db_add_sport, db_update_sport, db_search_sports
from models import Sport
from utils import generate_slug


sport_bp = Blueprint('sports', url_prefix='/sport')


#unnecessary, but lists all sports
@sport_bp.route('/', methods=['GET'])
async def get_sports(request: Request):
    sports = db_get_sports()
    return response.json([dict(sport) for sport in sports])


@sport_bp.route('/', methods=['POST'])
async def add_sport(request: Request):
    data = request.json
    slug = generate_slug(data['Name'])
    sport = Sport(Name=data['Name'], Slug=slug, Active=data.get('Active', True))
    sport_id = db_add_sport(sport)
    return response.json({'id': sport_id, **data}, status=201)


@sport_bp.route('/<sport_id:int>', methods=['PATCH'])
async def update_sport_route(request: Request, sport_id: int):
    data = request.json
    rowcount = db_update_sport(sport_id, name=data.get('Name'), slug=data.get('Slug'), active=data.get('Active'))
    if rowcount == 0:
        return response.json({'error': 'Sport not found'}, status=404)
    return response.json({'updated': rowcount}, status=200)


# Doesn't work for multiple queries yet
@sport_bp.route('/search', methods=['POST'])
async def search_sports_route(request: Request):
    data = request.json
    name = data.get('name')
    slug = data.get('slug')
    sports = db_search_sports(name=name, slug=slug)
    return response.json([dict(sport) for sport in sports])
