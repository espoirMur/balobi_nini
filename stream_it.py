import streamlit as st
from visualisation.terms_count import get_term_count
import matplotlib.pyplot as plt
from visualisation.plots_figures import generate_word_cloud, drc_flag_color_map

terms_counts = get_term_count()
wordcloud = generate_word_cloud(terms_counts, drc_flag_color_map)
st.title('Most Discussed word on Twitter')
plt.figure(figsize=(34, 28))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot()
