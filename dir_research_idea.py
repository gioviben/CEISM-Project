### Idée-squelette de la recherche de direction.

from collections import deque
import numpy as np

# Iterations on k :
def compute_dir(La,y_queue,s_queue, la_k,grad_la_k):
    La.pop()
    La.appendleft(la_k)
    Grads_la.pop()
    Grads_la.appendleft(grad_la_k)

    new_y = Grads_la[0] - Grads_la[1]
    new_s = La[0] - La[1]
    y_queue.pop()
    y_queue.appendleft(new_y)
    s_queue.pop()
    s_queue.appendleft(new_s)

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

    r *= -1
    return r

## Initialization : to be put OUTSIDE the loop on k
M = 5
D = ... ### problem size : TO BE MODIFIED
y_la_queue = deque([None for _ in range(M)])
s_la_queue = deque([None for _ in range(M)])
y_mu_queue = deque([None for _ in range(M)])
s_mu_queue = deque([None for _ in range(M)])
Grads_la = deque([None, None])
Grads_mu = deque([None, None])
La = deque([None, None])
Mu = deque([None, None])

## Implementation INSIDE the loop on k : after STEP 8 (compute gradients) and before STEP 10 (Backtracking Line Search)
grad_la_k, grad_mu_k = ... , ... ### RETRIEVE FROM STEP 8
dir_la , dir_mu = compute_dir(La,y_la_queue,la_k,grad_la_k) , compute_dir(Mu,y_mu_queue,mu_k,grad_mu_k)
# dir_la , dir_mu : INPUTS of STEP 10 (BLS)