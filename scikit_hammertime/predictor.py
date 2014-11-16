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
import w2v
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

    def load_training_examples(self):
        self.training_tuples = pkl.load(open('/data/aers/training/DRUGs.data'))
        self.training_reacs = pkl.load(open('/data/aers/training/REACs.data'))


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
            X.append(feature_engineer(drug2vec[training_tuple[0]],drug2vec[training_tuple[1]]))
            y.append(len(self.training_reacs[i]) > 0)
        X = np.array(X)
        y = np.array(y)
        return X,y

    def feature_engineer(self, vec1, vec2):
        """
            returns a numpy feature array for the two drugs vec1 and vec2
        """
        outer_product = np.dot(vec1,vec2.T)
        diff = vec1 - vec2








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
