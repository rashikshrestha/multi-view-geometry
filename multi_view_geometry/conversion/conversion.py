import numpy as np

def q2R(q):
    """
    Quaternion to Rotation Matrix.
    Code adapted from: https://github.com/colmap/colmap/blob/main/scripts/python/read_write_model.py
    """
    return np.array([
        [1 - 2 * q[2]**2 - 2 * q[3]**2,
         2 * q[1] * q[2] - 2 * q[0] * q[3],
         2 * q[3] * q[1] + 2 * q[0] * q[2]],
        [2 * q[1] * q[2] + 2 * q[0] * q[3],
         1 - 2 * q[1]**2 - 2 * q[3]**2,
         2 * q[2] * q[3] - 2 * q[0] * q[1]],
        [2 * q[3] * q[1] - 2 * q[0] * q[2],
         2 * q[2] * q[3] + 2 * q[0] * q[1],
         1 - 2 * q[1]**2 - 2 * q[2]**2]])


def R2q(R):
    """
    Rotation Matrix to Quaternion.
    Code adapted from: https://github.com/colmap/colmap/blob/main/scripts/python/read_write_model.py
    """
    Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz, Rzz = R.flat
    K = np.array([
        [Rxx - Ryy - Rzz, 0, 0, 0],
        [Ryx + Rxy, Ryy - Rxx - Rzz, 0, 0],
        [Rzx + Rxz, Rzy + Ryz, Rzz - Rxx - Ryy, 0],
        [Ryz - Rzy, Rzx - Rxz, Rxy - Ryx, Rxx + Ryy + Rzz]]) / 3.0
    eigvals, eigvecs = np.linalg.eigh(K)
    qvec = eigvecs[[3, 0, 1, 2], np.argmax(eigvals)]
    if qvec[0] < 0:
        qvec *= -1
    return qvec