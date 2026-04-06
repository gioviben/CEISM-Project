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
        
        self.GlobalReNumbering()
        
        # if self.flag['static']:
        for g in self.snapfile['np']:
            with hf.File(osj(self.wkd,'geometry{:>04d}.h5'.format(g)),'r') as h5f:
                for v in self.flag['static']:
                    if self.dset[v].size == 0:
                        self.dset[v]=h5f[v][...]
                    else:
                        self.dset[v]=np.append(self.dset[v],h5f[v][...],axis=0)
                    
        for v in self.flag['static']:
            if sup[v]=="node":
                self.dset[v] = self.dset[v][self.LocalElementConnectivityOriginal]
                self.dset[v] = self.dset[v][self.LocalNodeUniqueHashIndex]
                self.dset[v] = self.dset[v][self.Local2UniqueLocalIndexOnRank]
        
        
        for v in self.flag['dynamic']:
            for g in self.snapfile['np']:
                with hf.File(osj(self.wkd,'Rsem{:>04d}/sem_field.{:>04d}.h5'.format(self.begin_time+1,g)),'r') as h5f:
                    if self.dset[v].size == 0:
                        self.dset[v]=h5f[v][...]
                    else:
                        self.dset[v]=np.append(self.dset[v],h5f[v][...],axis=0)
            
            if len(self.dset[v].shape)==2:
                self.dset[v]=self.dset[v].reshape((*self.dset[v].shape,1))
            elif len(self.dset[v].shape)==1:
                self.dset[v]=self.dset[v].reshape((*self.dset[v].shape,1,1))
            if sup[v]=="node":
                self.dset[v] = self.dset[v][self.LocalElementConnectivityOriginal]
                self.dset[v] = self.dset[v][self.LocalNodeUniqueHashIndex]
                self.dset[v] = self.dset[v][self.Local2UniqueLocalIndexOnRank]
            shp = self.dset[v].shape
            
            for t in range(self.begin_time+1, self.end_time+1):
                dtmp = np.array([])
                for g in self.snapfile['np']:
                    with hf.File(osj(self.wkd,'Rsem{:>04d}/sem_field.{:>04d}.h5'.format(t,g)),'r') as h5f:
                        if dtmp.size == 0:
                            dtmp=h5f[v][...]
                        else:
                            dtmp=np.append(dtmp,h5f[v][...],axis=0)
                if sup[v]=="node":
                    dtmp = dtmp[self.LocalElementConnectivityOriginal]
                    dtmp = dtmp[self.LocalNodeUniqueHashIndex]
                    dtmp = dtmp[self.Local2UniqueLocalIndexOnRank]
                self.dset[v]=np.append(self.dset[v], dtmp.reshape(*shp),axis=2)    
    
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
                OnFileElementConnectivity = h5f["Elements"][...].astype(np.int64)+NodeCount
                
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

    def compute_element_shapes(self):
    #     """
    #     Creates a mapping for each hexahedron that converts reference coordinates
    #     (-1 to 1) into physical 3D coordinates (X, Y, Z).
    #     """
    #     # Get local data from the snapshot object
    #     elements = self.dset['Elements'] 
    #     coords = self.dset['Nodes'] 
        
    #     # Standard reference coordinates for the 8 corners of a cube
    #     ref_corners = np.array([
    #         [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1],
    #         [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1]
    #     ])

    #     element_mappers = {}

    #     for e_idx, node_indices in tqdm(enumerate(elements), total=len(elements), desc="Computing element shapes"):
    #         # STEP 1: Get the 8 physical [X, Y, Z] corners for this specific hex
    #         physical_corners = coords[node_indices] 
            
    #         # STEP 2: Create a function that "links" physical corners to the math
    #         def make_mapper(current_corners):
                
    #             def interpolate(xi, eta, zeta):
    #                 # Calculate the 8 weights (N_i) based on the reference space
    #                 # Each weight corresponds to one of the 8 corners
    #                 weights = 0.125 * (1 + ref_corners[:,0]*xi) * \
    #                                   (1 + ref_corners[:,1]*eta) * \
    #                                   (1 + ref_corners[:,2]*zeta)
                    
    #                 # STEP 3: USE THE CORNERS! 
    #                 # Multiply each weight by its corresponding physical corner coordinate
    #                 # physical_x = sum(N_i * corner_x_i), etc.
    #                 world_pos = np.dot(weights, current_corners)
                    
    #                 return {
    #                     'weights': weights,      # The influence of each GLL point
    #                     'world_pos': world_pos   # The actual X, Y, Z in your model
    #                 }
                
    #             return interpolate

    #         # Store the mapper function for this element
    #         element_mappers[e_idx] = make_mapper(physical_corners)
            
    #     return element_mappers
        pass

    def compute_mass_matrix(self):
    #     """
    #     Calcule la matrice de masse en utilisant directement le Jacobien (Jac) 
    #     fourni dans le fichier de snapshots, en intégrant sur les points GLL.
    #     """
    #     elements = self.dset['Elements']
    #     # Jac contient déjà le déterminant |J| pour chaque nœud GLL
    #     global_jac = self.dset['Jac'] 
        
    #     # Dans SEM, pour ngll=2 (trilinéaire), les poids d'intégration 
    #     # de Gauss-Lobatto sont simplement 1.0 à chaque sommet.
    #     # Pour un cube de référence [-1, 1], le poids total est 1.0 * 1.0 * 1.0 = 1.0
    #     gll_weight = 1.0 

    #     self.element_mass_matrices = {}

    #     for e_idx, node_indices in tqdm(enumerate(elements), total=len(elements), desc="Computing mass matrices (using Jac)"):
    #         # Initialisation de la matrice 8x8 pour l'élément hexaédrique
    #         Me = np.zeros((8, 8))
            
    #         # On boucle sur les 8 nœuds GLL de l'élément (cas ngll=2)
    #         for local_i in range(8):
    #             global_node_idx = node_indices[local_i]
                
    #             # Récupération directe du déterminant du Jacobien pré-calculé
    #             # Cela remplace tout le calcul lourd de np.linalg.det(J)
    #             detJ = global_jac[global_node_idx]
                
    #             # En intégration Gauss-Lobatto, la matrice de masse est diagonale
    #             # Me_ii = Integral( N_i * N_i * |J| dV )
    #             # Comme N_i = 1 au nœud i et 0 aux autres nœuds GLL :
    #             Me[local_i, local_i] = detJ * gll_weight
                
    #         self.element_mass_matrices[e_idx] = Me
        pass
    
    def compute_regularization_gradients(self):
    #     """
    #     Computes g_reg = Integral(N * N.T) * material_vector
    #     Returns local dictionaries for lambda and mu regularization gradients.
    #     """
    #     # Ensure mass matrices are computed first
    #     if not hasattr(self, 'element_mass_matrices'):
    #         self.compute_mass_matrix()
            
    #     g_reg_lambda = {}
    #     g_reg_mu = {}
        
    #     elements = self.dset['Elements']
        
    #     for e_idx, node_indices in enumerate(elements):
    #         # Me is the 8x8 integral of N*N.T for this element
    #         Me = self.element_mass_matrices[e_idx]
            
    #         # Extract local 8-node material property vectors
    #         lambda_e = self.dset['Lamb'][node_indices]
    #         mu_e = self.dset['Mu'][node_indices]
            
    #         # Matrix-vector product for regularization
    #         g_reg_lambda[e_idx] = np.dot(Me, lambda_e)
    #         g_reg_mu[e_idx] = np.dot(Me, mu_e)
            
    #     return g_reg_lambda, g_reg_mu
        pass
    
    def compute_misfit_gradients(self, snp_adj, dt):
        """
        Calcule les gradients de misfit de manière optimisée.
        Utilise l'intégration de Gauss-Lobatto (points GLL) et le Jacobien (Jac) pré-calculé.
        """
        elements = self.dset['Elements']
        nt = self.nt 
        global_jac = self.dset['Jac'] #
        
        # Initialisation des dictionnaires de gradients
        # Pour ngll=2, chaque élément a 8 points
        g_mis_lambda = {e: np.zeros(8) for e in range(len(elements))}
        g_mis_mu = {e: np.zeros(8) for e in range(len(elements))}

        # En Gauss-Lobatto (ngll=2), le poids est 1.0 par point
        gll_weight = 1.0 

        for e_idx, nodes in tqdm(enumerate(elements), total=len(elements), desc="Misfit gradients"):
            
            # On pré-extrait les données temporelles pour l'élément (vectorisation temporelle)
            # ev shape: (8, nt)
            ev = self.dset['eps_vol'][e_idx, :, :]
            ev_adj = snp_adj.dset['eps_vol'][e_idx, :, :]
            
            # Composantes déviatoriques
            e_ij_names = ['xx','yy','zz','xy','yz','xz']
            e_ij = {c: self.dset[f'eps_dev_{c}'][e_idx, :, :] for c in e_ij_names}
            e_ij_adj = {c: snp_adj.dset[f'eps_dev_{c}'][e_idx, :, :] for c in e_ij_names}

            # Boucle sur les 8 points GLL de l'élément
            for local_i in range(8):
                global_node_idx = nodes[local_i]
                detJ = global_jac[global_node_idx] #
                
                # Calcul du produit scalaire des déformations sur toute la durée T
                # On multiplie point par point sur l'axe du temps (nt)
                vol_term = ev[local_i, :] * ev_adj[local_i, :]
                
                dev_term = (e_ij['xx'][local_i, :] * e_ij_adj['xx'][local_i, :] +
                            e_ij['yy'][local_i, :] * e_ij_adj['yy'][local_i, :] +
                            e_ij['zz'][local_i, :] * e_ij_adj['zz'][local_i, :] +
                            2 * (e_ij['xy'][local_i, :] * e_ij_adj['xy'][local_i, :] +
                                e_ij['yz'][local_i, :] * e_ij_adj['yz'][local_i, :] +
                                e_ij['xz'][local_i, :] * e_ij_adj['xz'][local_i, :]))

                # Sommation temporelle (Sum_t ... * dt)
                # On multiplie par detJ car c'est le volume local associé au point i
                sum_time_lam = np.sum(vol_term) * dt
                sum_time_mu  = np.sum(2 * vol_term + dev_term) * dt
                
                # Application du signe négatif de la formule g_mis = -Sum(...)
                # Le poids gll_weight (1.0) est implicite ici.
                g_mis_lambda[e_idx][local_i] = -sum_time_lam * detJ
                g_mis_mu[e_idx][local_i]     = -sum_time_mu * detJ
                
        return g_mis_lambda, g_mis_mu

    def compute_local_contribution_rhs(self, snp_adj, dt, R_lam=1.0, R_mu=1.0):
        """
        Computes the nodal RHS by assembling element misfit gradients and 
        adding nodal regularization using the pre-computed Mass variable.
        """
        # 1. Compute element-level misfit gradients (optimized with Jac/GLL)
        g_mis_lam, g_mis_mu = self.compute_misfit_gradients(snp_adj, dt)

        # 2. Initialize global nodal accumulators for this MPI rank
        local_sum_lam = np.zeros(self.GlobalNumberofNodes)
        local_sum_mu = np.zeros(self.GlobalNumberofNodes)

        # 3. Misfit Assembly: Sum element misfit contributions into global nodes
        elements_global_map = self.dset["ElementsGlobal"]
        for e_idx in range(len(self.dset['Elements'])):
            global_indices = elements_global_map[e_idx]
            local_sum_lam[global_indices] += g_mis_lam[e_idx]
            local_sum_mu[global_indices]  += g_mis_mu[e_idx]

        # 4. Regularization: Add nodal term (g_reg = R * M * m)
        # Using the diagonal Global Mass (Mass) and Material properties (Lamb/Mu)
        # This directly implements the formula: g_total = g_misfit + (R * Mass * property)
        rank_indices = self.Global2UniqueLocalIndexOnRank
        
        local_sum_lam[rank_indices] += R_lam * (self.dset['Mass'] * self.dset['Lamb'])
        local_sum_mu[rank_indices]  += R_mu  * (self.dset['Mass'] * self.dset['Mu'])

        return local_sum_lam, local_sum_mu
    
    def compute_local_contribution_mass_matrix(self):
    #     """
    #     Computes the local contribution to the mass matrix from the element in the current MPI rank by 
    #     assembling 8x8 element matrices.
    #     Returns: A vector of size GlobalNumberofNodes.
    #     """
    #     # Initialize the 'Global Bucket' for the mass
    #     local_mass_vector = np.zeros(self.GlobalNumberofNodes)
        
    #     # Loop over every hexahedron in this MPI rank
    #     for e_idx in range(self.ElementCount):
    #         # Get the 8 diagonal values of the mass matrix for element e_idx
    #         Me_diag = np.diag(self.element_mass_matrices[e_idx])
            
    #         # Get the 'Addresses' (Global IDs) for these 8 nodes
    #         global_indices = self.dset["ElementsGlobal"][e_idx]
            
    #         # Assembly (A): Add the local mass to the global nodal slots
    #         local_mass_vector[global_indices] += Me_diag
        
    #     return local_mass_vector
        pass
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
        
        return g_lam_chunk, g_mu_chunk, mask
    
