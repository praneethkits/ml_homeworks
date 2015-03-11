import glob
import sys, os
import argparse
from general_functions import read_file_contents, stop_words_list
 
unnecessary_words = [ "", " ", "'", "\"", "~", ",", "%", "$", "#", "@", "~", "*", "class", "null", "."]

class ConvertArrf(object):
    """ converts the class folders text into ARRF format and writes 
        to a file.
    """
    def __init__(self, folder_name, output_file):
        """ Initializes the variable required by the class."""
        self.folder_name = folder_name
        self.output_file = output_file
        self.classes = {}
        self.word_counts = {}
        self.vocab = []
        self.wordc = 0
        self.set_classes()
        self.set_word_counts()
        
    def set_classes(self):
        """ sets the classes."""
        classes_paths = glob.glob(self.folder_name + "/*")
        for path in classes_paths:
            class_name = os.path.basename(path)
            self.classes[class_name] = path

    def set_word_counts(self):
        """ sets the word counts for each class."""
        for k, v in self.classes.iteritems():
            docs = glob.glob(v + "/*")
            self.word_counts[k] = self.get_word_count(docs)

    def stripped(self, x):
        return "".join([i for i in x if 31 < ord(i) < 127])
    
    def get_word_count(self, docs):
        """ Gets the word count from the list of docs."""
        textc = {}
        for doc in docs:
            textc[doc] = {}
            status, contents = read_file_contents(doc)
            vocab = contents.replace("\n", " ").replace("\r", "").split(" ")
            for word in vocab:
                word = self.stripped(word)
                if word in unnecessary_words or word.isdigit() or len(word) <= 2:
                    continue

                if word in textc[doc]:
                    textc[doc][word] += 1
                else:
                    textc[doc][word] = 1
            self.set_vocab(textc[doc].keys())
        return textc
            
    def set_vocab(self, vocab):
        """ Adds the given list of vocab to global vocab."""
        self.vocab.extend(vocab)

    def get_header(self):
        """ Returns the header format for arrf file."""
        header = "@RELATION " + os.path.basename(self.folder_name) + "_relations\n"
        vocab_hash = {}
        i = 0
        for word in set(self.vocab):
            i += 1
            header = header + "@ATTRIBUTE " + word + " NUMERIC\n"
            vocab_hash[i] = word
      
        self.wordc = i
        self.vocab = vocab_hash
        header = header + "@ATTRIBUTE Class        {"
        for class_name in self.classes.keys():
            header = header + class_name + ","

        header = header[:-1]
        header = header + "}\n\n"
            
        return header

    def get_data(self):
        """ Returns the data for the arrfile"""
        content = "@DATA \n"
        for k, docs in self.word_counts.iteritems():
            for doc, v in docs.iteritems():
                i = 1
                while i <= self.wordc:
                    word = self.vocab[i]
                    if word in v:
                        content = content + str(float(v[word])) + ","
                    else:
                        content = content + "0.0,"
                    i += 1
                content = content + str(k) + "\n"

        return content

    def generate_arrf_file(self):
        """ generates the arrf file."""
        header = self.get_header()
        data = self.get_data()

        fd = open(self.output_file, "w")
        fd.write(header)
        fd.write(data)
        fd.close()



def main():
    """ control and execute block."""
    parser = argparse.ArgumentParser(prog='convert_to_arff.py')
    parser.add_argument('-fn', nargs=1, required=True,
                        help="data path")
    parser.add_argument('-of',  nargs=1, required=True,
                        help="output file.")
    args = parser.parse_args()
    
    cf = ConvertArrf(args.fn[0], args.of[0])   
    cf.generate_arrf_file()


if __name__ == "__main__":
    """Start of program."""
    main()    