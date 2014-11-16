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
import sklearn
import pandas as pd
import pickle as pkl

class Predictor(object):
    """
        Class: Predictor 
        ================

        Class wrapping ML predictor for drug interactions
    """
    data_filename = 'data.df'
    clf_filename = 'clf.pkl'


    def __init__(self, data_dir='/data/aers/'):
        """
            data_dir: location of parameters 
        """
        self.load_data()


    ################################################################################
    ####################[ INTERNALS  ]##############################################
    ################################################################################

    def load_data(self, name='traindata.df'):
        """
            loads data to train 
        """
        print '-----> Loading data'
        data_path = os.path.join(self.data_dir, name)
        if os.path.exists(data_path):
            self.data = pkl.load(open(data_path, 'r'))
            if not type(data) == tuple and len(data) == 2:
                raise Exception("Incorrectly formatted data")
        else:
            self.data = None



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

