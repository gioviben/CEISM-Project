import numpy as np
from mpi4py import MPI 

def compute_dir_parallel(g_chunk, y_queue, s_queue, M, comm):
    """
    Parallel L-BFGS two-loop recursion algorithm.
    Takes local chunks of the vectors as input and uses MPI Allreduce 
    to compute the global dot products across all processes.
    """
    # Initialize q with the local portion of the gradient
    q = g_chunk.copy() 
    alphas = np.zeros(M)
    
    # First loop (backward pass)
    for i in range(len(y_queue)):
        y = y_queue[i]
        s = s_queue[i]
        
        # Parallel dot product <y, s>
        local_p = np.dot(y, s)
        p = comm.allreduce(local_p, op=MPI.SUM)
        
        # Safeguard against division by zero (or negative curvature)
        if p <= 1e-10: 
            break
            
        # Parallel dot product <s, q>
        local_sq = np.dot(s, q)
        global_sq = comm.allreduce(local_sq, op=MPI.SUM)
        
        # Calculate and store alpha for the forward pass
        alphas[i] = global_sq / p
        q -= alphas[i] * y 

    # Implicitly assuming the initial inverse Hessian approximation (H0) 
    # is the Identity matrix, so r = H0 * q becomes r = q
    r = q.copy()
    beta = 0
    
    # Second loop (forward pass)
    for i in reversed(range(len(y_queue))):
        y = y_queue[i]
        s = s_queue[i]
        
        # Recompute parallel dot product <y, s> 
        # (Note: this could potentially be cached from the backward pass to save MPI calls)
        local_p = np.dot(y, s)
        p = comm.allreduce(local_p, op=MPI.SUM)
        
        if p <= 1e-10:
            continue
            
        # Parallel dot product <y, r>
        local_yr = np.dot(y, r)
        global_yr = comm.allreduce(local_yr, op=MPI.SUM)
        
        # Calculate beta and update r
        beta = global_yr / p
        r += s * (alphas[i] - beta)
        
    # Return the local chunk of the descent direction (-H * g)
    return -r