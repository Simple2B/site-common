# flake8: noqa F821
from typing import List
from prompt_toolkit.key_binding.bindings import vi
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db
from .case_stacks import case_stacks


class Case(db.Model):
    __tablename__ = "cases"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), nullable=False, unique=True
    )

    sub_title: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)

    is_active: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=True
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False
    )
    project_link: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    is_main: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False
    )

    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    _stacks: orm.Mapped[List["Stack"]] = orm.relationship(
        secondary=case_stacks,
        back_populates="_cases",
        lazy="dynamic",
        viewonly=True,
    )
    _screenshots: orm.Mapped[List["CaseScreenshot"]] = orm.relationship(
        "CaseScreenshot", viewonly=True
    )

    case_images: orm.Mapped[List["CaseImage"]] = orm.relationship("CaseImage")

    @hybrid_property
    def stacks(self) -> str:
        return [stack.name for stack in self._stacks.all()]

    @hybrid_property
    def screenshots(self) -> str:
        return [img.url for img in self._screenshots]

    @hybrid_property
    def slug_name(self) -> str:
        return self.title.strip().replace(" ", "-").lower()

    def __repr__(self):
        return f"<{self.id}: {self.title}>"
