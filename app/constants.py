from enum import IntEnum


class TaskStatus(IntEnum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3


class BoardRole(IntEnum):
    OWNER = 1
    EDITOR = 2


class TaskImportance(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
