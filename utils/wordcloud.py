from typing import Dict, List

from visualisation.plots_figures import drc_flag_color_map, generate_word_cloud
from visualisation.terms_count import get_term_count


def generate_today_word_cloud(cleaned_tweets: List[Dict]):
    """
    generate today word cloud

    Args:
        path (str, optional): [description]. Defaults to 'images/'.
    """
    terms_counts = get_term_count(cleaned_tweets)
    if terms_counts:
        word_cloud = generate_word_cloud(terms_counts, drc_flag_color_map)
        return word_cloud
