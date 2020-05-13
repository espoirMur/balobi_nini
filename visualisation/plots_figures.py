import pickle
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.colors as colors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime


drc_flag_color_map = colors.LinearSegmentedColormap.from_list("", ["#0080FF",
                                                                   "#0080FF",
                                                                   "#D00F20",
                                                                   "#D00F20",
                                                                   "#F5D715",
                                                                   "#F5D715"])


def plot_term_frequency(term_counts, path):
    """
    Plot the term frequencies from  tweet terms  count

    Args:
        term_counts (dict, required): dictionary of terms and their count.
        path (str, required): path where we need to save the file.
    """
    y = [count for tag, count in term_counts.most_common(100)]
    x = range(1, len(y) + 1)
    plt.bar(x, y)
    plt.title("Term frequencies")
    plt.ylabel('frequency')
    plt.savefig(path)


def plot_tweet_time(tweet_path, images_path):
    """
    generate time serie plot for all tweets
    Args:
        tweet_path (string): path of the tweet files
        image_path (str, required): path where we need to save the file.
    """
    all_dates = list()
    for tweet in read_tweets_file(TWEETS_PATH):
        all_dates.append(tweet.get('created_at'))
    idx = pd.DatetimeIndex(all_dates)
    ones = np.ones(len(idx))
    one_second_series = pd.Series(ones, index=idx)
    # Downsample the series into 1 minute bins and sum the values of the
    # timestamps falling into a bin. Basically this helps us to know how many
    # tweet we have in one minute time slot.
    per_minute = one_second_series.resample('1Min').apply(sum).fillna(0)
    plt.figure(figsize=(17, 14))
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_title('tweet frequencies')
    hours = mdates.MinuteLocator(interval=60)
    date_formatter = mdates.DateFormatter('%H:%M')
    max_date = idx.max()
    min_date = idx.min()
    max_freq = per_minute.max()
    ax.set_ylim(0, max_freq)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.set_xlim(min_date, max_date)
    ax.plot(per_minute.index, per_minute)
    plt.savefig(images_path)


def generate_word_cloud(term_counts, color_map):
    """
    generate a word_cloud from term count dictionary

    Args:
        term_counts (dict, required): dictionary of terms and their count.
        color_map ([type]): color map to use in the word_cloud

    Returns:
        wordCould: an worldcould
    """
    return WordCloud(
        width=900,
        height=500,
        max_words=500,
        max_font_size=100,
        relative_scaling=0.5,
        colormap=color_map,
        normalize_plurals=True).generate_from_frequencies(term_counts)


def plot_word_cloud(word_cloud, path):
    """
    Args:
        word_cloud (wordCloud): the wordcloud to plot
        path ([type]): path where we save the plot
    Returns :

    """
    plt.figure(figsize=(17, 14))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.savefig(__path__)
    plt.axis("off")
    plt.show()
