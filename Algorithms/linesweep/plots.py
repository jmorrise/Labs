# This plotting file is rather old code.
# It generates a full set of plots illustrating the two different linesweep
# algorithms on randomly chosen points.
# It should be updated at some point so that the random number generator
# is seeded with some specifically chosen seed that generates plots that
# illustrate the algorithms well.
# This isn't currently an issue since the plots already conform to
# project standards, but if we ever want to standardize plot generation
# this will have to be taken care of.

import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')
from matplotlib import pyplot as plt
import numpy as np
from numpy.random import rand
import bisect as bs

# This generates the plots for the simplified linsweep.
# It generates more plots than are actually used in the lab.
# I just picked the plots that were useful in illustrating the algorithm.

def multidist(p0, p1):
    l = len(p0)
    return (sum([(p0[i] - p1[i])**2 for i in range(l)]))**(.5)

def mindist_simple_plot(Y):
    X = Y.take(Y[:,0].argsort(), axis=0)
    n = len(X)
    actives = []
    pt = tuple(X[0])
    actives.append(pt)
    pt = tuple(X[1])
    actives.append(pt)
    r = multidist(actives[0], actives[1])
    for i in xrange(2, len(X)):
        pt = tuple(X[i])
        l = len(actives)
        while l > 0:
            if actives[0][0] > pt[0] + r:
                actives.pop(0)
                l -= 1
            else:
                break
        plt.scatter(X[:,0], X[:,1])
        res = 15
        T = np.linspace(-.2, 1.2, res)
        res2 = 201
        theta = np.linspace(np.pi/2, 3*np.pi/2, res2)
        plt.plot([pt[0]]*res, T, color='r')
        plt.plot([pt[0]-r]*res, T, color='r')
        X0 = np.array([pt + r * np.array([np.cos(t), np.sin(t)]) for t in theta])
        plt.plot(X0[:,0], X0[:,1], color='g')
        plt.xlim((-.2, 1.2))
        plt.ylim((-.2, 1.2))
        plt.show()
        for k in xrange(len(actives)):
            d = multidist(pt, actives[k])
            if d < r:
                r = d
        actives.append(pt)
    return r

# This generates the plots for the full version.
# It generates more plots than are actually used in the lab.
# I just picked the plots that were useful in illustrating the algorithm.

def mindist_plot(Y):
    X = Y.take(Y[:,0].argsort(), axis=0)
    n = len(X)
    actives = []
    pt = X[0]
    actives.insert(bs.bisect_left(actives, tuple(reversed(tuple(pt)))), tuple(reversed(tuple(pt))))
    pt = X[1]
    actives.insert(bs.bisect_left(actives, tuple(reversed(tuple(pt)))), tuple(reversed(tuple(pt))))
    r = multidist(actives[0], actives[1])
    for i in xrange(2, n):
        plt.scatter(X[:,0], X[:,1])
        pt = tuple(X[i])
        res = 1401
        x = np.linspace(-.2, 1.2, res)
        plt.plot(x, [pt[1] - r] * res, color='r')
        plt.plot(x, [pt[1] + r] * res, color='r')
        plt.plot([pt[0]] * res, x, color='b')
        plt.plot([pt[0] - r] * res, x, color='b')
        T = np.linspace(np.pi / 2, 3 * np.pi / 2, res)
        pt = np.array(pt)
        X0 = np.array([pt + r * np.array([np.cos(t), np.sin(t)]) for t in T])
        plt.plot(X0[:,0], X0[:,1], color='g')
        block = actives[bs.bisect_left(actives, (pt[1] - r, pt[0] - r)): bs.bisect_right(actives, (pt[1] + r, pt[0]))]
        for k in xrange(len(block)):
            d = multidist(tuple(reversed(tuple(pt))), block[k])
            if d < r:
                r = d
        removalidx = 0
        while removalidx < len(actives):
            if abs(actives[removalidx][1] - pt[0]) > r:
                actives.pop(removalidx)
            else:
                removalidx += 1
        if len(actives) > 0:
            plt.scatter(np.fliplr(np.array(actives))[:,0], np.fliplr(np.array(actives))[:,1])
        if len(block) > 0:
            plt.scatter(np.fliplr(np.array(block))[:,0], np.fliplr(np.array(block))[:,1])
        plt.show()
        actives.insert(bs.bisect_left(actives, tuple(reversed(tuple(pt)))), tuple(reversed(tuple(pt))))
    return r

if __name__=="__main__":
    # Generate the plots for the simplified algorithm.
    X = rand(10, 2)
    mindist3plot(X)
    # Generate the plots for the full algorithm.
    X = rand(25, 2)
    mindistplot(X)
