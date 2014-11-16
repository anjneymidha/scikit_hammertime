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
import numpy as np
import os
import w2v
import pandas as pd
from util import *
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
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
        self.data = load_data()
        self.drug_names = load_drug_names()




    ################################################################################
    ####################[ INTERNALS  ]##############################################
    ################################################################################

    def load_training_examples(self):
        self.training_tuples = pkl.load(open('/data/aers/training/DRUGs.pkl'))
        self.training_reacs = pkl.load(open('/data/aers/training/REACs.pkl'))


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
       # if self.data is None:
        #    self.load_data()
        # load the word2vec trained module
        drug2vec = w2v.train()
        # load the training
        self.load_training_examples()
        # make the training X,Y numpy matrix
        X = []
        y = []
        for i in range(len(self.training_tuples)):
            training_tuple = self.training_tuples[i]
            try:
                X.append(self.feature_engineer(drug2vec[training_tuple[0]],drug2vec[training_tuple[1]]))
                y.append(len(self.training_reacs[i]) > 0)
            except:
                continue
        X = np.array(X)
        y = np.array(y)
        return X,y

    def feature_engineer(self, vec1, vec2):
        """
            returns a numpy feature array for the two drugs vec1 and vec2
        """
        outer_product = np.dot(vec1,vec2.T)
        diff = vec1 - vec2
        add = vec1 + vec2
        return np.hstack([diff,add])

    def cross_validate(self):
        # get X,y dataset
        X,y = self.train()
        # randomly permute it
        X,y = self.shuffle_in_unison(X,y)
        # instantiate the logistic regression
        LR = LogisticRegression()
        # get CV scores
        scores = cross_validation.cross_val_score(LR,X,y)
        return scores


    def shuffle_in_unison(self, a, b):
        assert len(a) == len(b)
        shuffled_a = np.empty(a.shape, dtype=a.dtype)
        shuffled_b = np.empty(b.shape, dtype=b.dtype)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
            shuffled_a[new_index] = a[old_index]
            shuffled_b[new_index] = b[old_index]
        return shuffled_a, shuffled_b







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
        return self.drug_names


    def get_conditions(self):
        conditions = set()
        for l in self.data.INDI:
            if type(l) == list:
                for term in l:
                    conditions.add(term)

        return list(conditions)


    def get_reactions(self):
        reactions = set()
        for l in self.data.REAC:
            if type(l) == list:
                for term in l:
                    reactions.add(term)

        return list(reactions)

    def query(self, drugs, condition):
       pass 

    def to_numpy_array(self, drugs, condition):
       pass 

