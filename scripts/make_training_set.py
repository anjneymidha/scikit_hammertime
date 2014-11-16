"""
Script: make_training_set.py
============================

Description:
------------

	Goes from preprocessed dfs to a set of documents 
	mapping sets of words to their labels


Arguments:
----------

	-i (--input): input directory
	-o (--output): output file

Usage:
------

	python preprocess.py -i $DATA_DIR -o data.df

##################
Jay Hack
jhack@stanford.edu
Fall 2014
##################
"""
import os
import pickle
import pandas as pd
from scikit_hammertime import *

def get_all_pairs(df, valid_words):
	"""
		given a dataframe, gathers all pairs that occur together 
		and maps them to their adverse effects 
	"""
	print '-----> Getting positive examples'
	pairs, rows = [], []
	for row in df.iterrows():



def make_training_set(input_dir='/data/aers/formatted', output_dir='/data/aers/training', num_dfs=1):

	#=====[ Step 1: load in dataframes to 'data'	]=====
	data = load_data(num_dfs=1, data_dir=input_dir, verbose=True)





if __name__ == '__main__':






