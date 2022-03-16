import json
from copy import deepcopy
from configure import *
from random import shuffle

with open(SAMPLES_JSON, 'r') as samples_file:
    samples = json.load(samples_file)

shuffled = shuffle(samples)
dummy_samples = []
for i, _sample in enumerate(samples[:5]):
    _sample['id'] = i
    _sample['spider_id'] = i
    _sample['substituted_db_id'] = _sample['db_id']
    _sample['substituted_sql'] = _sample['sql']
    _sample['substituted_question'] = _sample['question']
    _sample['substituted_query'] = _sample['query']
    _sample['paraphrased_question'] = _sample['question']
    new_sample = deepcopy(_sample)
    dummy_samples.append(new_sample)


with open(SAMPLES_PARAPHRASED_PATH, 'w') as samples_file:
    json.dump(dummy_samples, samples_file)