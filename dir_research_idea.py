### Idée-squelette de la recherche de direction.

import numpy as np

# Iterations on k :
def compute_dir(new_y,y_queue,s_queue,M):
    q = new_y
    alpha = 0
    for i in range(M):
        y = y_queue[i]
        if y is None:
            break
        s = s_queue[i]
        p = np.dot(y,s)                  # [To Parallelize] Scalar product
        alpha = np.dot(s,q) / p          # [TP] Scalar product
        q -= alpha * y

    r = q
    beta = 0
    for i in range(M):
        y = y_queue[i]
        if y is None:
            break
        s = s_queue[i]
        p = np.dot(y,s)                  # [TP] Scalar product
        beta = np.dot(y,r) / p           # [TP] Scalar product
        r += beta * y
    return -r