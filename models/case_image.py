import sqlalchemy as sa
from sqlalchemy import orm


# must have this import
from app.database import db



class CaseImage(db.Model):

    __tablename__ = "case_images"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    case_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("cases.id"), nullable=False)
    url: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)

    def __repr__(self):
        return f"<{self.id}: {self.url}>"