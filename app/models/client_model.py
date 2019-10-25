from app.database import db
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID


class ClientModel(db.Model):
    __tablename__ = "clients"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
