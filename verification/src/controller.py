import os
import json
import dill as pickle
from random import choice, shuffle
from copy import deepcopy
from datetime import datetime

from typing import *
from configure import *

from verification.settings.config import *
from verification.src.dto import *
from verification.src.errors import *
from verification.src.storage import *


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
        self.create()

    def create(self):  # ToDo
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def save(self) -> NoReturn:
        if self.last_sample:
            sample_id = self.last_sample.id
            self.results[sample_id] = self.last_sample.__dict__
            now = datetime.now()
            self.results[sample_id]['time'] = str(now)
        user_result_path = os.path.join(self.dir_path, f'{self.id}_results.json')
        with open(user_result_path, 'w', encoding='utf-8') as user_file:
            json.dump(self.results, user_file)


class Controller:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.statistics: Dict[str, int] = {}
        self.load_statistics()
        self.load_users()
        self.load_samples()

    def load_statistics(self):
        if not os.path.exists(STATISTICS_PATH):
            self.statistics = {}
            return
        with open(STATISTICS_PATH, "r", encoding="utf-8") as controller_file:
            self.statistics = json.load(controller_file)

    def load_users(self):
        if not os.path.exists(CONTROLLER_PATH):
            self.users = {}
            return
        with open(CONTROLLER_PATH, "rb") as controller_file:
            self.users = pickle.load(controller_file)

    def save(self):
        for _user in self.users.values():
            _user.save()
        self.save_controller()
        self.save_statistics()

    def save_controller(self):
        with open(CONTROLLER_PATH, "wb") as controller_file:
            pickle.dump(self.users, controller_file)

    def save_statistics(self):
        with open(STATISTICS_PATH, "w", encoding="utf-8") as statistics_file:
            json.dump(self.statistics, statistics_file)

    def load_samples(self):
        with open(SOURCE_SAMPLES_PATH, 'r', encoding="utf-8") as samples_file:
            self.samples = json.load(samples_file)
            print(len(self.samples))

    def add_new_user(self, user_id: int) -> NoReturn:
        self.users[user_id] = User(user_id)

    def update_statistics(self, user: User) -> NoReturn:
        if user.last_sample:
            sample_id = user.last_sample.id
            self.statistics[sample_id] = self.statistics.get(sample_id, 0) + 1

    def generate_sample_for_user(self, user: User) -> BotSample:
        self.update_statistics(user)
        user_id = user.id
        json_sample = None
        tryings = 0
        while (not json_sample \
                or self.statistics.get(json_sample['id'], 0) >= OVERLAPPING \
                or json_sample['id'] in user.results.keys()) \
                and tryings < len(self.samples):
            json_sample = choice(self.samples)
            tryings += 1
        if tryings >= len(self.samples):
            raise RanOutError()
        logger.info(f"{user.id}: {tryings}/{len(self.samples)}")
        generated_sample = BotSample(
            id=json_sample['id'],
            db=json_sample['db_id'],
            source_nl=json_sample['question'],
            source_sql=json_sample['query'],
            substituted_nl=json_sample['substituted_question'],
            substituted_sql=json_sample['substituted_query'],
            paraphrased_nl=json_sample['paraphrased_question'],
         )
        logger.info(f"{user.id}: Generated id = {generated_sample.id}, text = [{generated_sample.source_nl}]")
        self.users[user_id].last_sample = deepcopy(generated_sample)
        return generated_sample
