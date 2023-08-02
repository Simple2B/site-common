import sqlalchemy as sa
from sqlalchemy import orm
import enum


from .image import Image

# must have this import
from app.database import db


class EnumCaseImageType(enum.Enum):
    main_image = "main_image"
    full_main_image = "full_main_image"


class CaseImage(db.Model, Image):
    __tablename__ = "case_images"

    case_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cases.id"), nullable=False
    )
    type_of_image = orm.mapped_column(sa.Enum(EnumCaseImageType), nullable=False)

    is_deleted: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False
    )

    def __repr__(self):
        return f"<{self.id}: {self.url}>"
