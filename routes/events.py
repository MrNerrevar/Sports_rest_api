from sanic import Blueprint, response
from sanic.request import Request
from db import db_get_all_entries, db_add_event, db_update, db_search
from enums import EventType, EventStatus
from models import Event
from utils import generate_slug, stitch_logos, error_response, list_response, update_response, create_response
from datetime import datetime

event_bp = Blueprint('events', url_prefix='/event')


@event_bp.route('/', methods=['GET'])
async def get_events(request: Request):
    events = db_get_all_entries('events')
    return list_response(events)


# datetimes probably need formatting
@event_bp.route('/', methods=['POST'])
async def add_event(request: Request):
    data = request.json
    slug = generate_slug(data['Name'])
    active = False  # Set event to inactive by default
    scheduled_start = datetime.fromisoformat(data['ScheduledStart'])

    # clause to set actual_start value as current time if event status is "Started"
    actual_start = datetime.now() if data.get('Status') == 'STARTED' else None

    logos = stitch_logos(data['Name'])
    if logos is None:
        return error_response('No logos found')

    event = Event(
        Name=data['Name'],
        Slug=slug, Active=active, Type=EventType(data['Type']),
        Sport=data['Sport'], Status=EventStatus(data['Status']),
        ScheduledStart=scheduled_start, ActualStart=actual_start,
        Logos=logos
    )
    event_id = db_add_event(event)
    return create_response(event_id)


@event_bp.route('/<event_id:int>', methods=['PATCH'])
async def update_event(request: Request, event_id: int):
    data = request.json
    slug = generate_slug(data['Name'])

    # clause to set actual_start value as current time if event status is "Started"
    actual_start_updated = datetime.now() if data.get('Status') == 'STARTED' else None

    # scheduled_start and actual_start names modified to accommodate for the generic db_update method in db.py
    rowcount = db_update('events', event_id, name=data.get('Name'), slug=slug, active=data.get('Active'),
                         type=data['Type'], sport=data.get('Sport'), Status=data['Status'],
                         scheduled_start=data.get('ScheduledStart'), actual_start=actual_start_updated)
    if rowcount == 0:
        return error_response('Event not found')

    events = db_search("events", id=data['Sport'])
    if any([e['active'] for e in events]):
        sport = db_search('sports', id=data['Sport'])[0]
        db_update('sports', entity_id=sport['id'], Active=True)
    if all([e['active'] is False for e in events]):
        sport = db_search('sports', id=data['Sport'])[0]
        db_update('sports', entity_id=sport['id'], Active=False)

    return update_response(event_id)


@event_bp.route('/search', methods=['POST'])
async def search_events(request: Request):
    data = request.json
    events = db_search('events', **data)
    return list_response(events)
