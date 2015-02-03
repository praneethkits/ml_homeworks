#!/usr/bin/env python
import csv
import logging
import sys, os
from datetime import datetime
import math


def get_dict(file_name):
    """ This function is used read the csv file and load the datase into
        dictionary.
    Args:
	    file name: name of the file which needs to be read.
    Returns:
        True on success else False
        list with each row as a dictionary.
    Raises:
        NA.
    """
    logging.info("filename is: " + file_name)
    try:
        fd = open(file_name, "rb")
    except Exception as cause:  
        logging.error(cause)
        return False, [{}]
    ret_list = []
    reader = csv.DictReader(fd)
    keys = reader.fieldnames
    for i in reader:
        val_dict = {}
        for key in keys:
            val_dict[key] = i[key]
        ret_list.append(val_dict)
    fd.close()
    return True, ret_list


def get_entropy(val):
    """This function is used to calculate the entropy when distribution of
    positive and negative instances are given. This function assumes of binary
    values.
    Args: 
        val: array of count of distinct values
    Returns:
        entropy: entropy value for given distribution.
    Raises:
        NA.
    """
    total_dist = 0
    for i in val:
        total_dist += i
    total_dist = total_dist * 1.0

    entropy = 0
    for i in val:
        entropy += - (i/total_dist) * math.log(i/total_dist, 2)
    logging.info(str(entropy) + " is entropy for " + str(val))
    return entropy


def get_impurity_heuristic(val):
    """This function is used to calculate the impurity heauristic when
    distribution of positive and negative instances are given.
    Args:
        val: array of count of dictinct values.
    Returns:
        impurity_heuristic: Impurity heuristic of distinct values.
    Raises:
        NA.
    """
    total_dist = 0
    for i in val:
        total_dist += i

    total_dist = total_dist * 1.0
    impurity_heauristic = 1
    for i in val:
        impurity_heauristic = impurity_heauristic * (i/total_dist)

    logging.info(str(impurity_heauristic) + " is impurity heauristic for " + str(val))
    return impurity_heauristic


def get_gain(parent_entropy, parent_val_sum, val_list):
    """ This function is used to find the gain.
    Args:
        parent_entropy: entropy of the parent.
        val_list: list of distinct list of values.
    Returns:
        Gain
    Raises:
        NA.
    """
    gain = parent_entropy
    for val in val_list:
        sub_entropy = get_entropy(val_list[val].values())
        val_sum = sum(val_list[val].values())
        gain -= (val_sum * 1.0 * sub_entropy)/parent_val_sum

    logging.info("GAIN is " + str(gain))
    return gain


def get_impurity_heauristic_gain(parent_heauristic, parent_val_sum, val_list):
    """This function is used to find the gain.
     Args:
        parent_heauristic: impurity heauristic of the parent.
        parent_val_sum: sum of values of parent.
        val_list: list of values.
    Returns:
        Gain.
    Raises:
        NA.
    """
    gain = parent_heauristic
    for val in val_list:
        sub_heauristic = get_impurity_heuristic(val_list[val].values())
        val_sum = sum(val_list[val].values())
        gain -= (val_sum * 1.0 * sub_heauristic)/parent_val_sum

    logging.info("Heauristic Gain is " + str(gain))
    return gain


