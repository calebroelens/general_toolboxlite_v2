from . import splash
from . import connect
from . import apps
from . import application_state

api_routes = [
    splash.splash_router,
    connect.connect_router,
    apps.apps_router,
    application_state.application_state_router
]
