import json
from configure import *

with open(SAMPLES_JSON, 'r') as samples_file:
    samples = json.load(samples_file)

for i, _sample in enumerate(samples):
    _sample['id'] = i
    _sample['spider_id'] = i
    _sample['substituted_question'] = _sample['question']
    _sample['substituted_query'] = _sample['query']
    _sample['paraphrased_question'] = _sample['question']


with open(SAMPLES_PARAPHRASED_PATH, 'w') as samples_file:
    json.dump(samples, samples_file)