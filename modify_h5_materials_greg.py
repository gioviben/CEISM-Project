# -*- coding: utf-8 -*-
import h5py
import numpy as np
from sbatch_and_wait import sbatch_and_wait
from compute_misfit import compute_misfit

### TO BE MODIFIED, in order to correspond to the directory where lambda and mu are stored.
file_paths = {'Mu':'/workdir/match/mu.h5','La':'workdir/match/la.h5'}
###________________________________________________________________________________________


# Define fmesh at initialization :
initial_name  = file_paths['Mu'] # For example (just for the initialization. We could have taken La as well.)
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
        s_la_k (1D np.array): retrieved from step 9
        s_mu_k (1D np.array): _description_
        g_la_k (1D np.array): retrieved from step 8
        g_mu_k (1D np.array): _description_
        J_k (float): value of the misfit obtained at step k
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
        # Launch SEM3D ('/workdir/match/la.h5','/workdir/match/mu.h5' have just been updated
        # Call sbatch SOLVER, and then get the traces and Uobs
        sbatch_and_wait("SOLVER.sbatch")
        TRACES_SIMULATED_FOLDER_PATH = ... ### TO BE MODIFIED
        obs_u = ... ### TO BE MODIFIED
        J_learn = compute_misfit(TRACES_SIMULATED_FOLDER_PATH,obs_u)
        alpha_la *= xi
        alpha_mu *= xi
    # At the end of the loop, la.h5 and mu.h5 are updated,
    # and we can launch again a {Forward + Adjoint + BLS} process
    return None
