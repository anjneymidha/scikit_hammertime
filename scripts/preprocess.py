"""
Script: preprocess.py
=====================

Description:
------------

	Goes from raw ascii data, chunked in files,
	to a single pandas dataframe that is properly
	formatted.

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



def parse_quarter_dirname(quarter_dir):
	"""
		given AERS directory name, returns 
			year, quarter
	"""
	quarter_dir = os.path.split(quarter_dir)[-1]
	year = int(quarter_dir[:4])
	quarter = int(quarter_dir[5])
	return year, quarter


def parse_filename(filepath):
	"""
		given a .txt filename, returns 
			file_descriptor, year, quarter
	"""
	filename = os.path.split(filepath)[-1]
	file_descriptor = filename[:4].upper()
	year = int(filename[4:6])
	quarter = int(filename[7])
	return file_descriptor, year, quarter



################################################################################
####################[ FORMAT INDIVIDUAL FILES	]###############################
################################################################################

def lowercase_column_names (df):
	df.columns = [x.lower() for x in df.columns]


def retain_columns(df, col_list):
	drop_columns = set(df.columns).difference(set(col_list))
	df = df.drop(drop_columns, axis=1, inplace=True)


def format_DRUG(df):
	retain_columns(df, ['primaryid', 'drugname'])
	df.drugname = df.drugname.str.lower().str.strip().astype('category')
	df = df.groupby('primaryid').drugname.agg(lambda x: list(x))
	df = df.apply(lambda x: list(set([y.split()[0] for y in x if type(y) == str])))
	return df


def format_REAC(df):
	retain_columns(df, ['primaryid', 'pt'])
	df.pt = df.pt.str.lower().str.strip().astype('category')
	df = df.groupby('primaryid').pt.agg(lambda x: list(x))
	return df



def format_INDI(df):
	retain_columns(df, ['primaryid', 'indi_pt'])
	df.indi_pt = df.indi_pt.str.lower().str.strip().astype('category')
	df = df.groupby('primaryid').indi_pt.agg(lambda x: list(x))
	return df


def format_quarter(quarter_dir):
	"""
		given a path to a directory containing data files, 
		(i.e. data/faers_ascii_2014q1)
		returns a dataframe containing all the information
	"""
	#=====[ Step 1: Get ascii_dir, name	]=====
	year, quarter = parse_quarter_dirname(quarter_dir)
	print '=====[ %d, %d ]=====' % (year, quarter)
	ascii_dir = os.path.join(quarter_dir, 'ascii')
	if not os.path.exists(ascii_dir):
		ascii_dir = os.path.join(quarter_dir, 'ASCII')
	assert os.path.exists(ascii_dir)


	#=====[ Step 2: load/format each independently	]=====
	dfs = {}
	format_funcs = {
						'DRUG':format_DRUG,
						'REAC':format_REAC,
						'INDI':format_INDI
					}
	for filename in [os.path.join(ascii_dir, p) for p in os.listdir(ascii_dir) if p.endswith('.txt')]:

		file_descriptor, year, quarter = parse_filename(filename)
		if file_descriptor in format_funcs.keys() and filename.endswith('.txt'):
			
			print '	---> Loading: %s' % file_descriptor
			df = pd.read_csv(filename, delimiter='$')

			print '	---> Formatting: %s' % file_descriptor
			df = format_funcs[file_descriptor](df)

			dfs[file_descriptor] = df

	#=====[ Step 3: join on primaryid	]=====
	joined = pd.concat(dfs.values(), keys=dfs.keys(), axis=1)
	return joined


def join_dfs(input_dir='/data/aers/entries', output_dir='/data/aers/formatted'):
	data_dir = input_dir

	process_years = [2013, 2014]
	process_quarters = [1, 2, 3, 4]

	#=====[ Step 1: For each quarter... ]=====
	dfs = []
	quarter_dirs = [os.path.join(data_dir, p) for p in os.listdir(data_dir)]
	for quarter_dir in quarter_dirs:

		year, quarter = parse_quarter_dirname(quarter_dir)
		if year in process_years and quarter in process_quarters:

			dump_path_pickle = os.path.join(output_dir, str(year) + 'q' + str(quarter) + '.df')
			dump_path_csv = os.path.join(output_dir, str(year) + 'q' + str(quarter) + '.csv')
			df = format_quarter(quarter_dir)

			pickle.dump(df, open(dump_path_pickle, 'w'))
			df.to_csv(open(dump_path_csv, 'w'))
			print '-----> Dumping to: %s' % dump_path_pickle
			
			dfs.append(df)

	return dfs









if __name__ == '__main__':
	dfs = join_dfs()

