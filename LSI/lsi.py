import os
import numpy as np
from numpy import linalg as lg


def svd_approximate(matrix, approx):
    """
    Computes approximated SVD from given matrix.
    :param matrix: term-by-document matrix
    :param approx: approximation for faster calculations
    :return: final_u - decomposed matrix U_k
             diag_m - diagonal matrix kxk with eigenvalues in decreasing order
             final_v - decomposed matrix V_k
    """
    print("CALCULATING SVD\n\n")
    print("THIS WILL TAKE SOME TIME")
    # Get matrices
    a = matrix
    a_t = matrix.transpose()
    print("MATRIX SHAPE:", a.shape)

    # Compute U = AA^T and V = A^TA
    u = np.dot(a, a_t)
    v = np.dot(a_t, a)
    print("U = A {dot} A^T COMPLETE")
    print("V = A^T {dot} A COMPLETE")
    print("\n\nCALCULATING EIGEN VECTORS AND VALUES")
    print("THIS WILL TAKE SOME TIME\n\n")
    # Check for correct size of matrix
    if v.shape[0] < approx:
        approx = v.shape[0]

    if v.shape[1] < approx:
        approx = v.shape[1]

    # Compute eigen vectors of correlation matrix of terms
    u_eig_val, u_eig_vec = lg.eig(u)
    print("U EIGEN VECTORS COMPLETE")
    print("U EIGEN VALUES COMPLETE")
    # Approximates matrix
    final_u = u_eig_vec[:, 0:approx]
    # print("Dimensions of Matrix U:",final_u.shape)

    # Compute eigen vectors of correlation matrix of documents
    v_eig_val, v_eig_vec = lg.eig(v)
    print("V EIGEN VECTORS COMPLETE")
    print("V EIGEN VALUES COMPLETE")
    # Approximates matrix
    final_v = v_eig_vec.transpose()[:approx, :]
    # print("Dimensions of Matrix V", final_v.shape)

    s = u[0:approx, 0:approx]
    s_eig_val, s_eig_vec = lg.eig(s)
    print("S EIGEN VECTORS COMPLETE")
    print("S EIGEN VALUES COMPLETE")
    eig_values = sorted(s_eig_val, reverse=True)
    # eig_values = sorted(v_eig_val, reverse=True)
    diag_m = np.diag(eig_values)[0:approx, 0:approx]
    # print(diag_m)

    return final_u, diag_m, final_v


def svd(matrix, approx=50):
    """
        Saves computed and decomposed values for further usage.
        :param matrix: term-by-document matrix
        :param approx: approximation for faster calculations, default value is 50
        :return: final_u - decomposed matrix U_k
        """
    save_matrix = False
    u_k, s_k, v_k = svd_approximate(matrix, approx)
    print("SVD COMPLETE")
    print("SVD COMPLETE")
    print("SVD COMPLETE")
    # print(u_k.shape)
    # print(s_k.shape)
    # print(v_k.shape)

    d_k = np.dot(s_k, v_k)

    # print(d_k)
    # print(s_k)
    s_k_inv = lg.inv(s_k)
    print("S_k INVERSION COMPLETE")
    test = True
    if test:
        print("double test if inverse S^-1 works")
        print(np.allclose(np.dot(s_k, s_k_inv), np.eye(s_k.shape[0])))
        print(np.allclose(np.dot(s_k_inv, s_k), np.eye(s_k.shape[0])))
        print("S_k INVERSION TEST COMPLETE")

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
    # TODO: Save approximated values, they should be calculated only once and recalculated if needed.
