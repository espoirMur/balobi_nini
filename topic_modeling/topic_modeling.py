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
from topic_modeling.word_embedings_utils import WordEmbeddingUtils
from itertools import combinations
import matplotlib
import matplotlib.pyplot as plt
plt.style.use("ggplot")
matplotlib.rcParams.update({"font.size": 14})


class TopicModelNMF:
    def __init__(self, corpus_dataframe):
        self.corpus_dataframe = corpus_dataframe
        self.word_embeddings = WordEmbeddingUtils()
        super().__init__()
    
    def create_topic_model(self, ngram_range=(1, 2)):
        """
        given a a dataframe of time windows generate an array of topic models
        return the list of all terms and the list of different topics models
        for different k
        """
        vectorizer = TfidfVectorizer(lowercase=True,
                                     strip_accents="unicode",
                                     ngram_range=ngram_range)
        doc_term_matrix = vectorizer\
            .fit_transform(self.corpus_dataframe.cleanned_text.dropna())
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
        self.topic_models = topic_models
        self.terms = terms
    
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
        
        for term_index in top_indices[0:top]:
            yield (terms[term_index], H[topic_index, term_index].round(2))

    def calculate_topic_coherence(self, topic_descriptor):
        """
        take the term ranking and compute the coherence between the term
        """
        topics_terms = [x[0] for x in topic_descriptor]
        pairs_array = np.array(list(combinations(topics_terms, 2)))
        pairs_vectors = np.apply_along_axis(self.word_embeddings.compute_cosine_similarity, 
                                            1,
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

    def get_best_coherence(self):
        """
        return a dict of the k
        and the coresponding topic for ploting purpose
        """
        coherences_k = dict()
        for (k, W, H) in self.topic_models:
            coherence = self.compute_overhall_topic_coherence(H, self.terms)
            coherences_k[k] = coherence
            print("for k = {} the coherence is {:.2f}".format(k, coherence))
        best_coherence = max(coherences_k, key=coherences_k.get)
        self.best_k = best_coherence
        self.coherence_k = coherences_k
    
    def get_best_model(self):
        """
        loop trough all the topic models and return the
        best one with the coresponding terms
        """
        best_k = self.best_k
        best_model = self.topic_models[best_k-4]
        assert best_model[0] == best_k
        H = best_model[2]
        self.H = H
    
    def get_top_terms_per_model(self, top_terms=15):
        '''
        return the top term per matrix
        '''
        top_indices = np.flip(np.argsort(self.H))
        terms_array = np.array(self.terms, dtype=np.str)
        top_terms = np.take(terms_array, top_indices)[::-1, :top_terms]
        self.top_terms = top_terms

