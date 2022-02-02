from dataclasses import dataclass
from enum import Enum
from typing import *


class Status(Enum):
    READY = 0
    IN_PROGRESS = 1
    ERROR_DESCRIBING = 2


class State(Enum):
    SAMPLE = 0
    TABLES = 1
    VIEW = 2
    INFO = 3
    ERROR = 4


@dataclass
class Sample:
    nl: Optional[str] = None
    sql: Optional[str] = None
    source_nl: Optional[str] = None
    source_sql: Optional[str] = None
    result: Optional[str] = None


class User:
    def __init__(self, user_id):
        self.id: str = user_id
        self.last: Union[Sample, None] = None
        self.state: State = State.SAMPLE
        self.status: Status = Status.READY

    def generate_sample(self) -> Sample:  # TODO
        generated_sample = Sample(self.id)
        self.last = generated_sample
        return generated_sample


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def add_new_user(self, user_id):
        self.users[user_id] = User(user_id)

