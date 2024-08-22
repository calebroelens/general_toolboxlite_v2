from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse

from api.auth.session import session_db, get_session, odoo_db
from api.storage.database import Database
from api.apps.custom_commands.commands import BaseCommand

custom_commands_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@custom_commands_router.get('/custom_commands')
def render_custom_commands(request: Request, session: Database = Depends(session_db)):
    session_record = get_session(request, session)
    response_data = {'request': request, 'logged_in': session_record not in [None, False]}
    if session_record:
        response_data.update({"commands": BaseCommand.commands})
    return templates.TemplateResponse(
        'pages/custom_commands.html',
        response_data
    )


@custom_commands_router.get('/custom_commands/run/{technical_name}')
async def run_custom_commands(request: Request, technical_name: str, session: Database = Depends(session_db)):
    if session_id := get_session(request, session):
        command_register = {command.technical_name: command for command in BaseCommand.commands}
        if command := command_register.get(technical_name):
            client = odoo_db(session_id)
            client.start()
            client.login()
            kwargs = {'client': client}
            return StreamingResponse(yield_responses(command, kwargs), media_type="text/event-stream")
    else:
        return templates.TemplateResponse(
            'pages/connect.html',
            {
                "request": request
            }
        )


def yield_responses(command, kwargs):
    for res in command.run(**kwargs):
        yield res


