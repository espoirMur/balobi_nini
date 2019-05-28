#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# In this notebook I'm going to analyse the tweet collected and the the most used hashtags by congolese on twitter
# For now a simple defintion of a congolese on social media is someone who tweet using the following hashtags : DRC, RDC, RDCongo, DRCongo.

#%%
import sys
from collections import Counter
import json

#%% [markdown]
# Let analyse a tweet and get the hashtags involed in the tweet


#%%

def get_hashtags(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [tag.get('text').lower() for tag in hashtags]
