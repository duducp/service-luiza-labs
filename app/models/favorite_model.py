from app.database import db
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID


class FavoriteModel(db.Model):
    __tablename__ = "favorites"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clients.id"), nullable=False
    )
