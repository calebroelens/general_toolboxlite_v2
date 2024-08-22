from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from api.storage.models import model_bases

class Database:

    def __init__(self, engine_file: str, memory_database=False, echo=False):
        if not memory_database:
            self._engine = create_engine(f'sqlite:///{engine_file}', echo=echo, connect_args={"check_same_thread": False})
        else:
            self._engine = create_engine(f"sqlite:///:memory:", echo=echo, connect_args={'check_same_thread': False}, poolclass=StaticPool)
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)()

    def init_metadata(self, metadata):
        metadata.metadata.create_all(self._engine)

    def get_session(self):
        return self._session

    def __str__(self):
        return f"Engine: {self._engine}"

    def close(self):
        self._session.close_all()

    def create(self, *records, commit=True):
        self._session.add_all(records)
        if commit:
            self._session.commit()

    def get_one_by_id(self, model, identifier):
        return self._session.query(model).get(identifier)

    def get_all(self, model):
        return self._session.query(model).all()

    def delete_by_id(self, model, identifier: int, commit=True):
        self._session.query(model).filter(model.id == identifier).delete()
        if commit:
            self._session.commit()


# Initiate databases
db = Database("odoo_toolbox.db", memory_database=False)
for model_base in model_bases:
    db.init_metadata(model_base)


# Database accessor
def get_database():
    """
    Get database
    :return:
    """
    try:
        yield db
    finally:
        db.close()
