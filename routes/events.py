from sanic import Blueprint, response
from sanic.request import Request


event_bp = Blueprint('events', url_prefix='/event')


@event_bp.route('/', methods=['GET'])
async def get_events(request: Request):
    return


@event_bp.route('/', methods=['POST'])
async def add_event(request: Request):
    return


@event_bp.route('/{event_id}', methods=['PATCH'])
async def update_event(request: Request):
    return


@event_bp.route('/search', methods=['POST'])
async def search_events(request: Request):
    return
