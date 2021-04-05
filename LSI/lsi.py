import os
import numpy as np
from numpy import linalg as lg


def svd_approximate(matrix, approx):
    """
    Computes approximated SVD from given matrix.
    :param matrix: term-by-document matirix
    :param approx: approximation for faster calculations
    :return: final_u - decomposed matrix U_k
             diag_m - diagonal matrix kxk with eigenvalues in decreasing order
             final_v - decomposed matrix V_k
    """
    # Get matrixes
    a = matrix
    a_t = matrix.transpose()

    # Compute U = AA^T and V = A^TA
    u = np.dot(a, a_t)
    v = np.dot(a_t, a)

    # Check for correct size of matrix
    if v.shape[0] < approx:
        approx = v.shape[0]

    if v.shape[1] < approx:
        approx = v.shape[1]

    # Compute eigen vectors of correlation matrix of terms
    u_eig_val, u_eig_vec = lg.eig(u)
    # Approximates matrix
    final_u = u_eig_vec[:, 0:approx]
    # print("Dimensions of Matrix U:",final_u.shape)

    # Compute eigen vectors of correlation matrix of documents
    v_eig_val, v_eig_vec = lg.eig(v)
    # Approximates matrix
    final_v = v_eig_vec.transpose()[:approx, :]
    # print("Dimensions of Matrix V", final_v.shape)

    s = u[0:approx, 0:approx]
    s_eig_val, s_eig_vec = lg.eig(s)
    eig_values = sorted(s_eig_val, reverse=True)
    # eig_values = sorted(v_eig_val, reverse=True)
    diag_m = np.diag(eig_values)[0:approx, 0:approx]
    print(diag_m)

    return final_u, diag_m, final_v


def svd(matrix, approx=50):
    """
        Saves computed and decomposed values for further usage.
        :param matrix: term-by-document matrix
        :param approx: approximation for faster calculations, default value is 50
        :return: final_u - decomposed matrix U_k
        """
    u_k, s_k, v_k = svd_approximate(matrix, approx)
    print(u_k.shape)
    print(s_k.shape)
    print(v_k.shape)

    d_k = np.dot(s_k, v_k)
    print(d_k)

    # TODO: Save approximated values, they should be calculated only once and recalculated if needed.
