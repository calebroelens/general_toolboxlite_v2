import socket
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.auth.session import setup_session, session_db, delete_session
from api.storage.database import Database
from core.odoo.database_info import DatabaseInfo
from core.odoo.client import OdooClient

connect_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@connect_router.get('/connect')
def render_connect(request: Request):
    return templates.TemplateResponse(
        'pages/connect.html',
        {'request': request}
    )


@connect_router.post('/connect/find_databases')
async def find_database(request: Request):
    json_data = await request.json()
    db_info = DatabaseInfo(json_data.get('url'), json_data.get('port'))
    try:
        databases = db_info.list_databases(throw_exception=True)
        return JSONResponse(status_code=200, content={'databases': databases})
    except socket.gaierror as e:
        return JSONResponse(status_code=400, content={'error': str(e)})
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': str(e)})


@connect_router.post('/connect/login')
async def login(request: Request, response: Response, session=Depends(session_db)):
    json_data = await request.json()
    try:
        odoo_client = OdooClient(
            json_data.get('url'),
            json_data.get('port'),
            json_data.get('database'),
            json_data.get('user'),
            json_data.get('password')
        )
        odoo_client.start()
        user_uid = odoo_client.login()
    except Exception as exception:
        return JSONResponse(status_code=400, content={"error": str(exception)})
    # Setup session
    session_uid = str(uuid4())
    setup_session(session, session_uid, user_uid, json_data)
    # Set cookie
    response.set_cookie('session_key', session_uid)
    response.status_code = 200
    return response


@connect_router.get('/logout')
async def logout(request: Request, response: Response, session: Database = Depends(session_db)):
    """
    Logout
    :param request:
    :param response:
    :param session:
    :return:
    """
    delete_session(request, session)
    response.delete_cookie('session_key')
    response.status_code = 200
    return response

