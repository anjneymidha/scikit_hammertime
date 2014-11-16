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


    def __init__(self, data_dir='/data/aers/production/'):
        """
            data_dir: location of parameters 
        """
        self.data_dir = data_dir

        print '=====[ CONSTRUCTING PREDICTOR ]====='
        self.load_training_examples()
        self.drug_names = load_drug_names()
        self.clf = self.load_clf()
        print '=====[ CONSTRUCTION COMPLETE ]====='



    ################################################################################
    ####################[ LOADING/SAVING ]##########################################
    ################################################################################

    def load_training_examples(self):
        print '-----> Loading training examples'
        self.training_tuples = pkl.load(open('/data/aers/training/DRUGs.pkl'))
        self.training_reacs = pkl.load(open('/data/aers/training/REACs.pkl'))


    # def load_clf(self, name='classifier.pkl'):
    #     """
    #         loads the classifier 
    #     """
    #     print '-----> Loading clf'
    #     clf_path = os.path.join(self.data_dir, name)
    #     if os.path.exists(clf_path):
    #         clf = pkl.load(open(clf_path))
    #     else:
    #         clf = None
    #     return clf


    # def save_clf(self, name='classifier.pkl'):
    #     """
    #         saves the classifier to disk 
    #     """
    #     print '-----> Saving clf'
    #     clf_path = os.path.join(self.data_dir, name)
    #     pkl.dump(self.clf, open(clf_path, 'w'))



    def load_data(self, name='classifier.pkl'):
        """
            loads:
                X, y, drug2vec, clf (if exists)
        """
        print '=====[ LOADING DATA ]====='
        print '-----> Loading: drug2vec'
        self.drug2vec = pickle.load(open(os.path.join(self.data_dir, 'drug2vec.pkl'), 'r'))

        print '-----> Loading: X, y'
        self.X = pickle.load(open(os.path.join(self.data_dir, 'X.pkl'), 'r'))
        self.y = pickle.load(open(os.path.join(self.data_dir, 'y.pkl'), 'r'))

        print '=====[ LOADING DATA: COMPLETE ]====='



    def save_data(self):
        """
            saves:
                X, y, drug2vec, clf
        """
        print '=====[ SAVING DATA ]====='

        print '-----> Saving drug2vec'
        pickle.dump(self.drug2vec, open(os.path.join(self.data_dir, 'drug2vec.pkl'), 'w'))

        print '-----> Saving X, y'
        pickle.dump(self.X, open(os.path.join(self.data_dir, 'X.pkl'), 'w'))
        pickle.dump(self.y, open(os.path.join(self.data_dir, 'y.pkl'), 'w'))

        print '=====[ SAVING DATA: COMPLETE ]====='


    ################################################################################
    ####################[ TRAINING  ]###############################################
    ################################################################################

    def featurize(self, drug1, drug2):
        """
            returns a numpy feature array for the two drugs vec1 and vec2
        """
        #=====[ Step 1: get drug vectors ]=====
        vec1, vec2 = self.drug2vec[drug1], self.drug2vec[drug2]

        #=====[ Step 2: combos of them ]=====
        # outer_product = np.dot(vec1,vec2.T)
        diff = vec1 - vec2
        add = vec1 + vec2
        return np.hstack([diff,add])


    def get_X_y(self):
        """
            returns X, y
        """
        X, y = [], []
        for drug_tup, reac_tup in zip(self.training_tuples, self.training_reacs):
            try:
                X.append(self.featurize(drug_tup[0], drug_tup[1]))
                y.append(len(reac_tup) > 0)
            except:
                continue
        return np.array(X), np.array(y)

    
    def shuffle_in_unison(self, a, b):
        """
            shuffles a and b to randomize 
        """
        assert len(a) == len(b)
        shuffled_a = np.empty(a.shape, dtype=a.dtype)
        shuffled_b = np.empty(b.shape, dtype=b.dtype)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
            shuffled_a[new_index] = a[old_index]
            shuffled_b[new_index] = b[old_index]
        return shuffled_a, shuffled_b


    def gather_production_data(self, ndim=50, min_count=10):
        """
            gets X, y, drug2vec; saves them in /data/aers/production
        """
        print '=====[ GATHER PRODUCTION DATA: BEGIN ]====='

        #=====[ Step 0: load training examples ]=====
        self.load_training_examples()

        #=====[ Step 1: train word2vec ]=====
        print '-----> Training drug2vec'
        self.drug2vec = gensim.models.word2vec.Word2Vec(df.DRUG, size=ndim, min_count=min_count, sg=0).train()

        #=====[ Step 3: make X and y ]=====
        print '-----> Making X, y'
        self.X, self.y = self.get_X_y()

        #=====[ Step 4: shuffle X, y ]=====
        print '-----> Shuffling X, y'
        self.X, self.y = self.shuffle_in_unison(self.X, self.y)

        print '=====[ GATHER PRODUCTION DATA: COMPLETE ]====='


    def cross_validate(self):
        """
            trains classifier and cross_validates it 
        """
        #=====[ Step 1: Ensure data is there ]=====
        if self.X is None or self.y is None:
            self.gather_production_data()

        #=====[ Step ]=====
        raise NotImplementedError







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

