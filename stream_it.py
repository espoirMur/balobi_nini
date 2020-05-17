import streamlit as st
import numpy as np
import pandas as pd
from visualisation.terms_count import get_term_count
from wordcloud import WordCloud
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from visualisation.plots_figures import generate_word_cloud, drc_flag_color_map

terms_counts = get_term_count()
wordcloud = generate_word_cloud(terms_counts, drc_flag_color_map)
st.title('Most Discussed word on Twitter')
plt.figure(figsize=(34, 28))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot()