def ParseCL():
    """
        Parse command line flags
    """
    parser = argparse.ArgumentParser(prefix_chars='@')
    parser.add_argument('@@wkd',type=str,default='./res',help="Path to res directory")
    parser.add_argument('@@var',type=str,nargs='+',default=['Mass','Jac','Mu','Lamb','Nodes',
                                                            'Elements',
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
    opt_adj['wkd'] = '../sem3d_config_files_adj/res/'
    opt_adj['var'] = {
        'eps_vol','eps_dev_xx',
        'eps_dev_yy','eps_dev_zz',
        'eps_dev_xy','eps_dev_yz',
        'eps_dev_xz'
    }
    return opt, opt_adj

def GetSnapshots(comm,size,rank):

    # Parse Command Line
    opt, opt_adj = ParseCL()
    opt["comm"] = comm
    opt["size"] = size
    opt["rank"] = rank
    
    # Generate snapshot structure
    snp = SnapshotsSEM3D(**opt)
    snp_adj = SnapshotsSEM3D(**opt_adj)
    
    # Parse result snapshots 
    snp.ParseSEM3DSnapshots()
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
    
def compute_gradients_main():
    """
    Main execution block to compute gradients in a truly parallel way.
    Optimized to skip redundant mass and shape calculations.
    """
    # 1. Initialize MPI environment
    if not MPI.Is_initialized():
        MPI.Init()
    
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # 2. Load snapshots and geometry (Forward and Adjoint)
    # snp contains properties like 'Mass', 'Jac', 'Lamb', 'Mu'
    snp, snp_adj = GetSnapshots(comm, size, rank)
    
    # 3. Execute the Parallel Resolution
    # We no longer call snp.compute_mass_matrix() or snp.compute_element_shapes()
    # because solve_gradients_parallel now uses pre-computed file data directly.
    g_lam_final, g_mu_final = snp.solve_gradients_parallel(snp_adj, dt=0.5) 

    # 4. Handle the result on Rank 0
    if rank == 0:
        print(f"Parallel inversion complete. Global Node Count: {snp.GlobalNumberofNodes}")
        # Results (g_lam_final, g_mu_final) are ready for storage or VTK export
        return g_lam_final, g_mu_final
    
    else:
        return None, None
    
    
if __name__=="__main__":
    compute_gradients_main()
    # main()