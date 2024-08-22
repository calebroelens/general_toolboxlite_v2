from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse


splash_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@splash_router.get('/splash')
def render_splash(request: Request):
    return templates.TemplateResponse(
        'splash.html',
        {'request': request}
    )
