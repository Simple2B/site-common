# flake8: noqa F821
from typing import List

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
        "CaseScreenshot", viewonly=True, lazy="dynamic"
    )

    case_images: orm.Mapped[List["CaseImage"]] = orm.relationship(
        "CaseImage", viewonly=True, lazy="dynamic"
    )

    @hybrid_property
    def stacks_names(self) -> str:
        return [stack.name for stack in self._stacks.all()]

    @hybrid_property
    def stacks(self) -> str:
        return self._stacks.all()

    @hybrid_property
    def screenshots(self) -> str:
        return self._screenshots.all()

    @hybrid_property
    def main_image_url(self) -> str:
        from . import CaseImage, EnumCaseImageType

        image = (
            self.case_images.filter_by(
                type_of_image=EnumCaseImageType.case_main_image, is_deleted=False
            )
            .order_by(CaseImage.id.desc())
            .limit(1)
            .first()
        )

        if image:
            return image.url
        return ""

    @hybrid_property
    def preview_image_url(self):
        from . import CaseImage, EnumCaseImageType

        image = (
            self.case_images.filter_by(
                type_of_image=EnumCaseImageType.case_preview_image, is_deleted=False
            )
            .order_by(CaseImage.id.desc())
            .limit(1)
            .first()
        )

        if image:
            return image.url
        return ""

    @hybrid_property
    def slug_name(self) -> str:
        return self.title.strip().replace(" ", "-").replace("_", "-").lower()

    def as_dict(self):
        case_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        case_dict["_stacks"] = [stack.as_dict() for stack in self._stacks]

        return case_dict

    def __repr__(self):
        return f"<{self.id}: {self.title}>"
