from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
from json import dumps
from time import sleep

application_state_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@application_state_router.get('/application_state/init')
async def stream_application_state_init(request: Request):
    return StreamingResponse(stream_application_state_init_emitter(request), media_type="text/event-stream")


def stream_application_state_init_emitter(request: Request):
    for i in range(101):
        init_state = {"progress": i, "state": "Loaded"}
        data = dumps(init_state)
        sleep(0.05)
        yield f"event: application_state_init\ndata: {data}\n\n"