### LBFGS ALGORITHM
import numpy as np
from mpi4py import MPI 
comm=MPI.COMM_WORLD
NbP=comm.Get_size()
Me=comm.Get_rank()

# Iterations on k :
def compute_dir(new_y,y_queue,s_queue,M):
    q = new_y.copy() #current gradient , array of dim N, one for each gll node
    alphas=np.zeros(M)
    for i in range(M):
        y = y_queue[i] #y_queue[i]= y_{k-i}= g^(k-i)-g^(k-i-1) diff between gradients  
        if y is None:
            break
        s = s_queue[i]
        p = np.dot(y,s)                  # [To Parallelize] Scalar product
        if p<=0:
            break
        alphas[i] = np.dot(s,q) / p          # [TP] Scalar product
        q -= alphas[i] * y #element-per-element update 

    r =  q
    beta = 0
    for i in reversed(range(M)):
        y = y_queue[i]
        if y is None:
            continue
        s = s_queue[i]
        p = np.dot(y,s)                  # [TP] Scalar product
        if p <= 0:
            continue
        beta = np.dot(y,r) / p           # [TP] Scalar product
        r += s*(alphas[i]-beta)
    return -r