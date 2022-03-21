import re
import pymorphy2
from typing import *
from dto.sample import *
import nltk
from nltk.stem.porter import *

ru_morpher = pymorphy2.MorphAnalyzer()
en_stemmer = PorterStemmer()


def sample_token_processing(token):
    processed = token.lower()
    processed = re.sub("[\'\"]+", '', processed)
    # processed = processed.replace('\'', "")
    # processed = processed.replace("\"", "")
    # processed = processed.replace("\'", "")
    return processed


def db_token_process(token: str, language: Optional[Language]=None) -> str:
    processed = token.lower()
    if language is Language.RU:
        parsing = ru_morpher.parse(processed)
        if parsing and len(parsing) > 0:
            processed = ru_morpher.parse(processed)[0].word
    if language is Language.EN:
        processed = en_stemmer.stem(processed)
    return processed


if __name__ == "__main__":
    p = db_token_process("Стали", Language.RU)
    q = db_token_process("Singers", Language.EN)
    print(p)
    print(q)