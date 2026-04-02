# -*- coding: utf-8 -*-
import h5py
import numpy as np
# Steps :
# We have to overwrite each time we do an iteration of the Backtracking Line Search.
# [Pre] 1. Get the gradients by time and space integration
# [Pre] 2. Solve with the approximated Hessian the search directions
# Then, we enter the BLS :
# 1. Replace Lambda by Lambda + alpha*dir (same for Mu).
# alpha = 0.5^k at the k-th iteration of the BLS ; dir = remains the same during a BLS loop.
# Challenge : dir is a BIG vector (# elems = # elems of the mesh). We would actually like it to be a grid.
# --> Define a bijective mapping : grid (3D) --> vector (1D) to compute the gradients and then the directions (with L-BFGS)
# --> Apply the inverse to then overwrite the files :

initial_names = {'Mu':'/workdir/match/mu.h5',
    'La':'workdir/match/la.h5'}

# Define fmesh at initialization :
initial_name  = initial_names['Mu'] # For example (just for the initialization. We could have taken La as well.)
initial_fmesh = h5py.File(initial_name,"r+") ####

# Global variables :
xMinGlob = initial_fmesh.attrs["xMinGlob"]  # A point in 3D. As it is a cube we can define it only with these 2 extreme points.
xMaxGlob = initial_fmesh.attrs["xMaxGlob"]
xStep    = initial_fmesh.attrs["xStep"]

xn = np.arange(xMinGlob[0],xMaxGlob[0]+xStep[0],xStep[0],float) # List of the coordinates of the cube
yn = np.arange(xMinGlob[1],xMaxGlob[1]+xStep[1],xStep[1],float)
zn = np.arange(xMinGlob[2],xMaxGlob[2]+xStep[2],xStep[2],float)
Nx,Ny,Nz = len(xn), len(yn), len(zn)
# xv,yv,zv = np.meshgrid(xn,yn,zn,sparse=False,indexing='xy')

def grid_to_vec(names,prop):
    """Transforms an h5 file
    (the path of this file has to be written in the _names_ dictionary)
    into a 1D vector so that L-BFGS can deal with it.
    Args:
        names (dict): {'Mu' : '/workdir/match/init_mu.h5' , 'La' : ...}
        prop (str): 'La' or 'Mu'
    Returns:
        1D array
    """
    name = names[prop]
    fmesh = h5py.File(name,"r+")
    mat = fmesh["samples"][...]
    vec = mat.flatten()
    return vec

def vec_to_grid(vec):
    """Transforms a vector (1D) from L-BFGS into a 3D-array.
    This 3D-array will then be written into an h5 file.
    Args:
        vec (1D grid): typically a trial lambda/mu.
    Returns:
        3D grid (np.array): lambda_k or mu_k - to be converted into h5 format.
    """
    grid = np.zeros((Nx,Ny,Nz))
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                grid[i,j,k] = vec[Ny*Nz*i + Nz*j + k]
    return grid

def modify_h5(h5_path,vec_to_add):
    fmesh = h5py.File(h5_path,"r+")
    mat = fmesh["samples"][...]
    grid_to_add = vec_to_grid(vec_to_add)
    mat += grid_to_add
    del fmesh["samples"]
    dset = fmesh.create_dataset('samples',data=mat)
    return None

def backtracking_line_search(s_la_k,s_mu_k,g_la_k,g_mu_k,J_k,line_search_params={"alpha_la":1, "alpha_mu":1 , "c1":1e-4 , "xi":0.5}):
    """Updates the h5 files (la.h5 and mu.h5) through the backtracking line search.
    Args:
        s_la_k (1D np.array): recovered from 
        s_mu_k (1D np.array): _description_
        g_la_k (1D np.array): _description_
        g_mu_k (1D np.array): _description_
        J_k (float): _description_
    """
    ## Initialization ##
    alpha_la, alpha_mu , c1, xi = line_search_params["alpha_la"] , line_search_params["alpha_mu"], line_search_params["c1"], line_search_params["xi"]
    J_thresh = J_k + c1(alpha_la*np.dot(s_la_k,g_la_k) + alpha_mu*np.dot(s_mu_k,g_mu_k))
    J_learn = np.inf

    vec_to_add_la, vec_to_add_mu = 2*alpha_la*s_la_k , 2*alpha_mu*s_mu_k
    modify_h5('/workdir/match/la.h5',vec_to_add_la)
    modify_h5('/workdir/match/mu.h5',vec_to_add_mu)

    ## Backtracking loop ##
    while J_learn >= J_thresh:
        vec_to_add_la -= alpha_la*s_la_k
        vec_to_add_mu -= alpha_mu*s_mu_k
        modify_h5('/workdir/match/la.h5',vec_to_add_la)
        print("la.h5 modified",flush=True)
        modify_h5('/workdir/match/mu.h5',vec_to_add_mu)
        print("mu.h5 modified",flush=True)
        ###Lauch SEM3D ('/workdir/match/la.h5','/workdir/match/mu.h5' have just been updated ###
        ### Call sbatch SOLVER and go get the traces and Uobs ###
        J_learn = compute_misfit(traces_path,Uobs) # to be modified
        alpha_la *= xi
        alpha_mu *= xi
    # At the end of the loop, la.h5 and mu.h5 are updated,
    # and we can launch again a {Forward + Adjoint + BLS} process
    return None
