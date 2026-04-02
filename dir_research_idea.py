### Idée-squelette de la recherche de direction.

from collections import deque
import numpy as np

M = 5
D = # problem size
y_queue = deque([None for _ in range(M)])
s_queue = deque([None for _ in range(M)])
grads_la = deque([None, None])
grads_mu = deque([None, None])
La = deque([None, None])
Mu = deque([None, None])
# Iterations on k
args : la_k,mu_k,grad_la_k,grad_mu_k
La.pop()
La.appendleft(la_k)
Mu.pop()
Mu.appendleft(mu_k)
grads_la.pop()
grads_la.appendleft(grad_la_k)
grads_mu.pop()
grads_mu.appendleft(grad_mu_k)

new_y = grads_la[0] - grads_la[1]
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
    else:
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
    else:
        s = s_queue[i]
        p = np.dot(y,s)                  # [TP] Scalar product
        beta = np.dot(y,r) / p           # [TP] Scalar product
        r += beta * y

r *= -1
return r
