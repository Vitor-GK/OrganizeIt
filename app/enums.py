from enum import Enum

class TaksEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"