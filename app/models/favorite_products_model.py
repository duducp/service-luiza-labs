from uuid import uuid4

from app.database import db

from sqlalchemy.dialects.postgresql import UUID


class FavoriteProductsModel(db.Model):
    __tablename__ = "favorite_products"
    __table_args__ = (db.UniqueConstraint("favorite_id", "product_id"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    favorite_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("favorites.id"), nullable=False
    )
    product_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)
