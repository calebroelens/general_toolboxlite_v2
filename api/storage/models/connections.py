from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

# Base
ConnectionsBase = declarative_base()


class Connections(ConnectionsBase):
    # Table
    __tablename__ = "base_connections"

    # Columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    environment_type: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    port: Mapped[int] = mapped_column(Integer, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean)
