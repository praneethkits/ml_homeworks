import logging
import argparse
import glob
import os, sys


def read_file_contents(file_name=None):
    """This function is used to read the file contents and return contents
    in a string format.
    Args:
        file_name: file which need to be read.
    Returns:
        SUCCESS when successfully read else FAILURE
        file_content: Complete content of file.
    Raises:
        NA.
    """
    if file_name is None:
        return FAILURE, 'NA'

    try:
        file_descriptor = open(file_name, "rb")
    except IOError:
        logging.error("Unable to open given protobuf file")
        return FAILURE, 'NA'

    file_content = file_descriptor.read()
    file_descriptor.close()
    return SUCCESS, file_content


class NaiveBayes(object):
    """ This class is used to implement the naive bayes algorithm for
    text classification."""

    def __init__(self, test_set_path, training_set_path):
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
        self.training_classes = {}
        self.training_Documents = {}

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
        for k, v in self.training_classes:
            docs = glob.glob(v + "/*")
            if k in self.training_Documents:
                self.training_Documents[k].extend(docs)
            else:
                self.training_Documents[k] = docs


def main():
    """The control and execute block of the program."""
    parser = argparse.ArgumentParser(prog='bayes.py')
    parser.add_argument('-tr', nargs=1, required=True,
                        help="training set path.")
    parser.add_argument('-te',  nargs=1, required=True,
                        help="test set path.")
    args = parser.parse_args()



if __name__ == "__main__":
    """Start of program."""
    main()
