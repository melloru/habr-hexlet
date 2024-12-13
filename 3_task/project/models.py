from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid


class Base(DeclarativeBase):
    pass

class UserPurchases(Base):
    __tablename__ = "user_purchases"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
    item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
    category: Mapped[str] = mapped_column(String)
    purchase_date: Mapped[DateTime] = mapped_column(DateTime)

class Items(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)

class Recommendations(Base):
    __tablename__ = "recommendations"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
    item_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
