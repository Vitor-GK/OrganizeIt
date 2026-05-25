from enum import Enum

class TaksEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"

class PriorityEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"