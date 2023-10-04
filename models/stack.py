from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm
from .case_stacks import case_stacks

# must have this import
from app.database import db

if TYPE_CHECKING:
    from .case import Case


class Stack(db.Model):
    __tablename__ = "stacks"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    _cases: orm.Mapped[list["Case"]] = orm.relationship(
        secondary=case_stacks,
    )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
