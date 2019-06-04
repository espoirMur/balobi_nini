import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF


def create_topic_model(tweet_df, number_of_topics):
    """
    train an LDA model

    Args:
        tweet_df (dataframe): cleaned tweets to use while training
        number_of_topics (int): number of topics to use in the model

    Returns:
        LDAModel : trained lda model
        np array : features names
    """
    vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=5,
        token_pattern=r'\w+|\$[\d\.]+|\S+')
    transfromed_tweets = vectorizer.fit_transform(
        tweets_df.get('cleanned_tweet'))
    tf_feature_names = vectorizer.get_feature_names()
    topic_modeling_model = LatentDirichletAllocation(
        n_components=number_of_topics, random_state=0, max_iter=200)
    topic_modeling_model.fit(transfromed_tweets)
    return topic_modeling_model, tf_feature_names


def display_topics(model, feature_names, no_top_words):
    """

    Args:
        model : trained LDA models
        feature_names (np.array): array of features names
        no_top_words (int): number of top words per topic

    Returns:
        dataframe: word topic and weight dataframe
    """
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(
            feature_names[i]) for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(
            topic[i]) for i in topic.argsort()[:-no_top_words - 1:-1]]
    return pd.DataFrame(topic_dict)


def generate_visualization(lda_model, transfromed_tweets, vectorizer):
    """
    generate topic visualisation

    Args:
        lda_model ([type]):
        transfromed_tweets ([type]): [description]
        vectorizer ([type]): [description]
    """
    import pyLDAvis.sklearn
    pyLDAvis.enable_notebook()
    panel = pyLDAvis.sklearn.prepare(
        lda_model,
        transfromed_tweets,
        vectorizer,
        mds='tsne',
        sort=False)
    return panel
