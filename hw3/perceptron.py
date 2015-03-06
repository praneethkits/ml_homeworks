import logging
import argparse
import glob
import os, sys
import math
from general_functions import read_file_contents, stop_words_list


class perceptron(object):
    """ This class implements the perceptron training algorithm."""

    def __init__(self, training_set_path, test_set_path, RSW=False):
        """ Defines the variables required by the class."""
        self.test_set_path = test_set_path
        self.training_set_path = training_set_path
        self.RSW = RSW
        self.training_classes = {}
        self.test_classes = {}
        self.test_Documents = {}
        self.training_Documents = {}
        self.training_Vocabulary = {}
        self.Vocab = None
        self.set_training_classes()
        self.set_training_documents()
        self.set_training_vocabulary()
        self.set_test_classes()
        self.set_test_documents()

    def set_Vocab(self, vocab):
        self.Vocab = vocab

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

                if k in self.training_Vocabulary:
                    self.training_Vocabulary[k].extend(vocab)
                else:
                    self.training_Vocabulary[k] = vocab

    def get_uniq_vocab_from_training_vocab(self):
        """ returns the unique vocab from training vocabulary."""
        vocab = []
        for k, v in self.training_Vocabulary.iteritems():
            vocab.extend(v)

        v = []
        for w in set(vocab):
            v.append(w)

        self.set_Vocab(v)


def main():
    """The control and execute block of the program."""
    parser = argparse.ArgumentParser(prog='perceptron.py')
     parser.add_argument('-tr', nargs=1, required=True,
                        help="training set path.")
    parser.add_argument('-te',  nargs=1, required=True,
                        help="test set path.")
    parser.add_argument('-r', action='store_true',
                        help="removes the stop words from vocabulary.")
    args = parser.parse_args()

    pT = perceptron(args.tr[0], args.te[0], args.r)
     
