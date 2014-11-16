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
from collections import defaultdict
from itertools import combinations
import random
import pandas as pd
from scikit_hammertime import *


def get_X_y_positive(df):
	"""
		given a dataframe, gathers all pairs that occur together 
		and maps them to their adverse effects 
	"""
	print '-----> Getting positive examples'
	DRUGs, REACs = [], []
	for ix, row in df.iterrows():

		#=====[ Only looking at combos of drugs	]=====
		if not len(row.DRUG) >= 2 and len(row.DRUG) <= 4:
			continue

		combos = list(combinations(row.DRUG, 2))
		DRUGs += combos
		REACs += [row.REAC]*len(combos)

	return DRUGs, REACs


def get_X_y_positive_paragraph(df):
	"""
		gets paragraph vec version of X_y
	"""
	print '-----> Getting positive examples'
	DRUGs = list(df.DRUG)
	REACs = list(df.REAC)
	return DRUGs, REACs



def get_cooccurrences(df):
	"""
		given a dataframe, returns
			dict: Words -> Set of co-occurring words
	"""
	print '-----> Getting co-occurrences'
	co_occurrence = defaultdict(lambda: set([]))
	for ix, row in df.iterrows():

		drugs = row.DRUG
		for i in range(len(drugs)):
			for w in drugs[:i] + drugs[i+1:]:
				co_occurrence[drugs[i]].add(w)

	return co_occurrence


def get_X_y_negative(df, cooccurrences, num_samples):
	"""
		given a dataframe, returns sets that never 
		occurred together
	"""
	print '-----> Getting negative examples'
	DRUGs_neg = []
	for i in range(num_samples):
		d1 = random.choice(cooccurrences.keys())
		d2 = random.choice(cooccurrences.keys())
		while d2 == d1 or d2 in cooccurrences[d1]:
			d2 = random.choice(cooccurrences.keys())
		DRUGs_neg.append((d1, d2))
	
		if i % 1000 == 0:
			print '	%d' % i
	

	REACs_neg = [[]]*len(DRUGs_neg)

	return DRUGs_neg, REACs_neg


def get_X_y_negative_paragraph(df, cooccurrences, num_samples):
	"""
		given a dataframe, returns sets that never 
		occurred together
	"""
	print '-----> Getting negative examples'
	DRUGs_neg = []
	for i in range(num_samples):

		num_elements = 

		d1 = random.choice(cooccurrences.keys())
		d2 = random.choice(cooccurrences.keys())
		while d2 == d1 or d2 in cooccurrences[d1]:
			d2 = random.choice(cooccurrences.keys())
		DRUGs_neg.append((d1, d2))
	
		if i % 1000 == 0:
			print '	%d' % i
	

	REACs_neg = [[]]*len(DRUGs_neg)

	return DRUGs_neg, REACs_neg


def make_training_set(input_dir='/data/aers/formatted', output_dir='/data/aers/training', num_dfs=1):
	"""
		returns DRUGS, REACs
		DRUGs: list of tuples of DRUGs that either occur together or dont 
		REACs: list of reactions that occur when they occur together 
	"""

	#=====[ Step 1: load in dataframes to 'data'	]=====
	data = load_data(num_dfs=1, data_dir=input_dir, verbose=True)

	#=====[ Step 3: get positive examples	]=====
	DRUGs_pos, REACs_pos = get_X_y_positive(data)

	#=====[ Step 4: get negative examples	]=====
	co_occurrences = get_cooccurrences(data)
	DRUGs_neg, REACs_neg = get_X_y_negative(data, co_occurrences, 250000)

	return DRUGs_neg + DRUGs_pos, REACs_neg + REACs_pos








if __name__ == '__main__':

	DRUGs, REACs = make_training_set()
	print '-----> Saving to pickle'
	pickle.dump(DRUGs, open('DRUGs.pkl', 'w'))
	pickle.dump(REACs, open('REACs.pkl', 'w'))	




