# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Script read SEM3D snapshots with MPI-based algorithm

    Ex.1 : Parse Velocity snapshot files with n MPI cores
        
        mpirun --np n python3 parse_h5_snapshots.py @@wkd /path/to/sem3d/res @@var veloc

"""
# Required modules
import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize = False
from mpi4py import MPI
import glob
import argparse
from os.path import join as osj
import numpy as np
import h5py as hf
import hashlib
import debugpy
from tqdm import tqdm
import pyvista as pv

# General informations
__author__ = "Filippo Gatti"
__copyright__ = "Copyright 2020, CentraleSupélec (MSSMat UMR CNRS 8579)"
__credits__ = ["Filippo Gatti"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Filippo Gatti"
__email__ = "filippo.gatti@centralesupelec.fr"
__status__ = "Beta"

typ = {'Mass':'static','Dens':'static','Dom':'static','Elements':'static',
       'Jac':'static','Kappa':'static','Lamb':'static','Material':'static',
       'Mu':'static','Nodes':'static','Proc':'static','displ':'dynamic','veloc':'dynamic','Accel':'dynamic',
       'eps_dev_xx':'dynamic','eps_dev_xy':'dynamic','eps_dev_xz':'dynamic',
       'eps_dev_yy':'dynamic','eps_dev_yz':'dynamic','eps_dev_zz':'dynamic',
       'sig_dev_xx':'dynamic','sig_dev_xy':'dynamic','sig_dev_xz':'dynamic',
       'sig_dev_yy':'dynamic','sig_dev_yz':'dynamic','sig_dev_zz':'dynamic',
       'eps_vol':'dynamic','press_elem':'dynamic','press_gll':'dynamic'}

sup = {'Mass':'node','Dens':'node','Dom':'node','Elements':'element',
       'Jac':'node','Kappa':'node','Lamb':'node','Material':'element',
       'Mu':'node','Nodes':'node','Proc':'element',
       'press_gll':'node','displ':'node','veloc':'node','Accel':'node',
       'eps_dev_xx':'element','eps_dev_xy':'element','eps_dev_xz':'element',
       'eps_dev_yy':'element','eps_dev_yz':'element','eps_dev_zz':'element',
       'sig_dev_xx':'element','sig_dev_xy':'element','sig_dev_xz':'element',
       'sig_dev_yy':'element','sig_dev_yz':'element','sig_dev_zz':'element',
       'eps_vol':'element','press_elem':'element'}


def GetNonUniqueIndexes(UniqueArray,Array):
    sorted_keys = np.argsort(UniqueArray)
    indexes = sorted_keys[np.searchsorted(UniqueArray, Array, sorter=sorted_keys)]
    return indexes

class SnapshotsSEM3D(object):
    def __init__(self,**kwargs):
        self.__call__(**kwargs)
        
    def __call__(self,**kwargs):
        self.__dict__.update(**kwargs)
        self.setup()
        
    def setup(self):
        self.snapfile={}
        self.flag={}
        self.dset = {}
        self.dtmp = {}
        self.snapfile['geo'] = glob.glob(osj(self.wkd,'geometry*.h5'))
        self.snapfile['res'] = glob.glob(osj(self.wkd,'Rsem*'))
        self.snapfile['nc']  = len(self.snapfile['geo'])
        if self.end_time == -1: 
            self.end_time = len(self.snapfile['res'])
        self.nt = self.end_time - self.begin_time + 1
        (qc,rc) = divmod(self.snapfile['nc'],self.size)

        if self.rank<rc:
            self.snapfile['np'] = [self.rank*(qc+1)+q for q in range(qc+1)]
        else:
            self.snapfile['np'] = [rc*(qc+1)+(self.rank-rc)*qc+q for q in range(qc)]

        print("Rank {:d} - file range {}".format(self.rank,self.snapfile['np']))

        self.flag['static']  = []
        self.flag['dynamic'] = []

        for v in self.var:
            if 'static' in typ[v] and v not in self.flag['static']:
                if self.flag['static']:
                    self.flag['static'].append(v)
                else:
                    self.flag['static'] = [v]
            if 'dynamic' in typ[v] and v not in self.flag['dynamic']:
                if self.flag['dynamic']:
                    self.flag['dynamic'].append(v)
                else:
                    self.flag['dynamic'] = [v]
            self.dset[v] = np.array([])

    def NodeCoordinates2Hash(self,NodeCoords):
        return np.array([hashlib.md5(i.tobytes()).digest() for i in NodeCoords], dtype="S16")
    
    def ParseSEM3DSnapshots(self):
        # 1. Geometry and indexing (keeps your diagnostic print)
        self.GlobalReNumbering()
        
        print("\n" + "="*30)
        print(f"RANK {self.rank} DIAGNOSTIC")
        eg = self.dset['ElementsGlobal']
        print(f"ElementsGlobal Shape: {eg.shape}") # (41236, 8)
        print(f"First element nodes:  {eg[0]}")     
        print(f"Max Node Index:       {eg.max()}")   
        print("="*30 + "\n")
        
        # 2. Static data (remains the same)
        for g in self.snapfile['np']:
            with hf.File(osj(self.wkd,'geometry{:>04d}.h5'.format(g)),'r') as h5f:
                for v in self.flag['static']:
                    if self.dset[v].size == 0:
                        self.dset[v] = h5f[v][...]
                    else:
                        self.dset[v] = np.append(self.dset[v], h5f[v][...], axis=0)
                    
        for v in self.flag['static']:
            if sup[v] == "node":
                self.dset[v] = self.dset[v][self.LocalElementConnectivityOriginal]
                self.dset[v] = self.dset[v][self.LocalNodeUniqueHashIndex]
                self.dset[v] = self.dset[v][self.Local2UniqueLocalIndexOnRank]
        
        # 3. Dynamic data (Snapshots) - RESHAPE REMOVED
        for v in self.flag['dynamic']:
            time_series_data = []
            for t in range(self.begin_time, self.end_time + 1):
                rank_data = []
                for g in self.snapfile['np']:
                    file_path = osj(self.wkd, f'Rsem{t:04d}/sem_field.{g:04d}.h5')
                    try:
                        with hf.File(file_path, 'r') as h5f:
                            rank_data.append(h5f[v][...])
                    except OSError:
                        continue
                
                if rank_data:
                    dtmp = np.concatenate(rank_data, axis=0)
                    time_series_data.append(dtmp)

            if time_series_data:
                # Stack along the last axis to get (2639104, 1, nt)
                processed_data = np.stack(time_series_data, axis=-1)
                
                # STORE FLAT: No reshape to (41236, 64, nt)
                self.dset[v] = processed_data
                
                print(f"Rank {self.rank}: Variable {v} stored as FLAT array {self.dset[v].shape}")
                
    def GlobalReNumbering(self):
        
        LocalNodeCoordinates = None
        LocalElementConnectivity = None
        NodeCount = 0
        self.ElementCount = 0
        # Loop over geometry.XXXX.h5 files (static data) on process
        # Might be more than one file per process!
        for g in self.snapfile['np']:
            with hf.File(osj(self.wkd,'geometry{:>04d}.h5'.format(g)),'r') as h5f:
                # Local node coordinates truncated at 6 decimals
                OnFileNodeCoordinates = h5f["Nodes"][...].astype(np.float64).round(decimals=6)
                if LocalNodeCoordinates is None:
                    LocalNodeCoordinates = OnFileNodeCoordinates
                else:
                    LocalNodeCoordinates = np.append(LocalNodeCoordinates,
                                                     OnFileNodeCoordinates,
                                                     axis=0)
                
                # Element connectivity on geometry file
                OnFileElementConnectivity = h5f["Elements"][...].astype(np.int64)-1+NodeCount
                
                if LocalElementConnectivity is None:
                    LocalElementConnectivity = OnFileElementConnectivity
                else:
                    LocalElementConnectivity = np.append(LocalElementConnectivity,
                                                         OnFileElementConnectivity,
                                                         axis=0)
                NodeCount += OnFileNodeCoordinates.shape[0]
                self.ElementCount += OnFileElementConnectivity.shape[0]

        num_elements = LocalElementConnectivity.shape[0]
        cells = []
        for conn in LocalElementConnectivity:
            cells.append(8)
            cells.extend(conn)
        cell_types = np.full(num_elements, 12, dtype=np.uint8)
        cells = np.array(cells,dtype=np.int64)
        hex_mesh = pv.UnstructuredGrid(cells,cell_types, LocalNodeCoordinates)
        hex_mesh.save(f"multi_hexahedral_mesh_{self.rank}.vtk")
        
        LocalNodeHash = self.NodeCoordinates2Hash(LocalNodeCoordinates)

        LocalNodeUniqueHash, self.LocalNodeUniqueHashIndex, LocalNodeUniqueHashInverse = np.unique(LocalNodeHash[LocalElementConnectivity.flatten()],
                                                                                                   return_index=True,
                                                                                                   return_inverse=True,
                                                                                                   axis=0)
        self.LocalElementConnectivityOriginal = LocalElementConnectivity.flatten().copy()
        LocalNodeCoordinates = LocalNodeCoordinates[LocalElementConnectivity.flatten(),:][self.LocalNodeUniqueHashIndex,:]
        self.LocalNodeCount = LocalNodeUniqueHash.size
        LocalElementConnectivity = LocalNodeUniqueHashInverse.reshape(-1,8)
        
        
        GlobalNodeHash = self.comm.allgather(LocalNodeUniqueHash)
        RankPerGlobalNode = np.concatenate([r*np.ones((GlobalNodeHash[r].size,)) for r in range(self.size)],
                                           axis=0).astype(np.int64)

        GlobalNodeHash, GlobalUniqueIndex = np.unique(np.concatenate(GlobalNodeHash),
                                                      axis=0,
                                                      return_index=True)
        self.GlobalNumberofNodes = GlobalNodeHash.size
        RankPerGlobalNode = RankPerGlobalNode[GlobalUniqueIndex]
        OnRankIndexPerGlobalNode = np.argwhere(RankPerGlobalNode==self.rank).flatten()
        
        _, Local2UniqueLocalIndexOnRank, Global2UniqueLocalIndexOnRank = np.intersect1d(LocalNodeUniqueHash,
                                                                                        GlobalNodeHash,
                                                                                        assume_unique=True,
                                                                                        return_indices=True)
        _, index, _  = np.intersect1d(Global2UniqueLocalIndexOnRank,
                                     OnRankIndexPerGlobalNode,
                                     assume_unique=True,
                                     return_indices=True)
  
        self.dset["ElementsGlobal"] = Global2UniqueLocalIndexOnRank[LocalElementConnectivity]
        self.dset["NodesGlobal"] = LocalNodeCoordinates[Local2UniqueLocalIndexOnRank[index]]
        self.Local2UniqueLocalIndexOnRank = Local2UniqueLocalIndexOnRank[index]
        self.Global2UniqueLocalIndexOnRank = Global2UniqueLocalIndexOnRank[index]
        self.GlobalNodeCount = self.dset["NodesGlobal"].shape[0]

    
    def compute_misfit_gradients(self, snp_adj, dt):
        """
        Computes the misfit gradients for Lambda and Mu.
        Optimized for 1D flat arrays where strains are Element-wise 
        and the Jacobian is Nodal.
        """
        # 1. Setup dimensions
        nb_elements = self.dset['ElementsGlobal'].shape[0] # 2639104
        
        # 2. Extract Element-wise strains (Shape: 2639104, nt)
        ev = self.dset['eps_vol']
        ev_adj = snp_adj.dset['eps_vol']
        
        # 3. Compute Element-averaged Jacobian
        # Jac is Nodal (2701125,). We get the Jac for the 8 corner nodes of each element,
        # shape becomes (2639104, 8), then we average along axis 1 -> (2639104,)
        detJ_elem = np.mean(self.dset['Jac'][self.dset['ElementsGlobal']], axis=1)
        
        # 4. Volumetric Term (Element-wise multiplication)
        vol_term = ev * ev_adj
        
        # 5. Deviatoric Term Summation
        e_ij_names = ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']
        dev_term = np.zeros_like(vol_term)
        
        for c in e_ij_names:
            factor = 2.0 if c in ['xy', 'yz', 'xz'] else 1.0
            dev_term += factor * (self.dset[f'eps_dev_{c}'] * snp_adj.dset[f'eps_dev_{c}'])

        # 6. Time Integration (Sum over the time dimension, axis=1)
        # Resulting shape is exactly (2639104,) -> One gradient value per element
        sum_time_lam = np.sum(vol_term, axis=1) * dt
        sum_time_mu  = np.sum(2.0 * vol_term + dev_term, axis=1) * dt
        
        # 7. Final Gradient assignment mapped with the element volume (detJ)
        g_mis_lambda = -sum_time_lam * detJ_elem
        g_mis_mu     = -sum_time_mu * detJ_elem
        
        return g_mis_lambda, g_mis_mu
    
    def compute_local_contribution_rhs(self, snp_adj, dt, R_lam=1.0, R_mu=1.0):
        """
        Computes the nodal RHS by assembling element misfit gradients.
        """
        # 1. Get the scalar gradient for each element (Arrays of size 2639104)
        g_mis_lam, g_mis_mu = self.compute_misfit_gradients(snp_adj, dt)

        # 2. Initialize global nodal accumulators (Arrays of size 2701125)
        local_sum_lam = np.zeros(self.GlobalNumberofNodes)
        local_sum_mu  = np.zeros(self.GlobalNumberofNodes)

        # 3. FAST VECTORIZED ASSEMBLY
        # This replaces the slow 2.6-million iteration for-loop.
        # It adds the element gradient to all 8 of its corner nodes instantly.
        elements_global_map = self.dset["ElementsGlobal"]
        
        np.add.at(local_sum_lam, elements_global_map.flatten(), np.repeat(g_mis_lam, 8))
        np.add.at(local_sum_mu,  elements_global_map.flatten(), np.repeat(g_mis_mu, 8))

        # 4. Regularization mapping
        rank_indices = self.Global2UniqueLocalIndexOnRank
        
        local_sum_lam[rank_indices] += R_lam * (self.dset['Mass'] * self.dset['Lamb'])
        local_sum_mu[rank_indices]  += R_mu  * (self.dset['Mass'] * self.dset['Mu'])

        return local_sum_lam, local_sum_mu
    
    def solve_gradients_parallel(self, snp_adj, dt, R_lam=1.0, R_mu=1.0):
        """
        Parallelized resolution: Sums boundary nodes and distributes the linear 
        system so each process solves only its unique portion.
        """
        # STEP 1: Compute Local Contributions (Cubes owned by this rank)
        # These are vectors of size GlobalNumberofNodes, mostly zeros.
        loc_rhs_lam, loc_rhs_mu = self.compute_local_contribution_rhs(snp_adj,dt, R_lam, R_mu)
        # Use the pre-computed values from the file directly:
        loc_M = np.zeros(self.GlobalNumberofNodes)
        loc_M[self.Global2UniqueLocalIndexOnRank] = self.dset['Mass']

        # STEP 2: SUM AND DISTRIBUTE (The True Parallel Step)
        num_nodes = self.GlobalNumberofNodes
        
        # Determine how many nodes each rank will handle. 
        # We handle cases where num_nodes is not perfectly divisible by size.
        counts = [num_nodes // self.size + (1 if r < num_nodes % self.size else 0) for r in range(self.size)]
        my_count = counts[self.rank]
        
        # Initialize small buffers for this rank's unique piece
        chunk_rhs_lam = np.zeros(my_count)
        chunk_rhs_mu = np.zeros(my_count)
        chunk_M = np.zeros(my_count)

        print(f"Rank {self.rank} - local contribution computed. Preparing for Reduce_scatter with counts: {counts}")
        
        # Reduce_scatter sums the global data and gives a unique piece to each process.
        # This resolves the shared boundaries and splits the memory at the same time.
        self.comm.Reduce_scatter(loc_rhs_lam, chunk_rhs_lam, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_rhs_mu, chunk_rhs_mu, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_M, chunk_M, recvcounts=counts, op=MPI.SUM)

        # STEP 3: PARALLEL RESOLUTION (Division)
        # Now every process divides ONLY its assigned nodes.
        # Calculate the offset to pull the correct segment of Density (Rho)
        offset = sum(counts[:self.rank])
        rho_chunk = self.dset['Dens'][offset : offset + my_count]
        print(f"Rank {self.rank} - gathered local density chunk. Processing...")
        mask = chunk_M > 0
        g_lam_chunk = np.zeros(my_count)
        g_mu_chunk = np.zeros(my_count)

        # Resolution: g = (rho * RHS) / M
        g_lam_chunk[mask] = (rho_chunk[mask] * chunk_rhs_lam[mask]) / chunk_M[mask]
        g_mu_chunk[mask]  = (rho_chunk[mask] * chunk_rhs_mu[mask]) / chunk_M[mask]

        print(f"Rank {self.rank} - local gradients computed. Gathering results...")
        # STEP 4: GATHER RESULTS (Optional - for saving/output)
        # If you need the full domain on Rank 0 for VTK saving:
        
    # ========================================================================
        # if self.rank == 0:
        #     g_lam_final = np.zeros(num_nodes)
        #     g_mu_final = np.zeros(num_nodes)
        # else:
        #     g_lam_final = None
        #     g_mu_final = None

        # self.comm.Gatherv(g_lam_chunk, [g_lam_final, counts, sum(counts[:self.rank]), MPI.DOUBLE], root=0)
        # self.comm.Gatherv(g_mu_chunk, [g_mu_final, counts, sum(counts[:self.rank]), MPI.DOUBLE], root=0)

        # return g_lam_final, g_mu_final
        return g_lam_chunk, g_mu_chunk, counts
    # ========================================================================
        
    
def ParseCL():
    """
        Parse command line flags
    """
    parser = argparse.ArgumentParser(prefix_chars='@')
    parser.add_argument('@@wkd',type=str,default='./res',help="Path to res directory")
    parser.add_argument('@@var',type=str,nargs='+',default=['Mass','Jac','Mu','Lamb','Nodes',
                                                            'Elements', 'Dens',
                                                            'Dom','displ',
                                                            'eps_vol','eps_dev_xx',
                                                            'eps_dev_yy','eps_dev_zz',
                                                            'eps_dev_xy','eps_dev_yz',
                                                            'eps_dev_xz'],
                        help="Select snapshot")
    parser.add_argument('@@begin_time','@b', type=int, default=1, help="Initial time step to parse")
    parser.add_argument('@@end_time','@e', type=int, default=-1, help="Final time step to parse")
    opt = parser.parse_args().__dict__
    
    opt_adj = opt.copy()
    opt_adj['wkd'] = './sem3d_config_files_adj/res/'
    opt_adj['var'] = [
        'eps_vol','eps_dev_xx',
        'eps_dev_yy','eps_dev_zz',
        'eps_dev_xy','eps_dev_yz',
        'eps_dev_xz'
    ]
    return opt, opt_adj

def GetSnapshots(comm,size,rank):

    # Parse Command Line
    opt, opt_adj = ParseCL()
    opt["comm"] = comm
    opt["size"] = size
    opt["rank"] = rank
    
    opt_adj["comm"] = comm
    opt_adj["size"] = size
    opt_adj["rank"] = rank
    
    # Generate snapshot structure
    snp = SnapshotsSEM3D(**opt)
    snp_adj = SnapshotsSEM3D(**opt_adj)
    
    # Parse result snapshots 
    snp.ParseSEM3DSnapshots()
    print(f"Elements shape: {snp.dset['eps_vol'].shape}")
    snp_adj.ParseSEM3DSnapshots()

    print(f"Rank {rank} - snapshots parsed. Starting gradient computation...")
    return snp, snp_adj

def main():
    """
    Start parallel process
    """
    MPI.Init()
    comm = MPI.COMM_WORLD               # Get communicator
    size = MPI.COMM_WORLD.Get_size()    # Get size of communicator
    rank = MPI.COMM_WORLD.Get_rank()    # Get the current rank
    
    snp = GetSnapshots(comm,size,rank)

    # Gather global elements
    NumberofElements = np.array(comm.allgather(snp.ElementCount*8))
    
    if rank == 0:
        recvbuf = np.empty(sum(NumberofElements),dtype=np.int64)
    else:
        recvbuf = None
    
    comm.Gatherv(sendbuf=snp.dset["ElementsGlobal"].flatten(), 
                    recvbuf=[recvbuf, NumberofElements,
                            [sum(NumberofElements[:i]) for i in range(len(NumberofElements))],
                            MPI.LONG_LONG],
                    root=0)
    
    if rank == 0:
        ElementsGlob = recvbuf.astype(np.int64).reshape((-1,8))
    else:
        ElementsGlob = None
        
    
    
    # Gather global nodes
    NumberofNodeCoordinates = np.array(comm.allgather(snp.GlobalNodeCount*3))

    if rank == 0:
        recvbuf = np.empty(sum(NumberofNodeCoordinates),dtype=np.float64)
    else:
        recvbuf = None
    comm.Gatherv(sendbuf=snp.dset["NodesGlobal"].astype(np.float64).flatten(), 
                 recvbuf=[recvbuf, NumberofNodeCoordinates,
                          [sum(NumberofNodeCoordinates[:i]) for i in range(len(NumberofNodeCoordinates))],
                          MPI.DOUBLE],
                 root=0)

    if rank == 0:
        NodesTemp = recvbuf.astype(np.float64).reshape((-1,3))
    else:
        NodesTemp = None
        
    # Gather node global inindexes
    NumberofNodes = np.array(comm.allgather(snp.GlobalNodeCount))
    if rank == 0:
        recvbuf = np.empty(sum(NumberofNodes),dtype=np.float64)
    else:
        recvbuf = None
    comm.Gatherv(sendbuf=snp.Global2UniqueLocalIndexOnRank.astype(np.float64), 
                 recvbuf=[recvbuf, NumberofNodes,
                          [sum(NumberofNodes[:i]) for i in range(len(NumberofNodes))],
                          MPI.DOUBLE],
                 root=0)


    if rank == 0:
        NodesIndex = recvbuf.astype(np.int64)
        NodesGlobal = np.empty_like(NodesTemp)
        NodesGlobal[NodesIndex] = NodesTemp
    else:
        NodesIndex = None
    
    selected_var = snp.var[0]
    NumberofVectorComponents = NumberofNodeCoordinates*snp.nt
    if rank == 0:
        recvbuf = np.empty(sum(NumberofVectorComponents),dtype=np.float64)
    else:
        recvbuf = None
    comm.Gatherv(sendbuf=snp.dset[selected_var].astype(np.float64).flatten(), 
                 recvbuf=[recvbuf, NumberofVectorComponents,
                          [sum(NumberofVectorComponents[:i]) for i in range(len(NumberofVectorComponents))],
                          MPI.DOUBLE],
                 root=0)

    if rank == 0:
        DisplTemp = recvbuf.astype(np.float64).reshape((-1,3,snp.nt))
        DisplGlobal = np.empty_like(DisplTemp)
        DisplGlobal[NodesIndex] = DisplTemp
    else:
        DisplGlobal = None
        
    
    if rank == 0:
        import pyvista as pv
        # Convert to VTK-compatible format
        num_elements = ElementsGlob.shape[0]
        cells = []
        for conn in ElementsGlob:
            cells.append(8)  # First value: number of nodes per hexahedron
            cells.extend(conn)  # Add node indices
        cells = np.array(cells, dtype=np.int64)  # Convert to NumPy array

        # Cell types (all VTK_HEXAHEDRON)
        cell_types = np.full(num_elements, 12, dtype=np.uint8)
        # Create the Unstructured Grid
        hex_mesh = pv.UnstructuredGrid(cells,cell_types, NodesGlobal)
        # hex_mesh.save("multi_hexahedral_mesh.vtk")
        # hex_mesh["Time"] = np.arange(snp.begin_time, snp.end_time+1)
        for j in range(DisplGlobal.shape[-1]):
            t = snp.begin_time + j
            hex_mesh[selected_var] = DisplGlobal[:,:,j].reshape((-1,3))
            hex_mesh.save(f"multi_hexahedral_mesh_{t}.vtu")
    
    # if rank == 0:
    # # Let's say you want to see the points for the first 5 elements
    #     for element_id in range(5):
    #         # Get the IDs of the GLL points for this element
    #         point_indices = ElementsGlob[element_id]
            
    #         print(f"Element {element_id} is made of GLL Points: {point_indices}")
            
    #         # To get the actual (X,Y,Z) positions of these points:
    #         positions = NodesGlobal[point_indices]
    #         print(f"Coordinates:\n{positions}\n")
    MPI.Finalize()
    
import os
import numpy as np
from scipy.spatial import cKDTree
from mpi4py import MPI

import os
import numpy as np
from scipy.spatial import cKDTree
from mpi4py import MPI

def compute_gradients_main(x_bounds = [-1300, 1300], y_bounds = [-1300, 1300], z_bounds = [-1540, 0], steps = [200, 200, 20], cache_dir="./", wrt = True):
    """
    Computes gradients and maps them to a material mesh with step-by-step logging.
    
    Returns:
        - 4 Local compact vectors: grad_lam, grad_mu, lam, mu
        - 3 Global sparse vectors: x_gl, y_gl, z_gl
    """
    if not MPI.Is_initialized():
        MPI.Init()
    
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # 1. INITIALIZATION & PHYSICAL SOLVE
    if rank == 0: print(f"--- Step 1: Initializing snapshots on {size} ranks ---")
    
    # GetSnapshots handles CLI parsing and snapshot loading.
    snp, snp_adj = GetSnapshots(comm, size, rank) 
    
    if rank == 0: print("--- Step 2: Solving physical gradients on GLL mesh ---")
    # solve_gradients_parallel computes the GLL-based misfit gradients.
    g_lam_chunk, g_mu_chunk, counts = snp.solve_gradients_parallel(snp_adj, dt=0.5)
    
    phys_offsets = np.cumsum([0] + counts) 
    
    # Define Material Mesh Grid dimensions
    x_range = np.arange(x_bounds[0], x_bounds[1] + steps[0], steps[0])
    y_range = np.arange(y_bounds[0], y_bounds[1] + steps[1], steps[1])
    z_range = np.arange(z_bounds[0], z_bounds[1] + steps[2], steps[2])
    total_mat_nodes = len(x_range) * len(y_range) * len(z_range)
    
    cache_file = os.path.join(cache_dir, f'mesh_mapping_rank_{rank}.npz')

    # =========================================================================
    # 2. MAPPING LOGIC (CACHE OR COMPUTE)
    # =========================================================================
    if os.path.exists(cache_file):
        if rank == 0: print(f"--- Step 3: Loading mapping from cache: {cache_dir} ---")
        data = np.load(cache_file)
        mat_nodes_local = data['coords']
        mat_phys_idx_local = data['idx']
        mat_global_indices = data['global_mask_idx']
    else:
        if rank == 0: print("--- Step 3: No cache found. Starting Global Mapping process ---")
        
        # Gather GLL physical coordinates for the KD-Tree.
        local_nodes = snp.dset['NodesGlobal'] 
        if rank == 0:
            print(f"Rank 0: Gathering coordinates for {snp.GlobalNumberofNodes} physical nodes...")
            all_nodes_phys = np.empty((snp.GlobalNumberofNodes, 3), dtype=np.float64)
        else:
            all_nodes_phys = None
        
        counts_3d = [c * 3 for c in counts]
        displs_3d = [d * 3 for d in np.cumsum([0] + counts[:-1])]
        comm.Gatherv(sendbuf=local_nodes, recvbuf=[all_nodes_phys, counts_3d, displs_3d, MPI.DOUBLE], root=0)

        if rank == 0:
            print("Rank 0: Building Global KD-Tree...")
            tree = cKDTree(all_nodes_phys)
            
            grid_x, grid_y, grid_z = np.meshgrid(x_range, y_range, z_range, indexing='ij')
            mat_coords_global = np.stack([grid_x.ravel(), grid_y.ravel(), grid_z.ravel()], axis=1)
            original_indices = np.arange(total_mat_nodes)
            
            print(f"Rank 0: Querying tree for {total_mat_nodes} material points...")
            _, nearest_phys_indices = tree.query(mat_coords_global, k=1)
            
            print("Rank 0: Determining point ownership and bundling data...")
            target_ranks = np.searchsorted(phys_offsets, nearest_phys_indices, side='right') - 1
            
            send_mat_coords = [mat_coords_global[target_ranks == r] for r in range(size)]
            send_phys_indices = [nearest_phys_indices[target_ranks == r] for r in range(size)]
            send_global_mask = [original_indices[target_ranks == r] for r in range(size)]
            mat_counts = [len(c) for c in send_mat_coords]
            print("Rank 0: Bundling complete. Starting MPI distribution...")
        else:
            send_mat_coords = send_phys_indices = send_global_mask = mat_counts = None

        # Scatter information and distribute data bundles
        local_mat_count = comm.scatter(mat_counts, root=0)
        mat_nodes_local = np.empty((local_mat_count, 3), dtype=np.float64)
        mat_phys_idx_local = np.empty(local_mat_count, dtype=np.int64)
        mat_global_indices = np.empty(local_mat_count, dtype=np.int64)

        if rank == 0:
            for r in range(1, size):
                comm.Send(send_mat_coords[r], dest=r, tag=901)
                comm.Send(send_phys_indices[r], dest=r, tag=902)
                comm.Send(send_global_mask[r], dest=r, tag=903)
            mat_nodes_local = send_mat_coords[0]
            mat_phys_idx_local = send_phys_indices[0]
            mat_global_indices = send_global_mask[0]
        else:
            comm.Recv(mat_nodes_local, source=0, tag=901)
            comm.Recv(mat_phys_idx_local, source=0, tag=902)
            comm.Recv(mat_global_indices, source=0, tag=903)

        print(f"Rank {rank}: Mapping received and saved to local cache.")
        np.savez(cache_file, coords=mat_nodes_local, idx=mat_phys_idx_local, global_mask_idx=mat_global_indices)

    # =========================================================================
    # 3. VECTOR EXTRACTION & ASSEMBLY
    # =========================================================================
    if rank == 0: print("--- Step 4: Extracting local data and assembling coordinate vectors ---")
    
    # Mapping physical global IDs back to the local rank-specific chunk
    local_idx_mapped = mat_phys_idx_local - phys_offsets[rank]
    
    # COMPACT LOCAL VECTORS (Material values for local nodes)
    grad_lam_local = g_lam_chunk[local_idx_mapped]
    grad_mu_local  = g_mu_chunk[local_idx_mapped]
    # Extract Lamb and Mu properties from the dataset.
    lam_val_local  = snp.dset['Lamb'][local_idx_mapped] 
    mu_val_local   = snp.dset['Mu'][local_idx_mapped]   

    if wrt:
        # GLOBAL SPARSE VECTORS (Coordinates)
        x_gl = np.zeros(total_mat_nodes, dtype=np.float64)
        y_gl = np.zeros(total_mat_nodes, dtype=np.float64)
        z_gl = np.zeros(total_mat_nodes, dtype=np.float64)

        # Placing local coordinates into their global spatial index slots
        x_gl[mat_global_indices] = mat_nodes_local[:, 0]
        y_gl[mat_global_indices] = mat_nodes_local[:, 1]
        z_gl[mat_global_indices] = mat_nodes_local[:, 2]

        if rank == 0: 
            print("--- Final Step: Computation and assembly complete. Returning vectors. ---")

        return(grad_lam_local, grad_mu_local, 
                lam_val_local, mu_val_local,
                x_gl, y_gl, z_gl)    
    else:
        if rank == 0: print("--- Final Step: Computation and assembly complete. Returning local vectors only. ---")
        return (grad_lam_local, grad_mu_local, lam_val_local, mu_val_local, None, None, None)

if __name__=="__main__":
    compute_gradients_main()
    # main()