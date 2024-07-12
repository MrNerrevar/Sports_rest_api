from sanic import Blueprint
from sanic.request import Request

import db
from db import db_add_sport, db_add_event, db_add_selection, db_drop_table
from enums import EventType, EventStatus, SelectionOutcome
from models import Sport, Event, Selection
from utils import generate_slug, create_response, stitch_logos
import json
from datetime import datetime

populate_bp = Blueprint('populate', url_prefix='/populate')


@populate_bp.route('/', methods=['POST'])
async def populate_db(request: Request):
    populate_data = open('populate.json')
    data = json.load(populate_data)

    db_drop_table('sports')
    db_drop_table('events')
    db_drop_table('selections')
    db.create_tables()

    for sport in data['sports']:
        db_add_sport(Sport(Name=sport['Name'], Slug=generate_slug(sport['Name']), Active=False))

    for event in data['events']:
        scheduled_start = datetime.fromisoformat(event['ScheduledStart'])
        actual_start = datetime.now() if event['Status'] == 'STARTED' else None
        logos = stitch_logos(event['Name'])
        db_add_event(Event(Name=event['Name'], Slug=generate_slug(event['Name']), Active=False,
                           Type=EventType(event['Type']), Sport=event['Sport'], Status=EventStatus(event['Status']),
                           ScheduledStart=scheduled_start, ActualStart=actual_start, Logos=logos))

    for selection in data['selections']:
        db_add_selection(Selection(Name=selection['Name'], Event=selection['Event'], Price=selection['Price'],
                                   Active=False, Outcome=SelectionOutcome(selection['Outcome'])))

    return create_response('Populated Successfully')
