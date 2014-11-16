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
from collections import defaultdict, Counter
from itertools import combinations
import random
import pandas as pd
from scikit_hammertime import *


def get_legal_drugs(df, num_occurrences=10):
	"""
		returns a set of drugs
	"""
	occurrences = []
	for ix, row in df.iterrows():
		occurrences += row.DRUG
	counts = Counter(occurrences)
	return set([k for k in counts.keys() if counts[k] > num_occurrences])


def get_X_y_positive(df):
	"""
		given a dataframe, gathers all pairs that occur together 
		and maps them to their adverse effects 
	"""
	DRUGs, REACs = [], []
	for ix, row in df.iterrows():

		#=====[ Only looking at combos of drugs	]=====
		if not len(row.DRUG) >= 2 and len(row.DRUG) <= 4:
			continue

		combos = list(combinations(row.DRUG, 2))
		DRUGs += combos
		REACs += [row.REAC]*len(combos)

	return DRUGs, REACs



def get_co_occurrences(df):
	"""
		given a dataframe, returns
			dict: Words -> Set of co-occurring words
	"""
	co_occurrence = defaultdict(lambda: set([]))
	for ix, row in df.iterrows():

		drugs = row.DRUG
		for i in range(len(drugs)):
			for w in drugs[:i] + drugs[i+1:]:
				co_occurrence[drugs[i]].add(w)

	return co_occurrence


def get_X_y_negative(df, co_occurrences, num_samples=250000):
	"""
		given a dataframe, returns sets that never 
		occurred together
	"""
	DRUGs_neg = []
	for i in range(num_samples):
		d1 = random.choice(co_occurrences.keys())
		d2 = random.choice(co_occurrences.keys())
		while d2 == d1 or d2 in co_occurrences[d1]:
			d2 = random.choice(co_occurrences.keys())
		DRUGs_neg.append((d1, d2))
	
		if i % 1000 == 0:
			print '	%d' % i
	

	REACs_neg = [[]]*len(DRUGs_neg)

	return DRUGs_neg, REACs_neg










if __name__ == '__main__':

	#=====[ Step 1: load in dataframes to 'data'	]=====
	print '-----> Loading data'
	data = load_data(num_dfs=1, data_dir='/data/aers/formatted/', verbose=False)

	#=====[ Step 2: get the legal drugs	]=====
	print '-----> Getting legal drugs'
	legal_drugs = get_legal_drugs(data, num_occurrences=10)

	#=====[ Step 3: reduce dataset to only legal drugs	]=====
	print '-----> Reducing data.DRUGS to only legal drugs'
	data.DRUG = data.DRUG.apply(lambda l: [x for x in l if x in legal_drugs])

	#=====[ Step 3: get positives	]=====
	print '-----> Getting X, y positive'
	DRUGs_pos, REACs_pos = get_X_y_positive(data)

	#=====[ Step 4: get coocurrences	]=====
	print '-----> Getting coocurrences'
	co_occurrences = get_co_occurrences(data)

	#=====[ Step 5: get negative reactions	]=====
	print '-----> Getting X, y negative'
	DRUGs_neg, REACs_neg = get_X_y_negative(data, co_occurrences)


	print '-----> Saving to pickle'
	DRUGs = DRUGs_pos + DRUGs_neg 
	REACs = REACs_pos + REACs_neg
	pickle.dump(DRUGs, open('DRUGs.pkl', 'w'))
	pickle.dump(REACs, open('REACs.pkl', 'w'))	




