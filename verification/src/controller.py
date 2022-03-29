import json
from random import choice
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import *
from configure import *


class Status(Enum):
    READY = 0
    IN_PROGRESS_FLUENCY_SOURCE = 1
    IN_PROGRESS_FLUENCY_SUBSTITUTION = 2
    IN_PROGRESS_EQUIVALENT = 3
    IN_PROGRESS_SQL = 4
    ERROR_DESCRIBING_FLUENCY_SOURCE = 5
    ERROR_DESCRIBING_FLUENCY_SUBSTITUTION = 6
    ERROR_DESCRIBING_EQUIVALENT = 7
    ERROR_DESCRIBING_SQL = 8
    LAST = 9
    CHOOSING_TABLE = 10
    VIEW_TABLE = 11
    INFO_READING = 12


class State(Enum):
    SAMPLE = 0
    TABLES = 1
    VIEW = 2
    INFO = 3
    ERROR = 4


@dataclass
class BotSample:
    id: Optional[int] = None
    db: Optional[str] = None
    source_nl: Optional[str] = None
    source_sql: Optional[str] = None
    substituted_nl: Optional[str] = None
    substituted_sql: Optional[str] = None
    paraphrased_nl: Optional[str] = None
    result: Optional[str] = None
    ok_fluency_source: bool = True
    ok_fluency_substitution: bool = True
    ok_equivalent: bool = True
    ok_sql: bool = True


class User:
    def __init__(self, user_id):
        self.id: str = user_id
        self.last_sample: Optional[BotSample] = None
        self.last_message: Any = None
        self.state: State = State.SAMPLE
        self.status: Status = Status.READY
        self.last_status: Optional[Status] = None
        self.last_reaction: Optional[str] = None
        self.chosen_table: Optional[str] = None

    def create(self):  # ToDo
        pass

    def update(self):  # ToDo
        pass

    def load(self):  # ToDo
        pass

    def save(self, sample: BotSample) -> NoReturn:
        print("I have saved")


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.load_statuses()
        self.calculate_statistics()
        self.update_users()

    def load_statuses(self):  # ToDo
        pass

    def calculate_statistics(self):  # ToDo
        pass

    def update_users(self):  # ToDo
        pass

    def load_samples(self):
        with open(SAMPLES_PARAPHRASED_PATH, 'r') as samples_file:
            self.samples = json.load(samples_file)

    def add_new_user(self, user_id):
        self.users[user_id] = User(user_id)

    def generate_sample_for_user(self, user_id) -> BotSample:  # ToDo
        # generated_sample = Sample()
        json_sample = choice(self.samples)
        generated_sample = BotSample(
            id=json_sample['id'],
            db=json_sample['db_id'],
            source_nl=json_sample['question'],
            source_sql=json_sample['query'],
            substituted_nl=json_sample['substituted_question'],
            substituted_sql=json_sample['substituted_query'],
            paraphrased_nl=json_sample['paraphrased_question'],
         )
        self.users[user_id].last_sample = deepcopy(generated_sample)
        self.samples.remove(json_sample)
        return generated_sample
