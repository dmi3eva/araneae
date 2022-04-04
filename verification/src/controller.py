import os
import json
import dill as pickle
from random import choice, shuffle
from copy import deepcopy

from typing import *
from configure import *

from verification.settings.config import *
from verification.src.dto import *


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
        self.dir_path = os.path.join(USERS_FOLDER, f"{self.id}")
        self.results: Optional[Dict[int, Optional[Dict]]] = {}

    def create(self):  # ToDo
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def save(self) -> NoReturn:
        sample_id = self.last_sample.id
        self.results[sample_id] = self.last_sample
        user_result_path = os.path.join(self.dir_path, f'{self.id}_results.json')
        with open(user_result_path, 'w', encoding='utf-8'):
            json.dump(self.results)


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.statistics: Dict[str, int] = {}
        self.load_statistics()
        self.load_users()
        self.load_samples()

    def load_statistics(self):
        with open(STATISTICS_PATH, "r", encoding="utf-8") as controller_file:
            self.statistics = json.load(controller_file)

    def load_users(self):
        with open(CONTROLLER_PATH, "r", encoding="utf-8") as controller_file:
            self.users = pickle.load(controller_file)

    def save(self):
        for _user in self.users.values():
            _user.save()
        self.save_users()
        self.save_statistics()

    def save_users(self):
        with open(CONTROLLER_PATH, "w", encoding="utf-8") as controller_file:
            json.dump(self.users, controller_file)

    def save_statistics(self):
        with open(STATISTICS_PATH, "w", encoding="utf-8") as statistics_file:
            json.dump(self.users, statistics_file)

    def load_samples(self):
        with open(SAMPLES_PARAPHRASED_PATH, 'r', encoding="utf-8") as samples_file:
            self.samples = json.load(samples_file)

    def add_new_user(self, user_id: int) -> NoReturn:
        self.users[user_id] = User(user_id)

    def update_statistics(self, user: User) -> NoReturn:
        sample_id = user.last_sample.id
        self.statistics[sample_id] = self.statistics.get(sample_id, 0) + 1

    def generate_sample_for_user(self, user: User) -> BotSample:  # ToDo
        # generated_sample = Sample()
        self.update_statistics(user)
        user_id = user.id
        json_sample = None
        while not json_sample or self.statistics.get(json_sample['id'], 0) >= OVERLAPPING:
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
        return generated_sample
