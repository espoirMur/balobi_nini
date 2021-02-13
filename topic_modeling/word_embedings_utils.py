import numpy as np
from pathlib import Path
from gensim.models.fasttext import FastText as FT_gensim
from gensim.test.utils import datapath


class WordEmbeddingUtils:
    """
    This contains utilities to manage words embeddings.
    """
    def __init__(self):
        super().__init__()
        self.read_wv_model()

    def read_wv_model(self, model_name='embeddings_one_gram_fast_tweets_only'):
        """
        read the word to vv embedding model passed in parameter

        Args:
            path ([type]): [description]
        """
        model_path = Path.cwd().joinpath('models', model_name).__str__()
        self.model_gensim = FT_gensim.load(model_path)

    def check_bigram(self, word):
        """
        check if the given word passed in parameter is a bigram or not
        """
        if len(word.split(' ')) == 2:
            return True
        return False
    
    def get_bi_grams_vector(self, string):
        """
        get the vector of the bigram passed in parameter,
        this is done by using the average of the two words building the vector

        Args:
            string ([type]): [description]

        Returns:
            [type]: [description]
        """
        word1, words2 = string.split(' ')
        bigram_vector = np.mean([self.model_gensim.wv.get_vector(word1),
                                 self.model_gensim.wv.get_vector(words2)],
                                axis=0)
        return bigram_vector

    def compute_cosine_similarity(self, words):
        """
        This code use numpy to compute the
        cosine similarity between two given vectors
        params:
        words : a 2 d array with 2 words we are calculating the similarity for
        """
        word_1, word_2 = words[0], words[1]
        vector_1 = self.get_word_vector(word_1)
        vector_2 = self.get_word_vector(word_2)
        ma = np.linalg.norm(vector_1)
        mb = np.linalg.norm(vector_2)
        cosine_distance = (np.matmul(vector_1, vector_2))/(ma*mb)
        return cosine_distance

    def get_word_vector(self, word):
        """
        return the word vector for the corresponding word or bigram

        Args:
            word ([type]): [description]
        """
        if self.check_bigram(word):
            return self.get_bi_grams_vector(word)
        return self.model_gensim.wv.get_vector(word)

