from typing import List
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db
from .case_stacks import case_stacks

class Stack(db.Model):
    __tablename__ = "stacks"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    _cases: orm.Mapped[List["Case"]] = orm.relationship(
        "Case",
        secondary=case_stacks,
        viewonly=True,lazy="dynamic"
            )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"