from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String
# Base
SessionBase = declarative_base()


class Session(SessionBase):
    __tablename__ = "base_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    port: Mapped[int] = mapped_column(Integer, nullable=True)
    uid: Mapped[int] = mapped_column(Integer)
    db: Mapped[str] = mapped_column(String)
    session_id: Mapped[str] = mapped_column(String, unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
