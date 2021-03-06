#!/usr/bin/env python
import logging
import argparse
import numpy as np, numpy.random
from random import randint
import math, time, os

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


class EM(object):
    """ This class implements the expectation maximization algorithm."""
    def __init__(self, input_file, constVar=False, K=3):
        """Initialize the variables required by the EM class"""
        self.input_file = input_file
        self.data = []
        self.Num_inputs = 0
        self.alpha = []
        self.alpha_new = []
        self.mu = []
        self.var = [] 
        self.Weights = []
        self.data_mean = 0.0
        self.data_var = 0.0
        self.K = K
        self.Var = 1.0
        self.constVar = constVar
        
    def initialize(self, alpha=None, mu=None):
        """Initializes different variables"""
        self.read_file()
        self.init_alpha(alpha)
        self.init_Weights()
        self.init_mu(mu)
        self.init_var()
        
    def init_alpha(self, alpha=None):
        """ Initializes alpha with random values."""
        if alpha is None:
            randNums = np.random.dirichlet(np.ones(self.K),size=1)[0]
            i = 0
            for num in randNums:
                self.alpha.append(num)
                self.alpha_new.append(num)
                logging.info("Random alpha at " + str(i) + " is " + str(num));
                i += 1
        else:
            for num in alpha:
                self.alpha.append(num)
                self.alpha_new.append(num)

    def init_Weights(self):
        """ This function is used to initialize the weights."""
        i = 0
        while (i < self.Num_inputs):
            l = []
            j = 0
            while ( j < self.K):
                l.append(0)
                j += 1
            self.Weights.append(l)
            i += 1

    def init_mu(self, mu=None):
        """ This function initializes mu"""
        if mu is None:
            i = 0
            while (i < self.K):
                self.mu.append(self.data[randint(0, self.Num_inputs -1)])
                logging.info("mu at pos " + str(i) + " is " + str(self.mu[i]))
                i += 1
        else:
            self.mu.extend(mu)

    def init_var(self):
        """ This function initializes variance."""
        i = 0
        if self.constVar:
            while (i < self.K):
                self.var.append(self.Var)
                i += 1
        else:
            while (i < self.K):
                self.var.append(self.data_var * (1+randint(0, self.Num_inputs -1)%5))
                logging.info("var at pos " + str(i) + " is " + str(self.var[i]))
                i += 1

    def read_file(self):
        """ Reads the input file and stores the data in data variable."""
        fd = open(self.input_file, "r")
        content =  fd.readlines()
        fd.close()
        
        for line in content:
            self.data.append(float(line))
            self.data_mean += float(line)
            self.Num_inputs += 1

        logging.info("Number of inputs = " + str(self.Num_inputs))
        self.data_mean = self.data_mean/self.Num_inputs
        logging.info("Data mean = " + str(self.data_mean))

        for data_point in self.data:
            self.data_var += (data_point-self.data_mean) * (data_point-self.data_mean);
        self.data_var = self.data_var/self.Num_inputs;
        logging.info("Data var = " + str(self.data_var))

    def expectation_step(self):
        """ Computes the expectation for each point."""
        for i in xrange(self.Num_inputs):
            sum = 0.0
            l = []
            for j in xrange(self.K):
                l.append(self.alpha[j] * self.probability(i, j))
                sum += l[j] * l[j]

            sum = math.sqrt(sum)
            for j in xrange(self.K):
                if sum == 0:
                    logging.WARN("Sum at index " + str(j) + " is 0")
                    l[j] = 0
                else:
                    l[j] = l[j]/sum
                    logging.info("expectation at " + str(i) +"," + str(j) +
                                 " is " + str(l[j]));
            self.Weights[i] = l

    def probability(self, i, j):
        """ Calculates the probability."""
        x_mu = self.data[i] - self.mu[j]
        num = math.exp(-(x_mu * x_mu)/(2*self.var[j]))
        den = math.sqrt(2 * math.pi * self.var[j]);
        res = num/den
        logging.info("probability for " + str(i) +"," + str(j) + " is " +
                     str(res))
        return res

    def maximization_step(self):
        """ Maximizes the expectation calculated"""
        N = []
        d0 = 0.0
        for j in xrange(self.K):
            n0 = 0.0
            N.append(0.0)
            for i in xrange(self.Num_inputs):
                N[j] += self.Weights[i][j]
                n0 += self.Weights[i][j] * self.data[i]
            self.alpha_new[j] = N[j]/self.Num_inputs;
            d0 += self.alpha_new[j] * self.alpha_new[j]
            self.mu[j] = n0/N[j]

            n1 = 0.0
            for i in xrange(self.Num_inputs):
                n1 += self.Weights[i][j] * (self.data[i] - self.mu[j]) *\
                      (self.data[i] - self.mu[j])
            if not self.constVar:
                self.var[j] = n1/N[j]
            logging.info("Variance at " + str(j) + " is " + str(self.var[j]))

        d0 = math.sqrt(d0)
        for i in xrange(self.K):
            if d0 == 0:
                self.alpha_new[i] = 0
                logging.WARN("new alpha at index " + str(i) + " is 0")
            else:
                self.alpha_new[i] = self.alpha_new[i]/d0
            logging.info("new alpha at " + str(i) + " is " + str(self.alpha_new[i]))

    def check_convergence(self):
        """ Checks for the convergence."""
        diff = 0.0
        for i in xrange(self.K):
            diff += math.fabs(self.alpha[i] - self.alpha_new[i])
            logging.info("convergence difference is " + str(diff))
            if diff > 0.0001:
                return False
        return True

    def run(self):
        """ Runs the EM algorithm on given file."""
        loop = True
        iterations = 0
        self.print_stats(iterations, True)
        while loop:
            self.expectation_step()
            self.maximization_step()
            if self.check_convergence():
                loop = False
            for i in xrange(self.K):
                self.alpha[i] = self.alpha_new[i]
            iterations += 1
            logging.info("iterations = " +  str(iterations))

        self.print_stats(iterations)

    def print_stats(self, iterations, initial=False):
        """ Prints the EM Statistics."""
        if initial:
            print "INITIAL STATS\n"
        else:
            print "FINAL STATS\n"
            print "NUMBER OF ITERATIONS = %d\n" % iterations
            
        print "\nMEANS"
        i = 1
        for m in self.mu:
            print "mu at index %d = %f" % (i, m)
            i += 1
        
        print "\nVARIANCE"
        i = 1
        for v in self.var:
            print "variance at index %d = %f" % (i, v)
            i += 1

        print "\nALPHA"
        i = 1
        for a in self.alpha:
            print "alpha at index %d = %f" % (i, a)
            i += 1


