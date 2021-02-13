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
from topic_modeling.topic_modeling import TopicModelNMF
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

    def plot_all_coherence(self):
        """
        plot for all windows topic model the evolution of coherence measure
        """
        fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(8, 4))
        axes = axes.flatten()
        for coherence_k, axe, topic_model in zip(self.all_coherence, axes, self.all_topic_models):
            topic_model.get('topic_model').plot_topic_coherence(coherence_k, axe)
    
    def generate_all_topic_models(self):
        """
        compute topic modeling for all the time windows in the dataframe,s
        """

        all_coherence = []
        all_topic_models = list()
        for window_data in self.windows_data[:2]:
            topic_model = TopicModelNMF(window_data)
            topic_model.create_topic_model()
            topic_model.get_best_coherence()
            topic_model.get_best_model()
            terms = topic_model.terms
            coherence_k = topic_model.coherence_k
            best_coherence = topic_model.best_k
            all_topic_models.append({"terms": terms,
                                     "topic_model": topic_model,
                                     "best_k": best_coherence})
            all_coherence.append(coherence_k)
        self.all_coherence = all_coherence
        self.all_topic_models = all_topic_models

    def build_time_windows_matrix(self):
        """
        this build the $B$ matrix for the dynamic topic modelling
        """
        all_topic_matrix = list()
        for topic_model in self.all_topic_models:
            H = topic_model.H
            terms = topic_model.terms
            topic_model.get_top_terms_per_model
            top_terms = topic_model.top_terms
            all_topic_matrix.append(top_terms)
        self.B_matrix = np.concatenate(all_topic_matrix, axis=0)

