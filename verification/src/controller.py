import os
import json
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

    def create(self):  # ToDo
        user_dir_path = os.path.join(USERS_FOLDER, f"{self.id}")
        if not os.path.exists(user_dir_path):
            os.mkdir(user_dir_path)

    def save(self, sample: BotSample) -> NoReturn:
        print("I have saved")


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.statistics: Dict[str, int] = {}
        self.load_statuses()
        self.load_samples()

    def load_statuses(self):
        with open(CONTROLLER_PATH, "r", encoding="utf-8") as controller_file:
            self.user = json.load(controller_file)

    def calculate_statistics(self):
        with open(STATISTICS_PATH, 'r', encoding="utf-8") as statistics_file:
            statistics = json.load(statistics_file)
        for user_id in self.users.keys():
            user_result_file = os.path.join(USERS_FOLDER, f"{user_id}", "results.json")
            samples = []
            with open(user_result_file, 'r') as samples_file:
                samples = json.load(samples_file)
            for _sample in samples:
                id = _sample['id']
                statistics[id] = statistics.get(id, 0) + 1
        with open(STATISTICS_PATH, "w", encoding="utf-8") as statistics_file:
            json.dump(statistics, statistics_file)

    def update_users(self):
        for _user in self.users.values():
            _user.update()

    def save(self):
        self.save_statuses()
        self.save_statistics()

    def save_statuses(self):
        with open(CONTROLLER_PATH, "w", encoding="utf-8") as controller_file:
            json.dump(self.users, controller_file)

    def save_statistics(self):
        with open(CONTROLLER_PATH, "w", encoding="utf-8") as statistics_file:
            json.dump(self.users, statistics_file)

    def load_samples(self):
        with open(SAMPLES_PARAPHRASED_PATH, 'r', encoding="utf-8") as samples_file:
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
