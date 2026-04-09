# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Script read SEM3D snapshots with MPI-based algorithm

Ex.:
    mpirun --np n python3 parse_h5_snapshots.py @@wkd /path/to/sem3d/res @@var veloc
"""

import argparse
import glob
import hashlib
from pathlib import Path
import os
from os.path import join as osj

import h5py as hf
import mpi4py
import numpy as np
import pyvista as pv
from mpi4py import MPI
from scipy.spatial import cKDTree

mpi4py.rc.initialize = False
mpi4py.rc.finalize = False

__author__ = "Filippo Gatti"
__copyright__ = "Copyright 2020, CentraleSupélec (MSSMat UMR CNRS 8579)"
__credits__ = ["Filippo Gatti"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Filippo Gatti"
__email__ = "filippo.gatti@centralesupelec.fr"
__status__ = "Beta"

typ = {
    'Mass': 'static', 'Dens': 'static', 'Dom': 'static', 'Elements': 'static',
    'Jac': 'static', 'Kappa': 'static', 'Lamb': 'static', 'Material': 'static',
    'Mu': 'static', 'Nodes': 'static', 'Proc': 'static',
    'displ': 'dynamic', 'veloc': 'dynamic', 'Accel': 'dynamic',
    'eps_dev_xx': 'dynamic', 'eps_dev_xy': 'dynamic', 'eps_dev_xz': 'dynamic',
    'eps_dev_yy': 'dynamic', 'eps_dev_yz': 'dynamic', 'eps_dev_zz': 'dynamic',
    'sig_dev_xx': 'dynamic', 'sig_dev_xy': 'dynamic', 'sig_dev_xz': 'dynamic',
    'sig_dev_yy': 'dynamic', 'sig_dev_yz': 'dynamic', 'sig_dev_zz': 'dynamic',
    'eps_vol': 'dynamic', 'press_elem': 'dynamic', 'press_gll': 'dynamic'
}

sup = {
    'Mass': 'node', 'Dens': 'node', 'Dom': 'node', 'Elements': 'element',
    'Jac': 'node', 'Kappa': 'node', 'Lamb': 'node', 'Material': 'element',
    'Mu': 'node', 'Nodes': 'node', 'Proc': 'element',
    'press_gll': 'node', 'displ': 'node', 'veloc': 'node', 'Accel': 'node',
    'eps_dev_xx': 'element', 'eps_dev_xy': 'element', 'eps_dev_xz': 'element',
    'eps_dev_yy': 'element', 'eps_dev_yz': 'element', 'eps_dev_zz': 'element',
    'sig_dev_xx': 'element', 'sig_dev_xy': 'element', 'sig_dev_xz': 'element',
    'sig_dev_yy': 'element', 'sig_dev_yz': 'element', 'sig_dev_zz': 'element',
    'eps_vol': 'element', 'press_elem': 'element'
}


def GetNonUniqueIndexes(UniqueArray, Array):
    sorted_keys = np.argsort(UniqueArray)
    indexes = sorted_keys[np.searchsorted(UniqueArray, Array, sorter=sorted_keys)]
    return indexes


class SnapshotsSEM3D(object):
    def __init__(self, **kwargs):
        self.__call__(**kwargs)

    def __call__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.setup()

    def setup(self):
        self.snapfile = {}
        self.flag = {}
        self.dset = {}
        self.dtmp = {}

        self.snapfile['geo'] = glob.glob(osj(self.wkd, 'geometry*.h5'))
        self.snapfile['res'] = glob.glob(osj(self.wkd, 'Rsem*'))
        self.snapfile['nc'] = len(self.snapfile['geo'])

        print(f"[Rank {self.rank}] wkd = {self.wkd}")
        print(f"[Rank {self.rank}] geometry files found = {self.snapfile['nc']}")
        print(f"[Rank {self.rank}] first geometry files = {self.snapfile['geo'][:3]}")
        print(f"[Rank {self.rank}] number of Rsem folders = {len(self.snapfile['res'])}")

        if self.end_time == -1:
            self.end_time = len(self.snapfile['res']) - 1

        self.nt = self.end_time - self.begin_time + 1

        qc, rc = divmod(self.snapfile['nc'], self.size)

        if self.rank < rc:
            self.snapfile['np'] = [self.rank * (qc + 1) + q for q in range(qc + 1)]
        else:
            self.snapfile['np'] = [rc * (qc + 1) + (self.rank - rc) * qc + q for q in range(qc)]

        print(f"Rank {self.rank} - file range {self.snapfile['np']}")

        self.flag['static'] = []
        self.flag['dynamic'] = []

        for v in self.var:
            if 'static' in typ[v] and v not in self.flag['static']:
                self.flag['static'].append(v)
            if 'dynamic' in typ[v] and v not in self.flag['dynamic']:
                self.flag['dynamic'].append(v)
            self.dset[v] = np.array([])

    def NodeCoordinates2Hash(self, NodeCoords):
        return np.array([hashlib.md5(i.tobytes()).digest() for i in NodeCoords], dtype="S16")

    def ParseSEM3DSnapshots(self):
        self.GlobalReNumbering()

        print("\n" + "=" * 30)
        print(f"RANK {self.rank} DIAGNOSTIC")
        eg = self.dset['ElementsGlobal']
        print(f"ElementsGlobal Shape: {eg.shape}")
        print(f"First element nodes:  {eg[0]}")
        print(f"Max Node Index:       {eg.max()}")
        print("=" * 30 + "\n")

        # -------------------------------------------------------------
        # Static data
        # -------------------------------------------------------------
        for g in self.snapfile['np']:
            with hf.File(osj(self.wkd, f'geometry{g:04d}.h5'), 'r') as h5f:
                for v in self.flag['static']:
                    if self.dset[v].size == 0:
                        self.dset[v] = h5f[v][...]
                    else:
                        self.dset[v] = np.append(self.dset[v], h5f[v][...], axis=0)

        for v in self.flag['static']:
            if sup[v] == "node":
                values_local_unique = self.dset[v][self.LocalElementConnectivityOriginal]
                values_local_unique = values_local_unique[self.LocalNodeUniqueHashIndex]

                # local unique nodal values, compatible with LocalElementConnectivityUnique
                self.dset[f"{v}_local_unique"] = values_local_unique

                # owned-only nodal values, indexed by Global2UniqueLocalIndexOnRank
                self.dset[v] = values_local_unique[self.Local2UniqueLocalIndexOnRank]

        # -------------------------------------------------------------
        # Dynamic data
        # -------------------------------------------------------------
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
                processed_data = np.stack(time_series_data, axis=-1)
                self.dset[v] = processed_data
                print(f"Rank {self.rank}: Variable {v} stored as FLAT array {self.dset[v].shape}")

    def GlobalReNumbering(self):
        LocalNodeCoordinates = None
        LocalElementConnectivity = None
        NodeCount = 0
        self.ElementCount = 0

        for g in self.snapfile['np']:
            with hf.File(osj(self.wkd, f'geometry{g:04d}.h5'), 'r') as h5f:
                OnFileNodeCoordinates = h5f["Nodes"][...].astype(np.float64).round(decimals=6)

                if LocalNodeCoordinates is None:
                    LocalNodeCoordinates = OnFileNodeCoordinates
                else:
                    LocalNodeCoordinates = np.append(LocalNodeCoordinates, OnFileNodeCoordinates, axis=0)

                OnFileElementConnectivity = h5f["Elements"][...].astype(np.int64) - 1 + NodeCount

                if LocalElementConnectivity is None:
                    LocalElementConnectivity = OnFileElementConnectivity
                else:
                    LocalElementConnectivity = np.append(
                        LocalElementConnectivity,
                        OnFileElementConnectivity,
                        axis=0
                    )

                NodeCount += OnFileNodeCoordinates.shape[0]
                self.ElementCount += OnFileElementConnectivity.shape[0]

        if LocalElementConnectivity is None:
            raise RuntimeError(
                f"Rank {self.rank}: no geometry file was read. "
                f"wkd={self.wkd}, assigned files={self.snapfile['np']}, "
                f"total geometry files found={self.snapfile['nc']}"
            )

        num_elements = LocalElementConnectivity.shape[0]

        cells = []
        for conn in LocalElementConnectivity:
            cells.append(8)
            cells.extend(conn)

        cell_types = np.full(num_elements, 12, dtype=np.uint8)
        cells = np.array(cells, dtype=np.int64)

        hex_mesh = pv.UnstructuredGrid(cells, cell_types, LocalNodeCoordinates)
        hex_mesh.save(f"multi_hexahedral_mesh_{self.rank}.vtk")

        LocalNodeHash = self.NodeCoordinates2Hash(LocalNodeCoordinates)

        LocalNodeUniqueHash, self.LocalNodeUniqueHashIndex, LocalNodeUniqueHashInverse = np.unique(
            LocalNodeHash[LocalElementConnectivity.flatten()],
            return_index=True,
            return_inverse=True,
            axis=0
        )

        self.LocalElementConnectivityOriginal = LocalElementConnectivity.flatten().copy()
        LocalNodeCoordinates = LocalNodeCoordinates[LocalElementConnectivity.flatten(), :][self.LocalNodeUniqueHashIndex, :]
        self.LocalNodeCount = LocalNodeUniqueHash.size

        LocalElementConnectivity = LocalNodeUniqueHashInverse.reshape(-1, 8)
        self.LocalElementConnectivityUnique = LocalElementConnectivity.copy()

        GlobalNodeHash = self.comm.allgather(LocalNodeUniqueHash)
        RankPerGlobalNode = np.concatenate(
            [r * np.ones((GlobalNodeHash[r].size,)) for r in range(self.size)],
            axis=0
        ).astype(np.int64)

        GlobalNodeHash, GlobalUniqueIndex = np.unique(
            np.concatenate(GlobalNodeHash),
            axis=0,
            return_index=True
        )

        self.GlobalNumberofNodes = GlobalNodeHash.size
        RankPerGlobalNode = RankPerGlobalNode[GlobalUniqueIndex]
        OnRankIndexPerGlobalNode = np.argwhere(RankPerGlobalNode == self.rank).flatten()

        _, Local2UniqueLocalIndexOnRank, Global2UniqueLocalIndexOnRank = np.intersect1d(
            LocalNodeUniqueHash,
            GlobalNodeHash,
            assume_unique=True,
            return_indices=True
        )

        _, index, _ = np.intersect1d(
            Global2UniqueLocalIndexOnRank,
            OnRankIndexPerGlobalNode,
            assume_unique=True,
            return_indices=True
        )

        self.dset["ElementsGlobal"] = Global2UniqueLocalIndexOnRank[LocalElementConnectivity]
        self.dset["NodesGlobal"] = LocalNodeCoordinates[Local2UniqueLocalIndexOnRank[index]]

        self.Local2UniqueLocalIndexOnRank = Local2UniqueLocalIndexOnRank[index]
        self.Global2UniqueLocalIndexOnRank = Global2UniqueLocalIndexOnRank[index]
        self.GlobalNodeCount = self.dset["NodesGlobal"].shape[0]

    def compute_misfit_gradients(self, snp_adj, dt):
        ev = self.dset['eps_vol']
        ev_adj = snp_adj.dset['eps_vol']

        detJ_elem = np.mean(
            self.dset['Jac_local_unique'][self.LocalElementConnectivityUnique],
            axis=1
        )

        vol_term = ev * ev_adj

        e_ij_names = ['xx', 'yy', 'zz', 'xy', 'yz', 'xz']
        dev_term = np.zeros_like(vol_term)

        for c in e_ij_names:
            factor = 2.0 if c in ['xy', 'yz', 'xz'] else 1.0
            dev_term += factor * (self.dset[f'eps_dev_{c}'] * snp_adj.dset[f'eps_dev_{c}'])

        sum_time_lam = np.sum(vol_term, axis=1) * dt
        sum_time_mu = np.sum(2.0 * vol_term + dev_term, axis=1) * dt

        g_mis_lambda = -sum_time_lam * detJ_elem
        g_mis_mu = -sum_time_mu * detJ_elem

        return g_mis_lambda, g_mis_mu

    def compute_local_contribution_rhs(self, snp_adj, dt, R_lam=1.0, R_mu=1.0):
        g_mis_lam, g_mis_mu = self.compute_misfit_gradients(snp_adj, dt)

        local_sum_lam = np.zeros(self.GlobalNumberofNodes)
        local_sum_mu = np.zeros(self.GlobalNumberofNodes)

        elements_global_map = self.dset["ElementsGlobal"]

        np.add.at(local_sum_lam, elements_global_map.flatten(), np.repeat(g_mis_lam, 8))
        np.add.at(local_sum_mu, elements_global_map.flatten(), np.repeat(g_mis_mu, 8))

        rank_indices = self.Global2UniqueLocalIndexOnRank

        local_sum_lam[rank_indices] += R_lam * (self.dset['Mass'] * self.dset['Lamb'])
        local_sum_mu[rank_indices] += R_mu * (self.dset['Mass'] * self.dset['Mu'])

        return local_sum_lam, local_sum_mu

    def solve_gradients_parallel(self, snp_adj, dt, R_lam=1.0, R_mu=1.0):
        loc_rhs_lam, loc_rhs_mu = self.compute_local_contribution_rhs(snp_adj, dt, R_lam, R_mu)

        loc_M = np.zeros(self.GlobalNumberofNodes)
        loc_Dens = np.zeros(self.GlobalNumberofNodes)
        loc_Lamb = np.zeros(self.GlobalNumberofNodes)
        loc_Mu = np.zeros(self.GlobalNumberofNodes)

        loc_M[self.Global2UniqueLocalIndexOnRank] = self.dset['Mass']
        loc_Dens[self.Global2UniqueLocalIndexOnRank] = self.dset['Dens']
        loc_Lamb[self.Global2UniqueLocalIndexOnRank] = self.dset['Lamb']
        loc_Mu[self.Global2UniqueLocalIndexOnRank] = self.dset['Mu']

        num_nodes = self.GlobalNumberofNodes
        counts = [num_nodes // self.size + (1 if r < num_nodes % self.size else 0) for r in range(self.size)]
        my_count = counts[self.rank]

        chunk_rhs_lam = np.zeros(my_count)
        chunk_rhs_mu = np.zeros(my_count)
        chunk_M = np.zeros(my_count)
        chunk_Dens = np.zeros(my_count)
        chunk_Lamb = np.zeros(my_count)
        chunk_Mu = np.zeros(my_count)

        print(f"Rank {self.rank} - local contribution computed. Preparing for Reduce_scatter with counts: {counts}")

        self.comm.Reduce_scatter(loc_rhs_lam, chunk_rhs_lam, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_rhs_mu, chunk_rhs_mu, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_M, chunk_M, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_Dens, chunk_Dens, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_Lamb, chunk_Lamb, recvcounts=counts, op=MPI.SUM)
        self.comm.Reduce_scatter(loc_Mu, chunk_Mu, recvcounts=counts, op=MPI.SUM)

        print(f"Rank {self.rank} - gathered local chunk data. Processing...")

        mask = chunk_M > 0
        g_lam_chunk = np.zeros(my_count)
        g_mu_chunk = np.zeros(my_count)

        g_lam_chunk[mask] = (chunk_Dens[mask] * chunk_rhs_lam[mask]) / chunk_M[mask]
        g_mu_chunk[mask] = (chunk_Dens[mask] * chunk_rhs_mu[mask]) / chunk_M[mask]

        print(f"Rank {self.rank} - local gradients computed.")

        return g_lam_chunk, g_mu_chunk, chunk_Lamb, chunk_Mu, counts


def ParseCL():
    parser = argparse.ArgumentParser(prefix_chars='@')
    parser.add_argument('@@wkd', type=str, default='./res', help="Path to res directory")
    parser.add_argument(
        '@@var',
        type=str,
        nargs='+',
        default=[
            'Mass', 'Jac', 'Mu', 'Lamb', 'Nodes',
            'Elements', 'Dens', 'Dom', 'displ',
            'eps_vol', 'eps_dev_xx', 'eps_dev_yy', 'eps_dev_zz',
            'eps_dev_xy', 'eps_dev_yz', 'eps_dev_xz'
        ],
        help="Select snapshot"
    )
    parser.add_argument('@@begin_time', '@b', type=int, default=1, help="Initial time step to parse")
    parser.add_argument('@@end_time', '@e', type=int, default=-1, help="Final time step to parse")

    args, _ = parser.parse_known_args()
    opt = vars(args)

    forward_wkd = Path(opt['wkd']).resolve()
    project_root = forward_wkd.parents[1]
    adj_wkd = project_root / "sem3d_config_files_adj" / "res"

    opt_adj = opt.copy()
    opt_adj['wkd'] = str(adj_wkd)
    opt_adj['var'] = [
        'eps_vol', 'eps_dev_xx',
        'eps_dev_yy', 'eps_dev_zz',
        'eps_dev_xy', 'eps_dev_yz',
        'eps_dev_xz'
    ]

    return opt, opt_adj


def GetSnapshots(comm, size, rank):
    opt, opt_adj = ParseCL()

    opt["comm"] = comm
    opt["size"] = size
    opt["rank"] = rank

    opt_adj["comm"] = comm
    opt_adj["size"] = size
    opt_adj["rank"] = rank

    snp = SnapshotsSEM3D(**opt)
    snp_adj = SnapshotsSEM3D(**opt_adj)

    snp.ParseSEM3DSnapshots()
    print(f"Elements shape: {snp.dset['eps_vol'].shape}")
    snp_adj.ParseSEM3DSnapshots()

    print(f"Rank {rank} - snapshots parsed. Starting gradient computation...")
    return snp, snp_adj


def main():
    MPI.Init()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    snp, snp_adj = GetSnapshots(comm, size, rank)

    NumberofElements = np.array(comm.allgather(snp.ElementCount * 8))

    if rank == 0:
        recvbuf = np.empty(sum(NumberofElements), dtype=np.int64)
    else:
        recvbuf = None

    comm.Gatherv(
        sendbuf=snp.dset["ElementsGlobal"].flatten(),
        recvbuf=[
            recvbuf,
            NumberofElements,
            [sum(NumberofElements[:i]) for i in range(len(NumberofElements))],
            MPI.LONG_LONG
        ],
        root=0
    )

    if rank == 0:
        ElementsGlob = recvbuf.astype(np.int64).reshape((-1, 8))
    else:
        ElementsGlob = None

    NumberofNodeCoordinates = np.array(comm.allgather(snp.GlobalNodeCount * 3))

    if rank == 0:
        recvbuf = np.empty(sum(NumberofNodeCoordinates), dtype=np.float64)
    else:
        recvbuf = None

    comm.Gatherv(
        sendbuf=snp.dset["NodesGlobal"].astype(np.float64).flatten(),
        recvbuf=[
            recvbuf,
            NumberofNodeCoordinates,
            [sum(NumberofNodeCoordinates[:i]) for i in range(len(NumberofNodeCoordinates))],
            MPI.DOUBLE
        ],
        root=0
    )

    if rank == 0:
        NodesTemp = recvbuf.astype(np.float64).reshape((-1, 3))
    else:
        NodesTemp = None

    NumberofNodes = np.array(comm.allgather(snp.GlobalNodeCount))

    if rank == 0:
        recvbuf = np.empty(sum(NumberofNodes), dtype=np.float64)
    else:
        recvbuf = None

    comm.Gatherv(
        sendbuf=snp.Global2UniqueLocalIndexOnRank.astype(np.float64),
        recvbuf=[
            recvbuf,
            NumberofNodes,
            [sum(NumberofNodes[:i]) for i in range(len(NumberofNodes))],
            MPI.DOUBLE
        ],
        root=0
    )

    if rank == 0:
        NodesIndex = recvbuf.astype(np.int64)
        NodesGlobal = np.empty_like(NodesTemp)
        NodesGlobal[NodesIndex] = NodesTemp
    else:
        NodesIndex = None
        NodesGlobal = None

    selected_var = snp.var[0]
    NumberofVectorComponents = NumberofNodeCoordinates * snp.nt

    if rank == 0:
        recvbuf = np.empty(sum(NumberofVectorComponents), dtype=np.float64)
    else:
        recvbuf = None

    comm.Gatherv(
        sendbuf=snp.dset[selected_var].astype(np.float64).flatten(),
        recvbuf=[
            recvbuf,
            NumberofVectorComponents,
            [sum(NumberofVectorComponents[:i]) for i in range(len(NumberofVectorComponents))],
            MPI.DOUBLE
        ],
        root=0
    )

    if rank == 0:
        DisplTemp = recvbuf.astype(np.float64).reshape((-1, 3, snp.nt))
        DisplGlobal = np.empty_like(DisplTemp)
        DisplGlobal[NodesIndex] = DisplTemp
    else:
        DisplGlobal = None

    if rank == 0:
        num_elements = ElementsGlob.shape[0]
        cells = []
        for conn in ElementsGlob:
            cells.append(8)
            cells.extend(conn)
        cells = np.array(cells, dtype=np.int64)
        cell_types = np.full(num_elements, 12, dtype=np.uint8)

        hex_mesh = pv.UnstructuredGrid(cells, cell_types, NodesGlobal)

        for j in range(DisplGlobal.shape[-1]):
            t = snp.begin_time + j
            hex_mesh[selected_var] = DisplGlobal[:, :, j].reshape((-1, 3))
            hex_mesh.save(f"multi_hexahedral_mesh_{t}.vtu")

    MPI.Finalize()


def compute_gradients_main(
    comm,
    size,
    rank,
    x_bounds=[-1300, 1300],
    y_bounds=[-1300, 1300],
    z_bounds=[-1540, 0],
    steps=[200, 200, 20],
    cache_dir="./",
    wrt=True
):
    if rank == 0:
        print(f"--- Step 1: Initializing snapshots on {size} ranks ---")

    snp, snp_adj = GetSnapshots(comm, size, rank)

    if rank == 0:
        print("--- Step 2: Solving physical gradients on GLL mesh ---")

    g_lam_chunk, g_mu_chunk, lam_chunk, mu_chunk, counts = snp.solve_gradients_parallel(snp_adj, dt=0.5)

    phys_offsets = np.cumsum([0] + counts)

    x_range = np.arange(x_bounds[0], x_bounds[1] + steps[0], steps[0])
    y_range = np.arange(y_bounds[0], y_bounds[1] + steps[1], steps[1])
    z_range = np.arange(z_bounds[0], z_bounds[1] + steps[2], steps[2])
    total_mat_nodes = len(x_range) * len(y_range) * len(z_range)

    cache_file = os.path.join(cache_dir, f'mesh_mapping_rank_{rank}.npz')

    if os.path.exists(cache_file):
        if rank == 0:
            print(f"--- Step 3: Loading mapping from cache: {cache_dir} ---")
        data = np.load(cache_file)
        mat_nodes_local = data['coords']
        mat_phys_idx_local = data['idx']
        mat_global_indices = data['global_mask_idx']
    else:
        if rank == 0:
            print("--- Step 3: No cache found. Starting Global Mapping process ---")

        local_nodes = snp.dset['NodesGlobal']
        local_ids = snp.Global2UniqueLocalIndexOnRank.astype(np.int64)

        owned_counts = comm.allgather(local_nodes.shape[0])
        owned_counts_3d = [3 * c for c in owned_counts]
        owned_displs = [sum(owned_counts[:i]) for i in range(size)]
        owned_displs_3d = [3 * d for d in owned_displs]

        if rank == 0:
            tmp_coords = np.empty(sum(owned_counts_3d), dtype=np.float64)
            tmp_ids = np.empty(sum(owned_counts), dtype=np.int64)
        else:
            tmp_coords = None
            tmp_ids = None

        comm.Gatherv(
            sendbuf=local_nodes.astype(np.float64).flatten(),
            recvbuf=[tmp_coords, owned_counts_3d, owned_displs_3d, MPI.DOUBLE],
            root=0
        )

        comm.Gatherv(
            sendbuf=local_ids,
            recvbuf=[tmp_ids, owned_counts, owned_displs, MPI.LONG_LONG],
            root=0
        )

        if rank == 0:
            print(f"Rank 0: Rebuilding global physical coordinate array for {snp.GlobalNumberofNodes} nodes...")
            all_nodes_phys = np.empty((snp.GlobalNumberofNodes, 3), dtype=np.float64)
            all_nodes_phys[tmp_ids] = tmp_coords.reshape(-1, 3)

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
            send_mat_coords = None
            send_phys_indices = None
            send_global_mask = None
            mat_counts = None

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

    if rank == 0:
        print("--- Step 4: Extracting local data and assembling coordinate vectors ---")

    local_idx_mapped = mat_phys_idx_local - phys_offsets[rank]

    grad_lam_local = g_lam_chunk[local_idx_mapped]
    grad_mu_local = g_mu_chunk[local_idx_mapped]
    lam_val_local = lam_chunk[local_idx_mapped]
    mu_val_local = mu_chunk[local_idx_mapped]

    if wrt:
        x_gl = np.zeros(total_mat_nodes, dtype=np.float64)
        y_gl = np.zeros(total_mat_nodes, dtype=np.float64)
        z_gl = np.zeros(total_mat_nodes, dtype=np.float64)

        x_gl[mat_global_indices] = mat_nodes_local[:, 0]
        y_gl[mat_global_indices] = mat_nodes_local[:, 1]
        z_gl[mat_global_indices] = mat_nodes_local[:, 2]

        if rank == 0:
            print("--- Final Step: Computation and assembly complete. Returning vectors. ---")

        return (
            grad_lam_local, grad_mu_local,
            lam_val_local, mu_val_local,
            mat_global_indices,
            x_gl, y_gl, z_gl
        )

    if rank == 0:
        print("--- Final Step: Computation and assembly complete. Returning local vectors only. ---")

    return (
        grad_lam_local, grad_mu_local,
        lam_val_local, mu_val_local,
        mat_global_indices,
        None, None, None
    )


if __name__ == "__main__":
    main()