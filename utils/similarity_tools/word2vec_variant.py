import os
import gensim
from typing import *
import pymorphy2
import wget
import tarfile
from nltk.stem.porter import *
import fasttext.util
from scipy.spatial import distance
import gzip
import shutil
from utils.preprocessing.text import *
from configure import *
# from gensim.models.wrappers import FastText

from dto.sample import Language


class SimilarityDefiner:
    def __init__(self):
        self.load_models()
        self.embedders = {
            # Language.EN: fasttext.load_model(EN_EMBEDDING_MODEL_PATH),
            Language.RU: gensim.models.KeyedVectors.load_word2vec_format(RU_EMBEDDING_MODEL_PATH)
        }
        self.embedders[Language.RU].init_sims()
        print("Embedders were loaded.")
        # fasttext.load_model(EN_EMBEDDING_MODEL_PATH)
        # self.russian_embedder = gensim.models.KeyedVectors.load(RU_EMBEDDING_MODEL_PATH)
        # self.russian_embedder = FastText.load_fasttext_format(RU_EMBEDDING_MODEL_PATH)
        # self.russian_embedder.init_sims(replace=True)
        # self.english_embedder = gensim.models.KeyedVectors.load_word2vec_format("ruwikiruscorpora_0_300_20.bin.gz", binary=True)
        # self.english_embedder.init_sims(replace=True)
        self.russian_morpher = pymorphy2.MorphAnalyzer()
        self.english_stemmer = PorterStemmer()

    def load_models(self):
        # self.load_english_model()
        self.load_russian_model()

    def load_russian_model(self):
        print(0)
        if not os.path.exists(RU_EMBEDDING_MODEL_DIR):
            print(1)
            os.mkdir(RU_EMBEDDING_MODEL_DIR)
        if not os.path.exists(RU_EMBEDDING_MODEL_ARCHIVE):
            print(2)
            _ = wget.download(RU_EMBEDDING_MODEL_URL, out=RU_EMBEDDING_MODEL_ARCHIVE)
        if not os.path.exists(RU_EMBEDDING_MODEL_PATH):
            print(3)
            with gzip.open(RU_EMBEDDING_MODEL_ARCHIVE, 'rb') as f_in:
                with open(RU_EMBEDDING_MODEL_PATH, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        print(4)


            # file = tarfile.open(RU_EMBEDDING_MODEL_ARCHIVE)
            # file.extractall(RU_EMBEDDING_MODEL_DIR)
            # file.close()

    def load_english_model(self):
        if not os.path.exists(EN_EMBEDDING_MODEL_DIR):
            os.mkdir(EN_EMBEDDING_MODEL_DIR)
        if not os.path.exists(EN_EMBEDDING_MODEL_PATH):
            fasttext.util.download_model('en', if_exists='ignore')
            model = fasttext.load_model(EN_EMBEDDING_MODEL)
            model.save_model(EN_EMBEDDING_MODEL_PATH)

        # if not os.path.exists(RU_EMBEDDING_MODEL_ARCHIVE):
        #     _ = wget.download(RU_EMBEDDING_MODEL_URL, out=RU_EMBEDDING_MODEL_ARCHIVE)
        # if not os.path.exists(RU_EMBEDDING_MODEL_PATH):
        #     file = tarfile.open(RU_EMBEDDING_MODEL_ARCHIVE)
        #     file.extractall(RU_EMBEDDING_MODEL_DIR)
        #     file.close()

    def get_edit_distance(self, token_1: str, token_2: str) -> float:
        pass

    def get_semantic_similarity(self, language: Language, token_1: str, token_2: str) -> float:
        embedder = self.embedders[language]
        processed_1 = db_token_process(token_1, Language.RU)
        processed_2 = db_token_process(token_2, Language.RU)
        info_1 = f'{processed_1}_NOUN'
        info_2 = f'{processed_2}_NOUN'
        similarity = embedder.similarity(info_1, info_2)
        return similarity



if __name__ == "__main__":
    definer = SimilarityDefiner()

    # en_word_1 = "profit"
    # en_candidates_1 = ["profit", "profi", "income", "earning", "money", "company", "cat", "of", "blups"]
    # for candidate in en_candidates_1:
    #     sim_d = definer.get_semantic_distance(Language.EN, en_word_1, candidate)
    #     edit_d = 0
    #     # edit_d = definer.get_edit_distance(en_word_1, candidate)
    #     print(f"{en_word_1} : {candidate} = {sim_d} | {edit_d}")
    #
    # en_word_2 = "profits"
    # for candidate in en_candidates_1:
    #     sim_d = definer.get_semantic_distance(Language.EN, en_word_2, candidate)
    #     # edit_d = definer.get_edit_distance(en_word_2, candidate)
    #     edit_d = 0
    #     print(f"{en_word_2} : {candidate} = {sim_d} | {edit_d}")

    ru_word_1 = "прибыль"
    ru_candidates_1 = ["прибыль", "прибыл", "прибытие", "заработок", "маржа", "деньги", "кошка", "из", "мюмзя"]
    for candidate in ru_candidates_1:
        sim_d = definer.get_semantic_similarity(Language.RU, ru_word_1, candidate)
        edit_d = 0
        # edit_d = definer.get_edit_distance(ru_word_1, candidate)
        print(f"{ru_word_1} : {candidate} = {sim_d} | {edit_d}")

    ru_word_2 = "прибылями"
    for candidate in ru_candidates_1:
        sim_d = definer.get_semantic_similarity(Language.RU, ru_word_2, candidate)
        edit_d = 0
        # edit_d = definer.get_edit_distance(ru_word_2, candidate)
        print(f"{ru_word_2} : {candidate} = {sim_d} | {edit_d}")