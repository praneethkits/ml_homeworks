import logging
import argparse
import glob
import os, sys
import math
from general_functions import read_file_contents, stop_words_list


class NaiveBayes(object):
    """ This class is used to implement the naive bayes algorithm for
    text classification."""

    def __init__(self, training_set_path, test_set_path, RSW=False):
        """ This function is used to define the variables required by class.
        Args:
            test_set_path: path where test documents are stored.
            training_set_path: path where training documents are stored.
        Returns:
            NA.
        Raises:
            NA.
        """
        self.test_set_path = test_set_path
        self.training_set_path = training_set_path
        self.RSW = RSW
        self.training_classes = {}
        self.test_classes = {}
        self.test_Documents = {}
        self.training_Documents = {}
        self.training_Vocabulary = {}
        self.Vocab = None
        self.condProb = {}
        self.prior = {}
        self.set_training_classes()
        self.set_training_documents()
        self.set_training_vocabulary()
        self.set_test_classes()
        self.set_test_documents()

    def set_Vocab(self, vocab):
        self.Vocab = vocab

    def train_multinomial_nb(self):
        """ This function is used to train the naive bayes algorithm for
        text classification.
        Args:
            self: Instance of the class.
        Returns:
            None.
        Raise:
            NA.
        """
        self.get_uniq_vocab_from_training_vocab()
        docs_count = self.get_training_docs_count()
        N = 0
        for k in docs_count:
            N += docs_count[k]

        for clas in self.training_classes:
            self.prior[clas] = (docs_count[clas] * 1.0)/N
            Tct = self.get_text_count_for_class(clas)

            sum_tct = 0
            for k, v in Tct.iteritems():
                sum_tct += v
            denominator = sum_tct + len(self.Vocab)

            for t in self.Vocab:
                if t not in self.condProb:
                    self.condProb[t] = {}
                if t not in Tct:
                    Tct[t] = 0
                self.condProb[t][clas] = (Tct[t] + 1.0)/denominator

    def test_multinomial_nb(self, vocab):
        """ This function is used to test the naive bayes algorithm on test
            data set.
        Args:
            self: Instance of the class.
        Returns:
            Class for which document belongs.
        Raises:
            NA.
        """
        score = {}
        for k in self.training_classes:
            score[k] = math.log(self.prior[k])
            for t in vocab:
                if t in self.condProb:
                    score[k] += math.log(self.condProb[t][k])

        max_score = -10000000000
        clas = None
        for k, v in score.iteritems():
            if v > max_score:
                clas = k
                max_score = v

        return clas

    def get_accuracy_on_test_data(self):
        """ This function calculates the accuracy of the test dataset."""
        NC = 0
        NW = 0
        stop_words=stop_words_list()
        for k, v in self.test_Documents.iteritems():
            NCSub = 0
            NWSub = 0
            for doc in v:
                status, contents = read_file_contents(doc)
                vocab = contents.replace("\n", " ").replace("\r", "").split(" ")
                if self.RSW:
                    for word in vocab:
                        if word in stop_words:
                            vocab.remove(word)
                clas = self.test_multinomial_nb(vocab)
                if clas == k:
                    NC += 1
                    NCSub += 1
                else:
                    NW += 1
                    NWSub += 1

            sub_acc = (NCSub *100.0)/(NCSub + NWSub)
            print "accuracy of {0} is {1}".format(k, sub_acc) 

        accuracy = (NC * 100.0)/(NC + NW)
        return accuracy

    def get_text_count_for_class(self, clas):
        """ Returns the individual text count for a given class.
        Args:
            clas: class for which individual text count is required.
        """
        textc = {}
        if clas not in self.training_Vocabulary:
            return textc

        for text in self.training_Vocabulary[clas]:
            if text in textc:
                textc[text] += 1
            else:
                textc[text] = 1

        return textc
        
    def get_training_docs_count(self):
        """This function returns the training docs count."""
        count = {}
        for k, v in self.training_Documents.iteritems():
            count[k] = len(v)

        return count      

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
    parser = argparse.ArgumentParser(prog='bayes.py')
    parser.add_argument('-tr', nargs=1, required=True,
                        help="training set path.")
    parser.add_argument('-te',  nargs=1, required=True,
                        help="test set path.")
    parser.add_argument('-r', action='store_true',
                        help="removes the stop words from vocabulary.")
    args = parser.parse_args()

    nb = NaiveBayes(args.tr[0], args.te[0], args.r)
    nb.train_multinomial_nb()
    accuracy = nb.get_accuracy_on_test_data()
    print str(accuracy) + " Is accuracy with naive bayes algorithm."


if __name__ == "__main__":
    """Start of program."""
    main()
