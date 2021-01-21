#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: my-word-to-vec.py
# Author: #cf
# Version 0.2.0 (2016-10-08)

from pathlib import Path
"""
Function to build word2vec models from text files using gensim.
https://rare-technologies.com/word2vec-tutorial/
"""


##################
# Parameters
##################

WorkDir = Path.cwd()
TextDir = WorkDir.joinpath("data", "frwiki")
ModelFile = WorkDir.joinpath("models", "frwiki.gensim") 
Size = 500 # dimensions of the model



##################
# Imports
##################

import os
import re
import gensim 
import logging

print("gensim", gensim.__version__)

##################
# Functions
##################



def extract_sentences(TextPath): 
    """
    Turns a collection of plain text files into a list of lists of word tokens.
    """
    print("--extract_sentences")
    Sentences = []
    for File in os.listdir(TextDir):
        with open(File, "r") as InFile: 
            Text = InFile.read()
            Text = re.sub("\n", " ", Text)
            Text = re.sub("--", "", Text)
            Text = re.sub("\.\.\.", ".", Text)
            Text = Text.lower()
            SentencesOne = []
            Text = re.split("[.!?]", Text)
            for Sent in Text: 
                Sent = re.split("\W", Sent)
                Sent = [Token for Token in Sent if Token]
                SentencesOne.append(Sent)  
            Sentences.extend(SentencesOne)
    return Sentences



def build_model(TextDir, ModelFile): 
    """
    Builds a word vector model of the text files given as input.
    This should be used for very large collections of text, as it is very memory-friendly.
    """
    print("--build_model_new")
    
    class MySentences(object):
        def __init__(self, dirname):
            self.dirname = dirname
        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for Para in open(os.path.join(self.dirname, fname)):
                    if "<doc id" not in Para and "</doc>" not in Para:
                        Sentences = re.split("[.!?]", Para)
                        for Sent in Sentences:
                            Sent = re.split("\W", Sent)
                            Sent = [Token.lower() for Token in Sent if Token]
                            Sent = [Token for Token in Sent if len(Token) > 2]
                            if len(Sent) > 1: 
                                #print(Sent)
                                yield Sent
 
    Sentences = MySentences(TextDir) # a memory-friendly iterator
    Model = gensim.models.Word2Vec(Sentences, min_count=10, size=Size, workers=2)
    Model.save(ModelFile)


################
# Main function
################

def main(TextDir, Size, ModelFile):
    print("Launched.")
    logging.basicConfig(filename="logging.txt", level=logging.INFO)
    build_model(TextDir, ModelFile)
    print("Done.")
    
main(TextDir, Size, ModelFile)
