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

import click
@click.command()
@click.option('-i', '--input_dir', help='Input directory containing ascii files', default=os.environ['DATA_DIR'])
@click.option('-o', '--output', help='Input directory containing ascii files', default='data.df')
def preprocess(input_dir, output):

	#=====[ Step 1: get individual dataframes ]=====
	df_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if not f.startswith('.')]
	dfs = [pd.read_csv(p) for p in df_paths]




if __name__ == '__main__':
	example_script()
