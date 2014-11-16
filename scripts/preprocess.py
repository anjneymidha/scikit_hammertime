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
		given a filename, returns 
			file_descriptor, year, quarter
	"""
	filename = os.path.split(filepath)[-1]
	file_descriptor = filename[:4].upper()
	year = int(filename[4:6])
	quarter = int(filename[7])
	return file_descriptor, year, quarter


def parse_drug_ind_ther(df):
	"""
		does groupby to put all drugs in same row 
	"""
	df.groupby()


def parse_quarter_dir(quarter_dir):
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

	#=====[ Step 2: load all files	]=====
	dfs = {}	
	assert os.path.exists(ascii_dir)
	data_paths = [os.path.join(ascii_dir, p) for p in os.listdir(ascii_dir) if p.lower().endswith('.txt')]
	for p in data_paths:
		file_descriptor, year, quarter = parse_filename(p)
		print '	---> %s' % file_descriptor
		try:
			dfs[file_descriptor] = pd.read_csv(open(p, 'r'), delimiter='$')
		except:
			print '		###[ PANDAS READ ERROR ]###'

	return dfs










import click
@click.command()
@click.option('-i', '--input_dir', help='Input directory containing ascii files', default='/data/aers/entries')
@click.option('-o', '--output', help='Input directory containing ascii files')
def preprocess(input_dir, output):

	data_dir = input_dir

	#=====[ Step 1: For each quarter... ]=====
	quarter_dirs = [os.path.join(data_dir, p) for p in os.listdir(data_dir)]
	for quarter_dir in quarter_dirs:
		dfs = parse_quarter_dir(quarter_dir)









if __name__ == '__main__':
	dfs = preprocess()
