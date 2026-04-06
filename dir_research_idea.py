### LBFGS ALGORITHM
import mpi4py
import numpy as np

# Iterations on k :
def compute_dir(new_y,y_queue,s_queue,M):
    q = new_y #current gradient 
    alphas=np.zeros(M)
    for i in range(M):
        y = y_queue[i] #y_queue[i]= y_{k-i}= g^(k-i)-g^(k-i-1) diff between gradients  
        if y is None:
            break
        s = s_queue[i]
        p = np.dot(y,s)                  # [To Parallelize] Scalar product
        alphas[i] = np.dot(s,q) / p          # [TP] Scalar product
        q -= alphas[i] * y

    r =  q
    beta = 0
    for i in reversed(range(M)):
        y = y_queue[i]
        if y is None:
            break
        s = s_queue[i]
        p = np.dot(y,s)                  # [TP] Scalar product
        beta = np.dot(y,r) / p           # [TP] Scalar product
        r += s*(alphas[i]-beta)
    return -r