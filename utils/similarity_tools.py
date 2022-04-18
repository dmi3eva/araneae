from typing import *
import gensim
import pymorphy2
from nltk.stem.porter import *


from dto.sample import Language


class SimilarityDefiner:
    def __init__(self):
        self.russian_embedder = gensim.models.KeyedVectors.load_word2vec_format("ruwikiruscorpora_0_300_20.bin.gz", binary=True)
        self.russian_embedder.init_sims(replace=True)
        self.english_embedder = gensim.models.KeyedVectors.load_word2vec_format("ruwikiruscorpora_0_300_20.bin.gz", binary=True)
        self.english_embedder.init_sims(replace=True)
        self.russian_morpher = pymorphy2.MorphAnalyzer()
        self.english_stemmer = PorterStemmer()

    def get_edit_distance(self, token_1: str, token_2: str, language: Language) -> float:
        pass

    def get_semantic_distance(self, token_1: str, token_2: str, language: Language) -> float:
        pass


if __name__ == "__main__":
    definer = SimilarityDefiner()

    en_word_1 = "profit"
    en_candidates_1 = ["profit", "profi", "income", "earning", "money", "company", "cat", "of", "blups"]
    for candidate in en_candidates_1:
        sim_d = definer.get_semantic_distance(en_word_1, candidate)
        edit_d = definer.get_edit_distance(en_word_1, candidate)
        print(f"{en_word_1} : {candidate} = {sim_d} | {edit_d}")

    ru_word_1 = "прибыль"
    ru_candidates_1 = ["прибыль", "прибыл", "прибытие", "заработок", "маржа", "деньги", "кошка", "из", "мюмзя"]
    for candidate in ru_candidates_1:
        sim_d = definer.get_semantic_distance(ru_word_1, candidate)
        edit_d = definer.get_edit_distance(ru_word_1, candidate)
        print(f"{ru_word_1} : {candidate} = {sim_d} | {edit_d}")