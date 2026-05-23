from enum import StrEnum

class ServiceOrderStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    DONE = "done"
    CANCELED = "canceled"

class ServiceOrderPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"

class ExportFormat(StrEnum):
    PDF = "pdf"
    EXCEL = "excel"