from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus

class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ServiceOrderStatus] = mapped_column(
        Enum(ServiceOrderStatus),
        default=ServiceOrderStatus.OPEN,
        nullable=False,
    )
    priority: Mapped[ServiceOrderPriority] = mapped_column(
        Enum(ServiceOrderPriority),
        default=ServiceOrderPriority.MEDIUM,
        nullable=False,
    )
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    responsible_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)