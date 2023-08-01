import sqlalchemy as sa
from sqlalchemy import orm


from .image import Image

# must have this import
from app.database import db


class CaseImage(db.Model, Image):

    __tablename__ = "case_images"

    def __repr__(self):
        return f"<{self.id}: {self.url}>"
