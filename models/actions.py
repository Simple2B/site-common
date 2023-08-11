from datetime import datetime
from enum import IntEnum

import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db


class ActionsType(IntEnum):
    CREATE = 1
    EDIT = 2
    DELETE = 3


class Entity(IntEnum):
    CASE = 1
    ADMIN = 2
    QUESTION = 3
    CANDIDATE = 4


class Action(db.Model):
    __tablename__ = "actions"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("superusers.id"), nullable=False
    )
    action: orm.Mapped[ActionsType] = orm.mapped_column(
        sa.Enum(ActionsType), nullable=False
    )
    entity: orm.Mapped[Entity] = orm.mapped_column(sa.Enum(Entity), nullable=False)
    entity_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    text: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<{self.id}: {self.action} {self.entity}>"
