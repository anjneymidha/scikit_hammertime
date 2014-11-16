"""
Script: Predictor.py
====================

Description:
------------

    Class wrapping ML predictor for drug interactions

##################
Jay Hack
jhack@stanford.edu
Fall 2014
##################
"""
import os
import sklearn
import pandas as pd
import pickle as pkl

class Predictor(object):
    """
        Class: Predictor 
        ================

        Class wrapping ML predictor for drug interactions
    """
    clf_filename = 'clf.pkl'


    def __init__(self, data_dir='/data/aers/formatted/'):
        """
            data_dir: location of parameters 
        """
        self.data_dir = data_dir
        self.load_data()




    ################################################################################
    ####################[ INTERNALS  ]##############################################
    ################################################################################

    def load_data(self, num_dfs=1):
        """
            loads data to train 
        """
        print '-----> Loading data (%d dataframes)' % num_dfs
        dfs = []
        df_paths = [os.path.join(self.data_dir, p) for p in os.listdir(self.data_dir) if p.endswith('.df')]
        for p in df_paths[:num_dfs]:
            df = pkl.load(open(p, 'r'))
            dfs.append(pkl.load(open(p, 'r')))
        self.data = pd.concat(dfs, axis=0)


    def load_clf(self, name='classifier.pkl'):
        """
            loads the classifier 
        """
        print '-----> Loading clf'
        clf_path = os.path.join(self.data_dir, name)
        if os.path.exists(clf_path):
            self.clf = pkl.load(open(clf_path))
        else:
            self.clf = None


    def save_clf(self, name='classifier.pkl'):
        """
            saves the classifier to disk 
        """
        print '-----> Saving clf'
        clf_path = os.path.join(self.data_dir, name)
        pkl.dump(self.clf, open(clf_path, 'w'))


    def train(self):
        """
            trains the classifier 
        """
        if self.data is None:
            self.load_data()
        # load the trained w2v model
        d2v = w2v.train()
        







    ################################################################################
    ####################[ INTERFACE ]###############################################
    ################################################################################

    def predict(self, data):
        """
            returns p(interaction|data) for each possible type 
            of interaction 
        """
        raise NotImplementedError


    def get_drugs(self):
        pass

    def get_conditions(self):
        pass

    def query(self, drugs, condition):
       pass 

    def to_numpy_array(self, drugs, condition):
       pass 

    def train(self):
        # make onehot:

        # turn into numpy format
    
        # create naive bayes
        NB = sklearn.naive_bayes.BernoulliNB()
        NB.fit(X,y)

