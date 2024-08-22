from fastapi import FastAPI
from tkinter import Tk
from uvicorn import Config as ServerConfig
from webview import create_window as create_web_window
from webview import start as start_web_window
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from core.server import WindowedServer
from uuid import uuid4
from api.routes import api_routes
from api.apps import app_routers


def setup_webserver(server: FastAPI):
    """
    Setup webserver variables
    :param server: FastAPI instance
    :return:
    """
    server.mount('/static', StaticFiles(directory='static'), name='static')
    for route in api_routes:
        server.include_router(route)
    for route in app_routers:
        server.include_router(route)
    server.add_middleware(SessionMiddleware, secret_key=str(uuid4()))
    return server


if __name__ == "__main__":
    """
    Start app
    """
    web_server = FastAPI()
    web_server = setup_webserver(web_server)
    tk_window = Tk()
    tk_window.geometry("1600x800")
    create_web_window('Odoo Toolbox Lite v2 by Caleb Roelens', 'http://localhost:8000/splash', confirm_close=True)
    web_server_config = ServerConfig(web_server, host='0.0.0.0', port=8000)
    # App instance
    app_server = WindowedServer(web_server_config)
    with app_server.run_in_thread():
        start_web_window()
