"""
this package hold the code for the dynamic topic modeling with the nmf
"""
import pandas as pd
import numpy as np
from pathlib import Path
from gensim.models.fasttext import FastText as FT_gensim
from gensim.test.utils import datapath
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from itertools import combinations
import matplotlib
import matplotlib.pyplot as plt
plt.style.use("ggplot")
matplotlib.rcParams.update({"font.size": 14})


class DynamicNMF:
    def __init__(self):
        self.read_data()
        self.min_date = self.data.created_at.min().strftime('%d-%b-%Y')
        self.max_date = self.data.created_at.max().strftime('%d-%b-%Y')
        self.split_into_windows_docs()

    def read_data(self, dataset_name='cleanned_tweets_2021.csv'):
        """
        read the dataset and return it in a pandas dataframe

        Args:
            dataset_name (str, optional): [description]. Defaults to
            'cleanned_tweets_2021.csv'.
        """
        self.data_path = Path.cwd().joinpath('data', dataset_name)
        self.data = pd.read_csv(self.data_path, index_col='id', 
                                parse_dates=['created_at'])
        self.data = self.data[['created_at', 'cleanned_text']]
    
    def split_into_windows_docs(self, freq='1W'):
        """
        split the data into different windows document of the given length

        Args:
            freq (str, optional): [description]. Defaults to '1W'.
        """
        self.windows_groups = self.data.groupby(pd.Grouper(key="created_at",
                                                           freq=freq))
        self.windows_data = [df for time, df in self.windows_groups if not df.empty]

    def get_top_terms_per_model(self, H, terms, top_terms=15):
        '''
        given an H matrix and the terms return n tops terms
        in for each topic in the matrix in
        '''
        top_indices = np.flip(np.argsort(H))
        terms_array = np.array(terms, dtype=np.str)
        top_terms = np.take(terms_array, top_indices)[::-1, :top_terms]
        return top_terms
    
    def create_topic_model(self, windows_doc):
        """
        given a a dataframe of time windows generate an array of topic models
        return the list of all terms and the list of different topics models
        for different k
        """
        vectorizer = TfidfVectorizer(lowercase=True,
                                     strip_accents="unicode",
                                     ngram_range=(1, 2))
        doc_term_matrix = vectorizer\
            .fit_transform(windows_doc.cleanned_text.dropna())
        terms = vectorizer.get_feature_names()
        k_min = 4
        k_max = 20
        topic_models = []
        # try each value of k
        for k in range(k_min, k_max):
            model = NMF(n_components=k, init="nndsvd", random_state=0)
            W = model.fit_transform(doc_term_matrix)
            H = model.components_
            topic_models.append((k, W, H))
        return {"topic_models": topic_models, "terms": terms}
    
    def get_descriptor(self, terms, H, topic_index, top):
        """
        get the topic descriptor for the given term

        Args:
            terms ([type]): [description]
            H ([type]): [description]
            topic_index ([type]): [description]
            top ([type]): [description]

        Returns:
            [type]: [description]
        """
        # reverse sort the values to sort the indices
        top_indices = np.argsort(H[topic_index, :])[::-1]
        # now get the terms corresponding to the top-ranked indices
        top_terms = []
        for term_index in top_indices[0:top]:
            top_terms.append((terms[term_index], 
                              H[topic_index, term_index].round(2)))
        return top_terms

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
                                 self.model_gensim.wv.get_vector(words2)],\
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

    def calculate_topic_coherence(self, topic_descriptor):
        """
        take the term ranking and compute the coherence between the term
        """
        topics_terms = [x[0] for x in topic_descriptor]
        pairs_array = np.array(list(combinations(topics_terms, 2)))
        pairs_vectors = np.apply_along_axis(self.compute_cosine_similarity, 1,
                                            pairs_array)
        return pairs_vectors.mean()

    def compute_overhall_topic_coherence(self, H, terms):
        '''
        compute the overhall topic coherence for a topic model
        H is the topic term matrix
        '''
        overhall_coherence = []
        for topic_index in range(H.shape[0]):
            topic_descriptor = self.get_descriptor(terms,
                                                   H,
                                                   topic_index, 10)
            coherence = self.calculate_topic_coherence(topic_descriptor)
            overhall_coherence.append(coherence)
        return np.array(overhall_coherence).mean()
    
    def get_best_coherence(self, topic_models, terms):
        """
        return a dict of the k
        and the coresponding topic for ploting purpose
        """
        coherence_k = dict()
        for (k, W, H) in topic_models:
            coherence = self.compute_overhall_topic_coherence(H, terms)
            coherence_k[k] = coherence
            print("for k = {} the coherence is {:.2f}".format(k, coherence))
        return coherence_k
    
    def plot_topic_coherence(self, coherences_k, axe):
        """
        plot the coherence for each k in the topic model
        """
        axe.plot(coherences_k.keys(), coherences_k.values())
        axe.set_xticks(list(coherences_k.keys()))
        axe.set_xlabel("Number of Topics")
        axe.set_ylabel("Mean Coherence")
        # add the points
        axe.scatter(coherences_k.keys(), coherences_k.values(), s=120)
        # find and annotate the maximum point on the plot
        ymax = max(coherences_k.values())
        best_k = max(coherences_k, key=coherences_k.get)
        axe.annotate("k={}".format(best_k),
                     xy=(best_k, ymax),
                     xytext=(best_k, ymax),
                     textcoords="offset points", fontsize=16)

    def plot_all_coherences(self, all_coherences_k):
        """
        plot for all windows topic model the evolution of coherence measure
        """
        fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(8, 4))
        axes = axes.flatten()
        for coherences_k, axe in zip(all_coherences_k, axes):
            self.plot_topic_coherence(coherences_k, axe)
