from sanic import Blueprint, response
from sanic.request import Request
from db import db_get_events, db_add_event
from enums import EventType, EventStatus
from models import Event
from utils import generate_slug
from datetime import datetime

event_bp = Blueprint('events', url_prefix='/event')


@event_bp.route('/', methods=['GET'])
async def get_events(request: Request):
    events = db_get_events()
    return response.json([dict(event) for event in events])


# datetimes probably need formatting
# logos still need full fetching logic implemented
@event_bp.route('/', methods=['POST'])
async def add_event(request: Request):
    data = request.json
    slug = generate_slug(data['Name'])
    scheduled_start = datetime.fromisoformat(data['ScheduledStart'])
    actual_start = datetime.now() if (data.get('EventStatus') == 'STARTED') else None
    event = Event(
        Name=data['Name'], Slug=slug, Active=data['Active'], Type=EventType[data['Type']],
        Sport=data['Sport'], Status=EventStatus[data['Status']],
        ScheduledStart=scheduled_start, ActualStart=actual_start,
        Logos=data.get('Logos', '')
    )
    event_id = db_add_event(event)
    return response.json({'id': event_id, **data}, status=201)


@event_bp.route('/<event_id:int>', methods=['PATCH'])
async def update_event(request: Request):
    return


@event_bp.route('/search', methods=['POST'])
async def search_events(request: Request):
    return
