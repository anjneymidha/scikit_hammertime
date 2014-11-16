import sklearn
import pandas as pd
import pickle as pkl

class predictor(object):
    def __init__(self, df_path):
        self.df = pkl.load(open(df_path,'r'))

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

