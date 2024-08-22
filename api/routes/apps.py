from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.auth.session import session_db, get_session
from api.storage.database import Database

apps_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@apps_router.get('/apps')
def render_apps(request: Request, session: Database = Depends(session_db)):
    session_record = get_session(request, session)
    response_data = {'request': request, 'logged_in': session_record not in [None, False]}
    if session_record:
        response_data.update({'server_data': {'url': session_record.url, 'user': session_record.user}})
    return templates.TemplateResponse(
        'pages/apps.html',
        response_data
    )

