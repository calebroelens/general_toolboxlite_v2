from api.storage.database import Database
from api.storage.models.sessions import Session, SessionBase
from core.odoo.client import OdooClient

from fastapi import Request
from sqlalchemy.orm import Query

db = Database("sessions.odoo", memory_database=True)
db.init_metadata(SessionBase)


def session_db():
    """
    Get the session database: Close after each interaction
    :return:
    """
    try:
        yield db
    finally:
        db.close()


def odoo_db(session: Session):
    """
    Get the Odoo Database associated with a session
    :param session:
    :return:
    """
    return OdooClient(session.url, session.port, session.db, session.user, session.password)


def setup_session(session_database: Database, session_id: str, uid: str, auth: dict):
    session_database.create(
        Session(user=auth.get('user'), password=auth.get('password'), url=auth.get('url'), port=auth.get('port'), uid=uid, session_id=session_id, db=auth.get('database'))
    )


def get_session(request: Request, db_session: Database):
    if session_id := request.cookies.get('session_key'):
        res = db_session.get_session().query(Session).filter(Session.session_id == session_id)
        res: Query
        if res.all():
            return res.one()
        else:
            return False


def delete_session(request: Request, db_session: Database):
    if session_id := get_session(request, db_session):
        db_session.delete_by_id(Session, session_id.session_id, True)
