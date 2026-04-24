from enum import IntEnum


class TaskStatus(IntEnum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3


class BoardRole(IntEnum):
    OWNER = 1
    EDITOR = 2
