from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.enums import ServiceOrderStatus

class ServiceOrderHistory(Base):
    __tablename__ = "service_order_histories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_order_id: Mapped[int] = mapped_column(
        ForeignKey("service_orders.id"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        nullable=False,
    )
    old_status: Mapped[ServiceOrderStatus] = mapped_column(
        Enum(ServiceOrderStatus),
        nullable=False,
    )
    new_status: Mapped[ServiceOrderStatus] = mapped_column(
        Enum(ServiceOrderStatus), 
        nullable=False,
    )
    note: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True,
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