def get_parent_node(training_data_set, remaining_nodes=None,
                    class_node='Class', through_entropy=True):
    """ This function is used to get the parent node and its entropy.
    Args:
        training_data_set: dataset from which decision tree should be built.
    Returns:
        parent node and its entropy.
    Raises:
        NA.
    """
    entropy_keys = {}
    val_keys = {}

    if remaining_nodes is None:
        remaining_nodes = training_data_set[0].keys()
        remaining_nodes.remove(class_node)

    for node in remaining_nodes:
        val_keys[node] = {}
        entropy_keys[node] = {}

    total_records = 0
    for record in training_data_set:
        total_records += 1
        for node in remaining_nodes:
            if record[node] in val_keys[node]:
                if record[class_node] in val_keys[node][record[node]]:
                    val_keys[node][record[node]][record[class_node]] += 1
                else:
                    val_keys[node][record[node]][record[class_node]] = 1
            else:
                val_keys[node][record[node]] = {}
                val_keys[node][record[node]][record[class_node]] = 1

            if record[node] in entropy_keys[node]:
                entropy_keys[node][record[node]] += 1
            else:
                entropy_keys[node][record[node]] = 1

    nodes_entropy = {}
    nodes_gain = {}
    max_gain = -20000
    parent_node = ''
    for node in remaining_nodes:
        if through_entropy:
            nodes_entropy[node] = get_entropy(entropy_keys[node].values())
            nodes_gain[node] = get_gain(nodes_entropy[node], total_records,
                                        val_keys[node])
        else:
            nodes_entropy[node] = get_impurity_heuristic(entropy_keys[node].values())
            nodes_gain[node] = get_impurity_heauristic_gain(nodes_entropy[node],
                                                            total_records,
                                                            val_keys[node])
        if max_gain < nodes_gain[node]:
            max_gain = nodes_gain[node]
            parent_node = node
    logging.info(remaining_nodes + [" are remaining nodes"])
    logging.info(str(max_gain) + " is max gain")
    return parent_node


def validate_record(record, dec_tree, class_node='Class'):
    """ This function validates the record in dec_tree and
        outputs either true or false.
    Args:
        record: record which needs to be validated.
        dec_tree: decision tree from which we need to validate.
        class node: class variable.
    Returns: 
        True on successfule validation else False.
    Raises: 
        NA
    """
    node = dec_tree.keys()[0]
    logging.info(node + " is node")
    record_val = record[node]
    logging.info(str(record_val) + " is record_val")
    if record_val not in dec_tree[node]:
        return False

    if isinstance(dec_tree[node][record_val], dict):
        return validate_record(record, dec_tree[node][record_val], class_node)
    else:
        if dec_tree[node][record_val] == record[class_node]:
            return True
        else:
            return False


def validate(validation_data_set, dec_tree, class_node='Class'):
    """ This function is used to validate the decision tree with the validation
        data set.
    Args:
        validation_data_set: validation data set.
        class_node: name of the class node.
    Returns:
        accuracy: accuracy of the decision tree on validation data set.
    """
    total_records = 0
    correct_records = 0
    for record in validation_data_set:
        total_records += 1
        if validate_record(record, dec_tree, class_node):
            correct_records += 1

    accuracy = (correct_records * 100.0)/total_records
    logging.info(str(accuracy) + " is accuracy")
    return accuracy


def print_decision_tree(d, level=0, parent=None):
  for k, v in d.iteritems():
    if isinstance(v, dict):
      for k1, v1 in v.iteritems():
        if isinstance(v1, dict):
            print '|' * level + str(k) + " = " + str(k1) + " : "
            print_decision_tree(v1, level + 1)
        else:
            print '|' * level + str(k) + " = " + str(k1) + " : " + str(v1)


