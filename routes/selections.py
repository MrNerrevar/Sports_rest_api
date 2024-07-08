from sanic import Blueprint, response
from sanic.request import Request

selection_bp = Blueprint('selections', url_prefix='/selection')


@selection_bp.route('/', methods=['GET'])
async def get_selections(request: Request):
    return


@selection_bp.route('/', methods=['POST'])
async def add_selection(request: Request):
    return


@selection_bp.route('/{selection_id}', methods=['PATCH'])
async def update_selection(request: Request):
    return


@selection_bp.route('/search', methods=['POST'])
async def search_selections(request: Request):
    return
