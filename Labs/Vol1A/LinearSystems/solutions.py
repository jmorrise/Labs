# solutions.py
"""Volume I: Linear Systems. Solutions file."""

import numpy as np
from time import time
from scipy import sparse
from scipy import linalg as la
from scipy.sparse import linalg as spla
from matplotlib import pyplot as plt


# Problem 1
def ref(A):
    """Reduce the square matrix A to REF. You may assume that A is invertible
    and that a 0 will never appear on the main diagonal. Avoid operating on
    entries that you know will be 0 before and after a row operation.
    """
    A = np.array(A, dtype=np.float, copy=True)
    m,n = A.shape
    for j in xrange(n):
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    return A


# Problem 2
def lu(A):
    """Compute the LU decomposition of the square matrix A. You may assume the
    decomposition exists and requires no row swaps.
    """
    m, n = A.shape
    U = np.array(A, dtype=np.float, copy=True)
    L = np.eye(n)
    for j in xrange(n):
        for i in xrange(j+1, m):
            L[i,j] = U[i,j]/U[j,j]
            U[i,j:] -= L[i,j]*U[j,j:]
    return L,U


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may assume that A is invertible (hence square).
    """
    A, b = np.array(A), np.ravel(b)
    m, n = A.shape
    assert m == n, "Matrix must be square."
    assert b.size == m, "Bad shape!"

    L, U = lu(A)

    # First solve Ly = Pb (assume P = I).
    y = np.zeros(n)
    for k in xrange(n):
        y[k] = b[k] - np.dot(L[k,:k], y[:k])

    # Now solve Ux = y.
    x = np.zeros(n)
    for k in reversed(xrange(n)):
        x[k] = (y[k] - np.dot(U[k,k:], x[k:])) / U[k,k]

    return x


# Problem 4
def prob4(N=12):
    """Time different scipy.linalg functions for solving square linear systems.
    Plot the system size versus the execution times. Use log scales if needed.
    """
    domain = 2**np.arange(1,N+1)
    inv, solve, lu_factor, lu_solve = [], [], [], []

    for n in domain:
        A = np.random.random((n,n))
        b = np.random.random(n)

        start = time()
        la.inv(A).dot(b)
        inv.append(time()-start)

        start = time()
        la.solve(A, b)
        solve.append(time()-start)

        start = time()
        x = la.lu_factor(A)
        la.lu_solve(x, b)
        lu_factor.append(time()-start)

        start = time()
        la.lu_solve(x, b)
        lu_solve.append(time()-start)

    plt.subplot(121)
    plt.plot(domain, inv, '.-', lw=2, label="la.inv()")
    plt.plot(domain, solve, '.-', lw=2, label="la.solve()")
    plt.plot(domain, lu_factor, '.-', lw=2,
                                        label="la.lu_factor() + la.lu_solve()")
    plt.plot(domain, lu_solve, '.-', lw=2, label="la.lu_solve() alone")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, inv, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, solve, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_factor, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_solve, '.-', basex=2, basey=2, lw=2)
    plt.xlabel("n")

    plt.suptitle("Problem 4 Solution")
    plt.show()


# Problem 5
def prob5(n):
    """Return a sparse n x n tridiagonal matrix with 2's along the main
    diagonal and -1's along the first sub- and super-diagonals.
    """
    return sparse.diags([2,-1,2], [-1,0,1], shape=(n,n))


# Problem 6
def prob6(N=10):
    """Time regular and sparse linear system solvers. Plot the system size
    versus the execution times. As always, use log scales where appropriate.
    """
    domain = 2**np.arange(2,N+1)
    solve, spsolve = [], []

    for n in domain:
        A = prob5(n).tocsr()
        b = np.random.random(n)

        start = time()
        spla.spsolve(A, b)
        spsolve.append(time()-start)

        A = A.toarray()
        start = time()
        la.solve(A, b)
        solve.append(time()-start)

    plt.subplot(121)
    plt.plot(domain, spsolve, '.-', lw=2, label="spla.spsolve()")
    plt.plot(domain, solve, '.-', lw=2, label="la.solve()")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, spsolve, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, solve, '.-', basex=2, basey=2, lw=2)
    plt.xlabel("n")

    plt.suptitle("Problem 6 Solution")
    plt.show()


# Additional Material =========================================================

def ref_with_swaps(A):
    """Reduce an mxn matrix to REF, using row swaps if necessary.
    This is only one of a few ways to do it.
    """
    A = np.array(A, dtype=float, copy=True)
    m,n = A.shape
    for j in xrange(min(m, n) - 1):
        # Deal with 0's on the diagonal.
        if np.allclose(A[j:,j], np.zeros(m-i)):
            continue
        while np.isclose(A[j,j], 0):
            A[j:] = np.roll(A[j:], -1, axis=0)
        # Zero out the rows below the current entry.
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    # Set extra rows to zero.
    if m > n:
        A[n:] = 0
    return A