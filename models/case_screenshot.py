import sqlalchemy as sa
from sqlalchemy import orm

from .image import Image

# must have this import
from app.database import db


class CaseScreenshot(db.Model, Image):

    __tablename__ = "case_screenshots"

    case_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cases.id"), nullable=False
    )
    description: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True, default=""
    )

    def __repr__(self):
        return f"<{self.id}: {self.url}>"
