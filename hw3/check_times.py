import time
import math
import numpy as np

def timeit1():
    s = time.time()
    for i in xrange(750000):
        z=(i**.5)**.5
    print "sqrt Took %f seconds" % (time.time() - s)

def timeit2(arg=math.sqrt):
    s = time.time()
    for i in xrange(750000):
        z=arg(arg(i))
    print "math.sqrt Took %f seconds" % (time.time() - s)

def timeit3(arg=np.sqrt):
    s = time.time()
    for i in xrange(750000):
        z=arg(arg(i))
    print "np.sqrt Took %f seconds" % (time.time() - s)


timeit1()
timeit2()
timeit3()
