from datetime import datetime
from pathlib import Path

import matplotlib.colors as colors
from wordcloud import WordCloud

drc_flag_color_map = colors.LinearSegmentedColormap.from_list(
    "", ["#0080FF", "#0080FF", "#D00F20", "#D00F20", "#F5D715", "#F5D715"]
)


def generate_word_cloud(term_counts, color_map):
    """
    generate a word_cloud from term count dictionary

    Args:
        term_counts (dict, required): dictionary of terms and their count.
        color_map ([type]): color map to use in the word_cloud

    Returns:
        wordCould: an worldcould
    """
    world_cloud = WordCloud(
        width=900,
        height=500,
        max_words=500,
        max_font_size=100,
        relative_scaling=0.5,
        colormap=color_map,
        normalize_plurals=True,
    )
    world_cloud_image = world_cloud.generate_from_frequencies(term_counts)

    return save_world_cloud_image_to_file(world_cloud_image)


def save_world_cloud_image_to_file(world_cloud_image):
    """save the world cloud image to a file

    Args:
        world_cloud_image (_type_): _description_
    """
    today = datetime.today().strftime("%m-%d-%Y")
    file_name = f"word_cloud_{today}.png"
    path = Path.cwd().joinpath("world_cloud", file_name)
    world_cloud_image.to_file(path)
    return path
