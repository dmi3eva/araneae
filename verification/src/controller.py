import json
from random import choice
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import *
from verification.settings.configuration import *

SAMPLES_PATH = '../datasets/araneae/araneae.json'

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
    db: Optional[str] = None
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


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.samples = []
        self.load_samples()

    def load_samples(self):
        with open(SAMPLES_PATH, 'r') as samples_file:
            self.samples = json.load(samples_file)

    def add_new_user(self, user_id):
        self.users[user_id] = User(user_id)

    def generate_sample_for_user(self, user_id) -> Sample:  # TODO
        # generated_sample = Sample()
        json_sample = choice(self.samples)
        generated_sample = Sample(
            db=json_sample['db_id'],
            nl=json_sample['question'],
            sql=json_sample['query']
        )
        self.users[user_id].last = deepcopy(generated_sample)
        return generated_sample

