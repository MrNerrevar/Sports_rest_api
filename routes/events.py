from sanic import Blueprint, response
from sanic.request import Request
from db import db_get_all_entries, db_add_event, db_update, db_search
from enums import EventType, EventStatus
from models import Event
from utils import generate_slug, fetch_logos
from datetime import datetime

event_bp = Blueprint('events', url_prefix='/event')


@event_bp.route('/', methods=['GET'])
async def get_events(request: Request):
    events = db_get_all_entries('events')
    return response.json([dict(event) for event in events])


# datetimes probably need formatting
@event_bp.route('/', methods=['POST'])
async def add_event(request: Request):
    data = request.json
    slug = generate_slug(data['Name'])
    scheduled_start = datetime.fromisoformat(data['ScheduledStart'])
    actual_start = datetime.now() if (data.get('EventStatus') == 'STARTED') else None

    try:
        team_1, team_2 = data['Name'].split(' vs ')
    except ValueError:
        return response.json({'error': 'Invalid event name format. It should be "team_1 vs team_2".'}, status=400)

    logo_1 = fetch_logos(team_1)
    logo_2 = fetch_logos(team_2)
    logos = f"{logo_1}|{logo_2}" if logo_1 or logo_2 else None

    event = Event(
        Name=data['Name'],
        Slug=slug, Active=data['Active'], Type=EventType(data['Type']),
        Sport=data['Sport'], Status=EventStatus(data['Status']),
        ScheduledStart=scheduled_start, ActualStart=actual_start,
        Logos=logos
    )
    event_id = db_add_event(event)
    return response.json({'id': event_id, **data}, status=201)


@event_bp.route('/<event_id:int>', methods=['PATCH'])
async def update_event(request: Request, event_id: int):
    data = request.json
    slug = generate_slug(data['Name'])
    rowcount = db_update('events', event_id, name=data.get('Name'), slug=slug, active=data.get('Active'),
                         type=EventType(data['Type']), sport=data.get('Sport'), Status=EventStatus(data['Status']),
                         ScheduledStart=data.get('ScheduledStart'), ActualStart=data.get('ActualStart'))
    if rowcount == 0:
        return response.json({'error': 'Sport not found'}, status=404)
    return response.json({'updated': rowcount}, status=200)


@event_bp.route('/search', methods=['POST'])
async def search_events(request: Request):
    data = request.json
    events = db_search('events', **data)
    return response.json([dict(event) for event in events])