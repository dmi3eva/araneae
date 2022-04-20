
import os
import gensim
from typing import *
import pymorphy2
import wget
import tarfile
from nltk.stem.porter import *
import fasttext.util
from scipy.spatial import distance
from utils.preprocessing.text import *
from configure import *
# from gensim.models.wrappers import FastText



from dto.sample import Language


class SimilarityDefiner:
    def __init__(self):
        self.load_models()
        self.embedders = {
            Language.EN: fasttext.load_model(EN_EMBEDDING_MODEL_PATH)
        }
        fasttext.load_model(EN_EMBEDDING_MODEL_PATH)
        # self.russian_embedder = gensim.models.KeyedVectors.load(RU_EMBEDDING_MODEL_PATH)
        # self.russian_embedder = FastText.load_fasttext_format(RU_EMBEDDING_MODEL_PATH)
        # self.russian_embedder.init_sims(replace=True)
        # self.english_embedder = gensim.models.KeyedVectors.load_word2vec_format("ruwikiruscorpora_0_300_20.bin.gz", binary=True)
        # self.english_embedder.init_sims(replace=True)
        self.russian_morpher = pymorphy2.MorphAnalyzer()
        self.english_stemmer = PorterStemmer()

    def load_models(self):
        self.load_english_model()
        # self.load_russian_model()


    def load_russian_model(self):
        if not os.path.exists(RU_EMBEDDING_MODEL_DIR):
            os.mkdir(RU_EMBEDDING_MODEL_DIR)
        if not os.path.exists(RU_EMBEDDING_MODEL_ARCHIVE):
            _ = wget.download(RU_EMBEDDING_MODEL_URL, out=RU_EMBEDDING_MODEL_ARCHIVE)
        if not os.path.exists(RU_EMBEDDING_MODEL_PATH):
            file = tarfile.open(RU_EMBEDDING_MODEL_ARCHIVE)
            file.extractall(RU_EMBEDDING_MODEL_DIR)
            file.close()

    def load_english_model(self):
        if not os.path.exists(EN_EMBEDDING_MODEL_DIR):
            os.mkdir(EN_EMBEDDING_MODEL_DIR)
        if not os.path.exists(EN_EMBEDDING_MODEL_PATH):
            print("Hi")
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
        initial_1 = self.english_stemmer.stem(token_1)
        initial_2 = self.english_stemmer.stem(token_2)
        vector_1 = embedder.get_word_vector(initial_1)
        vector_2 = embedder.get_word_vector(initial_2)
        similarity = 1 - distance.cosine(vector_1, vector_2)
        return similarity




if __name__ == "__main__":
    definer = SimilarityDefiner()

    en_word_1 = "profit"
    en_candidates_1 = ["profit", "profi", "income", "earning", "money", "company", "cat", "of", "blups"]
    for candidate in en_candidates_1:
        sim_d = definer.get_semantic_similarity(Language.EN, en_word_1, candidate)
        edit_d = 0
        # edit_d = definer.get_edit_distance(en_word_1, candidate)
        print(f"{en_word_1} : {candidate} = {sim_d} | {edit_d}")

    en_word_2 = "profits"
    for candidate in en_candidates_1:
        sim_d = definer.get_semantic_similarity(Language.EN, en_word_2, candidate)
        # edit_d = definer.get_edit_distance(en_word_2, candidate)
        edit_d = 0
        print(f"{en_word_2} : {candidate} = {sim_d} | {edit_d}")

    # ru_word_1 = "прибыль"
    # ru_candidates_1 = ["прибыль", "прибыл", "прибытие", "заработок", "маржа", "деньги", "кошка", "из", "мюмзя"]
    # for candidate in ru_candidates_1:
    #     sim_d = definer.get_semantic_distance(ru_word_1, candidate)
    #     edit_d = definer.get_edit_distance(ru_word_1, candidate)
    #     print(f"{ru_word_1} : {candidate} = {sim_d} | {edit_d}")
    #
    # ru_word_2 = "прибылями"
    # for candidate in ru_candidates_1:
    #     sim_d = definer.get_semantic_distance(ru_word_2, candidate)
    #     edit_d = definer.get_edit_distance(ru_word_2, candidate)
    #     print(f"{ru_word_2} : {candidate} = {sim_d} | {edit_d}")