def decision_tree(training_data_set, remaining_nodes=None,
                  class_node='Class', through_entropy=True):
    """ This function creates the decision tree for the given training
    data set.
    Args:
        training_data_set: dataset from which decision tree should be built.
    Returns:
        Decision_tree: tree from which decisions can be made.
    Raises:
        NA
    """
    if len(training_data_set) == 0:
        return None

    class_val = {}
    for record in training_data_set:
        class_val[record[class_node]] = 1

    logging.info("Number of distinct outputs for training dataset is "
                 + str(len(class_val)))
    if len(class_val) == 1:
        return class_val.keys()[0]

    ret_decision_tree = {}

    if remaining_nodes is None:
        remaining_nodes = training_data_set[0].keys()
        remaining_nodes.remove(class_node)

    if len(remaining_nodes) == 1:
        parent_node = remaining_nodes[0]
        ret_decision_tree[parent_node] = {}
        val_out = {}
        for record in training_data_set:
            if record[parent_node] in val_out:
                if record[class_node] in val_out[record[parent_node]]:
                    val_out[record[parent_node]][record[class_node]] += 1
                else:
                    val_out[record[parent_node]][record[class_node]] = 1
            else:
                val_out[record[parent_node]] = {}
                val_out[record[parent_node]][record[class_node]] = 1
        for val in val_out:
            max_val = -1
            out_val = ''
            for k, v in val_out[val].iteritems():
                if v > max_val:
                    max_val = v
                    out_val = k
            ret_decision_tree[parent_node][val] = out_val

        return ret_decision_tree
            
    else:
        parent_node = get_parent_node(training_data_set, remaining_nodes,
                                      class_node, through_entropy)
    logging.info(str(parent_node) + " is parent node")

    sub_training_data_sets = {}
    for record in training_data_set:
        if record[parent_node] in sub_training_data_sets:
            sub_training_data_sets[record[parent_node]].append(record)
        else:
            sub_training_data_sets[record[parent_node]] = []
            sub_training_data_sets[record[parent_node]].append(record)

    ret_decision_tree[parent_node] = {}
    remaining_nodes.remove(parent_node)
    for key in sub_training_data_sets:
        rn = []
        rn.extend(remaining_nodes)
        sub_decision_tree = decision_tree(sub_training_data_sets[key],
                                          rn, class_node, through_entropy)
        ret_decision_tree[parent_node][key] = sub_decision_tree

    return ret_decision_tree


def copy_tree(actual, copy):
    """ Makes a copy of actual decision tree"""
    for k, v in actual.iteritems():
        if isinstance(v, dict):
            sub_copy = {}
            copy_tree(v, sub_copy)
            copy[k] = sub_copy
        else:
            copy[k] = v


def main():
    """ Starts the program."""
    if len(sys.argv) != 7:
        print "Usage: ./decision_tree.py <L> <K> <training_set> <validation_set> <test_set> <to_print>"
        return False

    L = sys.argv[1]
    K = sys.argv[2]
    training_set = sys.argv[3]
    validation_set = sys.argv[4]
    test_set = sys.argv[5]
    to_print = sys.argv[6]

    if to_print.upper() != 'YES' and to_print.upper() != 'NO':
        print "to_print argument can take either 'Yes' or 'No', given = %s" % to_print
        return False
    elif to_print.upper() == 'YES':
        to_print = True
    else:
        to_print = False
 
    status, tr_set = get_dict(training_set)
    if not status:
        logging.error("unable to load training data set.")
        return False

    status, te_set = get_dict(test_set)
    if not status:
        logging.error("unable to load testing data set.")
        return False

    status, v_set = get_dict(validation_set)
    if not status:
        logging.error("unable to load validating data set.")
        return False

    dec_tree = decision_tree(tr_set, through_entropy=True)
    if to_print:
        print_decision_tree(dec_tree)

    accuracy = validate(v_set, dec_tree)
    print str(accuracy) + " is accuracy of validation set with entropy"
    print str(validate(te_set, dec_tree)) + " is accuracy of test set with entropy"

    hearistic_dec_tree = decision_tree(tr_set, through_entropy=False)
    accuracy = validate(v_set, hearistic_dec_tree)
    print str(accuracy) + " is accuracy of validation set with impurity heuristic."
    print str(validate(te_set, hearistic_dec_tree)) + " is accuracy of test set with impurity heuristic"
    return True

if __name__ == "__main__":
    LOG_DIR = "/tmp/"
    LOG_BASE_FILE = "decision_trees_"
    LOG_FILE = "".join([LOG_DIR, LOG_BASE_FILE,
                        datetime.now().strftime("%Y%m%d_%H%M%S_%f"), ".log"])
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    open(LOG_FILE, 'a').close()  # create log file if not present
    print "LOG_FILE = %s" %LOG_FILE
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    
    if not main():
        sys.exit(-1)
