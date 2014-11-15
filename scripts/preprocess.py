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
import pandas


def parse_filename(filepath):
	"""
		given a filename, returns 
			file_descriptor, year, quarter
	"""
	filename = os.path.split(filepath)[-1]
	file_descriptor = filename[:4].lower()
	year = int(filename[4:6])
	quarter = int(filename[7])
	return file_descriptor, year, quarter



def parse_ascii_directory(path):
	"""
		given a path to a directory containing data files, 
		(i.e. data/faers_ascii_2014q1)
		returns a dataframe containing all the information
	"""
	#=====[ Step 1: ascii dir	]=====
	path = os.path.join(path, 'ascii')
	assert os.path.exists(path)

	#=====[ Step 2: fill 'dfs' with dict mapping filetype to df	]=====
	dfs = {}	
	data_paths = [os.path.join(path, p) for p in os.listdir(path) if p.endswith('.txt')]
	with click.progressbar(data_paths) as _data_paths:
		for p in _data_paths:
			file_descriptor, year, quarter = parse_filename(p)
			dfs[file_descriptor] = pd.read_csv(open(p, 'r'), delimiter='$')

	return dfs










import click
@click.command()
@click.option('-i', '--input_dir', help='Input directory containing ascii files')
@click.option('-o', '--output', help='Input directory containing ascii files')
def preprocess(input_dir, output):

	#=====[ Step 1: get individual dataframes ]=====
	df = parse_ascii_directory(input_dir)




if __name__ == '__main__':
	df = preprocess()
