from sanic import Blueprint, response
from sanic.request import Request
from db import db_get_selections, db_add_selection
from models import Selection
from enums import SelectionOutcome
from decimal import Decimal

selection_bp = Blueprint('selections', url_prefix='/selection')


@selection_bp.route('/', methods=['GET'])
async def get_selections(request: Request):
    selections = db_get_selections()
    return response.json([dict(selection) for selection in selections])


@selection_bp.route('/', methods=['POST'])
async def add_selection(request: Request):
    data = request.json
    selection = Selection(
        Name=data['Name'], Event=data['Event'], Price=Decimal(data['Price']),
        Active=data['Active'], Outcome=SelectionOutcome[data['Outcome']]
    )
    selection_id = db_add_selection(selection)
    return response.json({'id': selection_id, **data}, status=201)


@selection_bp.route('/<selection_id:int>', methods=['PATCH'])
async def update_selection(request: Request):
    return


@selection_bp.route('/search', methods=['POST'])
async def search_selections(request: Request):
    return
