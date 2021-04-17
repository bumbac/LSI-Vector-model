import os
import numpy as np
from numpy import linalg as lg


def svd_approximate(matrix, approx):
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
    _u, _s, _v = lg.svd(a)

    # Approximate
    _v = _v[:approx, :]
    _u = _u[:, :approx]

    sigma = np.zeros(shape=(approx, approx))
    for diag in range(sigma.shape[1]):
        sigma[diag, diag] = _s[diag]

    return _u, sigma, _v


def svd(matrix, approx=10):
    """
        Saves computed and decomposed values for further usage.
        :param matrix: term-by-document matrix
        :param approx: approximation for faster calculations, default value is 50
        :return: final_u - decomposed matrix U_k
        """

    u_k, s_k, v_k = svd_approximate(matrix, approx)
    d_k = np.dot(s_k, v_k)
    s_k_inv = lg.inv(s_k)

    test = False
    if test:
        print("double test if inverse S^-1 works")
        print(np.allclose(np.dot(s_k, s_k_inv), np.eye(s_k.shape[0])))
        print(np.allclose(np.dot(s_k_inv, s_k), np.eye(s_k.shape[0])))
        print("S_k INVERSION TEST COMPLETE")

    save_matrix = False
    if save_matrix:
        u_k_file = open("U_k", "wb")
        np.save(u_k_file, u_k)
        u_k_file.close()
        s_k_file = open("S_k", "wb")
        np.save(s_k_file, s_k)
        s_k_file.close()
        v_k_file = open("V_k", "wb")
        np.save(v_k_file, v_k)
        v_k_file.close()
        d_k_file = open("D_k", "wb")
        np.save(d_k_file, d_k)
        d_k_file.close()
        s_k_inv_file = open("S_k_inv", "wb")
        np.save(s_k_inv_file, s_k_inv)
        s_k_inv_file.close()
    return {"U": u_k,
            "S": s_k,
            "V": v_k,
            "D": d_k,
            "S_inv": s_k_inv}
