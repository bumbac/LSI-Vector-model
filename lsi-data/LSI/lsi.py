import os
import numpy as np
from numpy import linalg as lg


def svd_approximate(matrix):
    """
    Computes approximated SVD from given matrix.
    :param matrix: term-by-document matrix
    :param approx: approximation for faster calculations
    :return: _u - decomposed matrix U_k
             sigma - diagonal matrix kxk with eigenvalues in decreasing order
             _v - decomposed matrix V_k
    """
    # Get matrix
    a = matrix

    # Linag SVD
    _u, _s, _v = lg.svd(a, full_matrices=False)

    print("_u: ", np.shape(_u))
    print("_v: ", np.shape(_v))

    # approx = _v.shape[1]

    # Approximate
    # _v = _v[:approx, :]
    # _u = _u[:, :approx]

    sigma = np.zeros(shape=(len(_s), len(_s)))
    for diag in range(sigma.shape[1]):
        sigma[diag, diag] = _s[diag]

    return _u, sigma, _v


def svd(matrix):
    """
        Saves computed and decomposed values for further usage.
        :param matrix: term-by-document matrix
        :param approx: approximation for faster calculations, default value is 50
        :return: final_u - decomposed matrix U_k
        """

    u_k, s_k, v_k = svd_approximate(matrix)
    d_k = np.dot(s_k, v_k)
    s_k_inv = lg.inv(s_k)

    # return {"U": u_k, "S": s_k, "V": v_k, "D": d_k, "S_inv": s_k_inv}
    return {"V": v_k, "D": d_k, "S_inv": s_k_inv}
