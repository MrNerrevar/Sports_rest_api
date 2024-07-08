from sanic import Blueprint, response
from sanic.request import Request


sport_bp = Blueprint('sports', url_prefix='/sport')


@sport_bp.route('/', methods=['GET'])
async def get_sports(request: Request):
    return


@sport_bp.route('/', methods=['POST'])
async def add_sport(request: Request):
    return


@sport_bp.route('/{sport_id}', methods=['PATCH'])
async def update_sport(request: Request):
    return


@sport_bp.route('/search', methods=['POST'])
async def search_sport(request: Request):
    return
