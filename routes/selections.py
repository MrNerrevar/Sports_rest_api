from sanic import Blueprint
from sanic.request import Request
from db import db_get_all_entries, db_add_selection, db_update, db_search
from models import Selection
from enums import SelectionOutcome
from utils import error_response, list_response, update_response, create_response

selection_bp = Blueprint('selections', url_prefix='/selection')


@selection_bp.route('/', methods=['GET'])
async def get_selections(request: Request):
    selections = db_get_all_entries('selections')
    return list_response(selections)


@selection_bp.route('/', methods=['POST'])
async def add_selection(request: Request):
    data = request.json
    active = False  # Set event to inactive by default
    selection = Selection(
        Name=data['Name'],
        Event=data['Event'],
        Price=data['Price'],
        Active=active,
        Outcome=SelectionOutcome(data['Outcome'])
    )
    selection_id = db_add_selection(selection)
    return create_response(selection_id)


@selection_bp.route('/<selection_id:int>', methods=['PATCH'])
async def update_selection(request: Request, selection_id: int):
    data = request.json
    rowcount = db_update('selections', selection_id, name=data.get('Name'), event=data.get('Event'),
                         price=data['Price'], active=data.get('Active'),
                         outcome=data['Outcome'])
    if rowcount == 0:
        return error_response('Selection not found')

    event_id = data['Event']
    selections = db_search('selections', event=event_id)
    if any([e['active'] for e in selections]):
        event = db_search('events', id=event_id)[0]
        sport_id = event['sport']
        db_update('events', entity_id=event_id, active=1)
        db_update('sports', entity_id=sport_id, active=1)
    if all([not e['active'] for e in selections]):
        event = db_search('events', id=event_id)[0]
        sport_id = event['sport']
        db_update('events', entity_id=event_id, active=0)
        events = db_search('events', id=sport_id)
        if all([not e['active'] for e in events]):
            db_update('sports', entity_id=sport_id, active=0)

    return update_response(selection_id)


@selection_bp.route('/search', methods=['POST'])
async def search_selections(request: Request):
    data = request.json
    selections = db_search('selections', **data)
    return list_response(selections)
