from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db


class CandidateResume(db.Model):
    __tablename__ = "candidates_resumes"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    cv_path: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), default=datetime.now)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("candidates.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.id}: at {self.created_at}>"