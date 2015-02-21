import os, sys, glob
import logging
import argparse
import math, numpy
from general_functions import read_file_contents, stop_words_list


class LogisticRegression(object):
    """ This class implements the naive bayes algorithm for
    text classification."""
    def __init__(self, training_set_path, test_set_path, initial_weight=0.5,
                 lamda=0.1, eeta=0.1, acceptable_delta=1, max_iterations=100,
                 RSW=False):
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
        self.test_vocab_doc = {}
        self.training_Documents = {}
        self.training_vocab_doc = {}
        self.training_Vocabulary = {}
        self.weights = {}
        self.Vocab = None
        self.initial_weight = initial_weight
        self.w0 = initial_weight
        self.lamda = lamda
        self.eeta = eeta
        self.set_training_classes()
        self.set_training_documents()
        self.set_training_vocabulary()
        self.set_weights()
        self.set_test_classes()
        self.set_test_documents()
        self.set_test_vocab_doc()
        self.acceptable_delta = acceptable_delta
        self.max_iterations = max_iterations

    def get_probability_doc(self, doc):
        """ Returns the probablity of doc belonging to ham."""
        sum1 = self.w0
        for text, value in self.training_vocab_doc[doc].iteritems():
            sum1 += self.weights[text]*value

        exp = numpy.exp(sum1 * -1)
        prob = 1/(1.0 + exp)
        # print prob, sum1, exp
        return prob

    def get_max_diff_weights(self, new_weights):
        """ Returns the max difference between old and new weights."""
        diff = 0
        for text in self.weights:
            curr_diff = abs(self.weights[text] - new_weights[text])
            if curr_diff > diff:
                diff = curr_diff
        return diff

    def get_text_sigma_value(self, text, doc_ham_prob):
        """ Returns the text new weight sums."""
        sum = 0
        for clas, v in self.training_Documents.iteritems():
            if clas.lower() == "ham":
                Y = 1
            else:
                Y = 0
            for doc in v:
                if text not in self.training_vocab_doc[doc]:
                    self.training_vocab_doc[doc][text] = 0
                sum += self.training_vocab_doc[doc][text] * (Y - doc_ham_prob[doc])

        return sum

    def train_logistic_regression(self):
        """ Trains the model using the traing data. """
        diff = self.acceptable_delta + 1
        i = 0
        while diff > self.acceptable_delta and i <= self.max_iterations:
            new_weights = {}
            w0 = self.w0 - self.eeta*self.lamda*self.w0
            doc_ham_prob = {}
            for clas, v in self.training_Documents.iteritems():
                for doc in v:
                    doc_ham_prob[doc] = self.get_probability_doc(doc)

            for text in self.Vocab:
                sum = self.get_text_sigma_value(text, doc_ham_prob)
                new_weights[text] = self.weights[text] + self.eeta*sum - \
                    self.eeta*self.lamda*self.weights[text]

            diff = self.get_max_diff_weights(new_weights)
            self.weights.clear()
            self.weights = new_weights
            i = i + 1
            if (abs(w0 - self.w0) > diff):
                diff = abs(w0 - self.w0)
            self.w0 = w0

            logging.info(i, diff)

        print "Training stopped after " + str(i) + " iterations."

    def get_test_probability_doc(self, doc):
        """ Returns the probablity of doc belonging to ham."""
        sum1 = self.w0
        for text, value in self.test_vocab_doc[doc].iteritems():
            if text not in self.weights:
                self.weights[text] = 0
            sum1 += self.weights[text]*value

        exp = numpy.exp(sum1 * -1)
        prob = 1/(1.0 + exp)
        # print prob, sum1, exp
        return prob


    def get_accuracy(self):
        """ Vaidates the weights on test dataset."""
        Nc = 0
        Nw = 0
        for clas, v in self.test_Documents.iteritems():
            clasNc = 0
            clasNw = 0
            for doc in v:
                ham_prob = self.get_test_probability_doc(doc)
                if ham_prob >= 0.5:
                    prediction = 'ham'
                else:
                    prediction = 'spam'

                if prediction == clas.lower():
                    Nc += 1
                    clasNc += 1
                else:
                    Nw += 1
                    clasNw += 1
            acc = (clasNc * 100.0)/(clasNc + clasNw)
            logging.info(str(acc) + " is accuracy for class " + clas)

        accuracy = (Nc * 100.0)/(Nc + Nw)

        return accuracy

    def set_Vocab(self, vocab):
        self.Vocab = vocab

    def set_weights(self):
        for text in self.Vocab:
            self.weights[text] = self.initial_weight

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

    def set_test_vocab_doc(self):
        """ Sets the vocabulary count for each document."""
        stop_words = stop_words_list()
        for k, v in self.test_Documents.iteritems():
            for doc in v:
                self.test_vocab_doc[doc] = {}
                status, contents = read_file_contents(doc)
                vocab = contents.replace("\n", " ").split(" ")
                if self.RSW:
                    for word in vocab:
                        if word in stop_words:
                            vocab.remove(word)

                for text in vocab:
                    if text in self.test_vocab_doc[doc]:
                        self.test_vocab_doc[doc][text] += 1
                    else:
                        self.test_vocab_doc[doc][text] = 1

    def set_training_vocabulary(self):
        """ This function sets the vocabulary."""
        stop_words = stop_words_list()
        for k, v in self.training_Documents.iteritems():
            for doc in v:
                status, contents = read_file_contents(doc)
                vocab = contents.replace("\n", " ").split(" ")
                if self.RSW:
                    for word in vocab:
                        if word in stop_words:
                            vocab.remove(word)
                if k in self.training_Vocabulary:
                    self.training_Vocabulary[k].extend(vocab)
                else:
                    self.training_Vocabulary[k] = vocab

                self.training_vocab_doc[doc] = {}
                for text in vocab:
                    if text in self.training_vocab_doc[doc]:
                        self.training_vocab_doc[doc][text] += 1
                    else:
                        self.training_vocab_doc[doc][text] = 1
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



def main():
    """The control and execute block of the program."""
    parser = argparse.ArgumentParser(prog='logistic_regression.py')
    parser.add_argument('-tr', nargs=1, required=True,
                        help="training set path.")
    parser.add_argument('-te',  nargs=1, required=True,
                        help="test set path.")
    parser.add_argument('-iw', nargs=1, required=True,
                        help="Initial weights.")
    parser.add_argument('-l', nargs=1, required=True,
                        help="lambda.")
    parser.add_argument('-e', nargs=1, required=True,
                        help="eeta.")
    parser.add_argument('-ad', nargs=1, required=True,
                        help="acceptible delta between weights for convergence.")
    parser.add_argument('-mi', nargs=1, required=True,
                        help="maximum number of iterations.")
    parser.add_argument('-r', action='store_true',
                        help="Remove the stop words.")
    args = parser.parse_args()
    lg = LogisticRegression(args.tr[0], args.te[0], float(args.iw[0]),
                            float(args.l[0]), float(args.e[0]),
                            float(args.ad[0]), int(args.mi[0]), args.r)
    lg.train_logistic_regression()

    print str(lg.get_accuracy()) + " is the accuracy."


if __name__ == "__main__":
    """Start of program."""
    main()

