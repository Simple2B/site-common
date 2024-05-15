# flake8: noqa F821

import sqlalchemy as sa
from sqlalchemy import orm


# must have this import
from app.database import db


class BlacklistIP(db.Model):
    __tablename__ = "blacklist_ips"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    address: orm.Mapped[str] = orm.mapped_column(sa.String(64))

    def __repr__(self):
        return f"<BlacklistIP: {self.address}>"
