import logging
import argparse
import glob
import os, sys
import math
import numpy
import random
from general_functions import read_file_contents, stop_words_list


class perceptron(object):
    """ This class implements the perceptron training algorithm."""

    def __init__(self, training_set_path, test_set_path, initial_weight=0.5,
                 eeta=0.1, RSW=False):
        """ Defines the variables required by the class."""
        self.test_set_path = test_set_path
        self.training_set_path = training_set_path
        self.initial_weight = initial_weight
        self.eeta = eeta
        self.RSW = RSW
        self.training_classes = {}
        self.test_classes = {}
        self.test_Documents = {}
        self.training_Documents = {}
        self.training_Vocabulary = {}
        self.Vocab = None
        self.weights = {}
        self.set_training_classes()
        self.set_training_documents()
        self.set_training_vocabulary()
        self.set_test_classes()
        self.set_test_documents()
        self.set_weights()

    def set_Vocab(self, vocab):
        self.Vocab = vocab

    def set_weights(self):
        for word in self.Vocab:
            self.weights[word] = self.initial_weight

    def set_training_classes(self):
        """This function is used to set the training classes.
        Args:
            self: Instance of the class.
        Returns:
            NA.
        Raises:
            NA.
        """
        classes_paths = glob.glob(self.training_set_path + "/*")
        for path in classes_paths:
            class_name = os.path.basename(path)
            self.training_classes[class_name] = path

    def set_test_classes(self):
        """This function is used to set the testing classes.
        Args:
            self: Instance of the class.
        Returns:
            NA.
        Raises:
            NA.
        """
        classes_paths = glob.glob(self.test_set_path + "/*")
        for path in classes_paths:
            class_name = os.path.basename(path)
            self.test_classes[class_name] = path

    def set_training_documents(self):
        """ This function is used to set the training documnets
            for each class.
        Args:
            self: Instance of the class.
        Returns:
            NA.
        Raises:
            NA.
        """
        for k, v in self.training_classes.iteritems():
            docs = glob.glob(v + "/*")
            if k in self.training_Documents:
                self.training_Documents[k].extend(docs)
            else:
                self.training_Documents[k] = docs

    def set_test_documents(self):
        """ This function is used to set the training documnets
            for each class.
        Args:
            self: Instance of the class.
        Returns:
            NA.
        Raises:
            NA.
        """
        for k, v in self.test_classes.iteritems():
            docs = glob.glob(v + "/*")
            if k in self.test_Documents:
                self.test_Documents[k].extend(docs)
            else:
                self.test_Documents[k] = docs

    def set_training_vocabulary(self):
        """ This function sets the vocabulary."""
        stop_words=stop_words_list()
        for k, v in self.training_Documents.iteritems():
            for doc in v:
                status, contents = read_file_contents(doc)
                vocab = contents.replace("\n", " ").replace("\r", "").split(" ")
                if self.RSW:
                    for word in vocab:
                        if word in stop_words:
                            vocab.remove(word)

                if doc in self.training_Vocabulary:
                    self.training_Vocabulary[doc].extend(vocab)
                else:
                    self.training_Vocabulary[doc] = vocab
        self.get_uniq_vocab_from_training_vocab()

    def get_uniq_vocab_from_training_vocab(self):
        """ returns the unique vocab from training vocabulary."""
        vocab = []
        for k, v in self.training_Vocabulary.iteritems():
            vocab.extend(v)

        v = []
        for w in set(vocab):
            v.append(w)

        self.set_Vocab(v)

    def get_text_count_for_doc(self, doc):
        """ Returns the individual text count for a given doc.
        Args:
            doc: doc for which individual text count is required.
        """
        textc = {}
        if doc not in self.training_Vocabulary:
            return textc

        for text in self.training_Vocabulary[doc]:
            if text in textc:
                textc[text] += 1
            else:
                textc[text] = 1

        return textc

    def step_function(self, value):
        if value <= -15:
            return -1
        else:
            return 1

    def class_to_val(self, class_name):
        if class_name == "spam":
            t = -1
        else:
            t = 1

        return t

    def train_perceptron(self):
        """ Implements the perceptron training algorithm.
        Assumes the bias value w0 as 0."""
        docs_hash = {}
        for k, v in self.training_Documents.iteritems():
            for doc in v:
                docs_hash[doc] = k
        
        for doc, k in docs_hash.iteritems():
                textc = self.get_text_count_for_doc(doc)
                val = 0
                for word, count in textc.iteritems():
                    val +=  self.weights[word] * count

                t = self.class_to_val(k)
                o = self.step_function(val)

                for word, count in textc.iteritems():
                    self.weights[word] += self.eeta * (t - o) * count

    def get_text_count_for_test_doc(self, doc):
        """ Returns the individual text count for a given doc.
        Args:
            doc: doc for which individual text count is required.
        """
        textc = {}
        status, contents = read_file_contents(doc)
        # print status, contents
        vocab = contents.replace("\n", " ").replace("\r", "").split(" ")
        
        for word in vocab:
            if self.RSW:
                if word in stop_words:
                    vocab.remove(word)
                    continue
            if word in textc:
                textc[word] += 1
            else:
                textc[word] = 1

        return textc

    def get_accuracy(self):
        """ Returns the accuracy on test data."""
        NC = 0
        NW = 0
        for k, v in self.test_Documents.iteritems():
            NCSub = 0
            NWSub = 0
            sum = 0
            min = 100000
            max = -100000
            for doc in v:
                textc = self.get_text_count_for_test_doc(doc)
                val = 0
                for word, count in textc.iteritems():
                    # print "current val is " + str(val)
                    if word in self.weights:
                        val +=  count * self.weights[word]
                t = self.class_to_val(k)
                o = self.step_function(val)
                # print val, k
                sum += val
                if val < min:
                    min = val
                elif val > max:
                    max = val
                if t == o:
                    NC += 1
                    NCSub += 1
                else:
                    NW += 1
                    NWSub += 1
            accSub = (NCSub * 100.0)/(NCSub + NWSub)
            print str(accSub) + " is accuracy of class " + k
            # print str(min) + " is min for class " + k
            # print str(max) + " is max for class " + k
            # print str(sum/(NCSub + NWSub)) + " is avg for class " + k
        # print NC, NW
        accuracy = (NC * 100.0)/(NC + NW)
        return accuracy

def main():
    """The control and execute block of the program."""
    parser = argparse.ArgumentParser(prog='perceptron.py')
    parser.add_argument('-tr', nargs=1, required=True,
                        help="training set path.")
    parser.add_argument('-te',  nargs=1, required=True,
                        help="test set path.")
    parser.add_argument('-r', action='store_true',
                        help="removes the stop words from vocabulary.")
    parser.add_argument('-iw', nargs=1, required=True,
                        help="Initial weights.")
    parser.add_argument('-e', nargs=1, required=True,
                        help="eeta.")
    args = parser.parse_args()

    stop_words=stop_words_list()
    pT = perceptron(args.tr[0], args.te[0], float(args.iw[0]), 
                    float(args.e[0]), args.r)
    i=0
    while i< 25:
        pT.train_perceptron()
        i+=1
        print "Accuracy is " +  str(pT.get_accuracy()) + " after " + str(i) + " iteration"
    

if __name__ == "__main__":
    """Start of program."""
    main()