def main():
    """Control block of the program."""
    parser = argparse.ArgumentParser(prog='em.py')
    parser.add_argument('-f', nargs=1, required=True,
                        help="input file.")
    parser.add_argument('-k', nargs=1, type=int,
                        help="Number of clusters")
    parser.add_argument('-d', nargs=1, required=False,
                        choices=LEVELS.keys(),
                        help="Level of debugging")
    parser.add_argument('-a', nargs='+', required=False,
                        type=float, help="Alpha values")
    args = parser.parse_args()
    log_file = "em_%s.log" % time.strftime("%Y%m%d_%H%M%S")
    log_dir = "./em_logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    open(log_dir + log_file, 'a').close()  # Create log file if not present.
    if args.d is not None:
        logging.basicConfig(filename=log_dir + log_file,
                            level=LEVELS.get(args.d[0]))
    else:
        logging.basicConfig(filename=log_dir + log_file,
                            level=logging.WARNING)
    
    print "**************With Variable Variance**************\n\n"
    if args.k is None:
        em = EM(args.f[0])
    else:
        em = EM(args.f[0], K=args.k[0])
    em.initialize(alpha=args.a)
    a = []
    a.extend(em.alpha)
    mu = []
    mu.extend(em.mu)
    em.run()
    
    print "\n\n**************With Constant Variance**************\n\n"
    if args.k is None:
        em = EM(args.f[0], constVar=True)
    else:
        em = EM(args.f[0], constVar=True, K=args.k[0])
    em.initialize(a, mu)
    em.run()


if __name__ == "__main__":
    """Start of program."""
    main()
