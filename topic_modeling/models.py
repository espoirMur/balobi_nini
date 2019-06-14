import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF


def vectorize_tweets(tweets_df,):
    """
    Return a vectorize version of tweets
    Args:
        tweest_df (dataframe): a dataframe  of cleanned tweets
    Returns :
    np array : features names
    np array : transformed_tweet tweet transformed
    np array : count vectorizer for the cleanned tweets
    """
    vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=5,
        token_pattern=r'\w+|\$[\d\.]+|\S+')
    transformed_tweets = vectorizer.fit_transform(
        tweets_df.get('cleanned_tweet'))
    tf_feature_names = vectorizer.get_feature_names()
    return tf_feature_names, transformed_tweets, vectorizer


def create_topic_model(transformed_tweets, number_of_topics, is_lda=True):
    """
    train an LDA model

    Args:
        transformed_tweets (np.array): matrix document and world count
        number_of_topics (int): number of topics to use in the model
        is_lda (boolean) default True: the model to use

    Returns:
        Model : trained lda model
    """
    model = None
    if is_lda:
        topic_modeling_model = LatentDirichletAllocation(
            n_components=number_of_topics, random_state=0, max_iter=200)
        topic_modeling_model.fit(transformed_tweets)
        model = topic_modeling_model
    else:
        topic_model_nmf = NMF(
            n_components=number_of_topics,
            random_state=0,
            alpha=.1,
            l1_ratio=.5)
        topic_model_nmf.fit(transformed_tweets)
        model = topic_model_nmf
    return model


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
        lda_model (LDA model): model to genrate a visualization for
        transfromed_tweets (np array): tweet matrix
        vectorizer (): [description]
    """
    import pyLDAvis.sklearn
    pyLDAvis.enable_notebook()
    panel = pyLDAvis.sklearn.prepare(
        lda_model,
        transfromed_tweets,
        vectorizer,
        mds='tsne')
    return panel
