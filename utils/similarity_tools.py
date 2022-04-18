
import os
import gensim
from typing import *
import pymorphy2
import wget
import tarfile
from nltk.stem.porter import *
from configure import *
# from gensim.models.wrappers import FastText


from dto.sample import Language


class SimilarityDefiner:
    def __init__(self):
        self.load_models()
        self.russian_embedder = gensim.models.KeyedVectors.load(RU_EMBEDDING_MODEL_PATH)
        # self.russian_embedder = FastText.load_fasttext_format(RU_EMBEDDING_MODEL_PATH)
        self.russian_embedder.init_sims(replace=True)
        # self.english_embedder = gensim.models.KeyedVectors.load_word2vec_format("ruwikiruscorpora_0_300_20.bin.gz", binary=True)
        # self.english_embedder.init_sims(replace=True)
        self.russian_morpher = pymorphy2.MorphAnalyzer()
        self.english_stemmer = PorterStemmer()

    def load_models(self):
        self.load_russian_model()

    def load_russian_model(self):
        if not os.path.exists(RU_EMBEDDING_MODEL_DIR):
            os.mkdir(RU_EMBEDDING_MODEL_DIR)
        if not os.path.exists(RU_EMBEDDING_MODEL_ARCHIVE):
            _ = wget.download(RU_EMBEDDING_MODEL_URL, out=RU_EMBEDDING_MODEL_ARCHIVE)
        if not os.path.exists(RU_EMBEDDING_MODEL_PATH):
            file = tarfile.open(RU_EMBEDDING_MODEL_ARCHIVE)
            file.extractall(RU_EMBEDDING_MODEL_DIR)
            file.close()




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