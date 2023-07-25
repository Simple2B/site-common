import sqlalchemy as sa

# must have this import
from app.database import db

case_stacks = sa.Table(
    "case_stacks",
    db.Model.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("case_id", sa.ForeignKey("cases.id")),
    sa.Column("stack_id", sa.ForeignKey("stacks.id")),
)


class CaseStack(db.Model):
    __tablename__ = "case_stacks"
