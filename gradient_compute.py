# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
gradient_compute.py — RTM gradient via cross-correlation of forward and adjoint strain snapshots.

Computes the sensitivity kernels:

    g_λ(x) = ∫₀ᵀ  tr(ε[u(x,t)])  ·  tr(ε[Λ(x,t)])  dt
    g_μ(x) = ∫₀ᵀ  dev(ε[u(x,t)]) : dev(ε[Λ(x,t)])  dt

where u is the forward wavefield (forward solve) and Λ is the adjoint wavefield
(adjoint solve with time-reversed residuals as sources at receivers).

The integral is discretised as a sum over N_snap snapshots spaced dt_snap apart.
Each snapshot k covers physical time t = k * dt_snap.

The MPI strategy mirrors parse_sem3d_snapshots.py:
  - SEM3D writes one geometry file and one sem_field file per SEM3D MPI rank.
  - Python MPI ranks distribute these files among themselves.
  - No communication is needed during the accumulation loop — each Python rank
    works on its own GLL points independently.
  - A single Gatherv at the end collects the result on rank 0.

Usage:
    mpirun -np N python3 gradient_compute.py       \\
        @@wkd      /path/to/sim/dir               \\
        @@res_fwd  res                             \\
        @@res_adj  res_adj                         \\
        @@out      gradient.h5                     \\
        @@n_snap   40                              \\
        @@dt_snap  0.5

    @@wkd      : simulation directory containing geometry*.h5 and res*/ subdirs
    @@res_fwd  : subfolder name for forward snapshots  (default: res)
    @@res_adj  : subfolder name for adjoint snapshots  (default: res_adj)
    @@out      : output HDF5 file path                 (default: gradient.h5)
    @@n_snap   : number of snapshots (-1 = auto-detect from res_fwd)
    @@dt_snap  : time interval between snapshots [s]   (default: 0.5)
"""

import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize   = False
from mpi4py import MPI

import argparse
import glob
import os
from os.path import join as osj

import numpy as np
import h5py

# ── Dataset names inside sem_field.PPPP.h5 ──────────────────────────────────
# These match the variable names used by SEM3D and declared in parse_sem3d_snapshots.py
VAR_EVOL = 'eps_vol'
VAR_EDEV = [
    'eps_dev_xx',   # index 0  →  ε_xx  (diagonal)
    'eps_dev_yy',   # index 1  →  ε_yy  (diagonal)
    'eps_dev_zz',   # index 2  →  ε_zz  (diagonal)
    'eps_dev_xy',   # index 3  →  ε_xy  (off-diagonal, counted twice)
    'eps_dev_xz',   # index 4  →  ε_xz  (off-diagonal, counted twice)
    'eps_dev_yz',   # index 5  →  ε_yz  (off-diagonal, counted twice)
]

# Double-dot product weights for symmetric tensor stored as [xx,yy,zz,xy,xz,yz]:
#   A:B = A_xx*B_xx + A_yy*B_yy + A_zz*B_zz + 2*(A_xy*B_xy + A_xz*B_xz + A_yz*B_yz)
# Factor 2 accounts for the symmetry A_ij = A_ji (off-diagonal terms appear twice in 3x3 sum)
EDEV_WEIGHTS = np.array([1., 1., 1., 2., 2., 2.], dtype=np.float64)


# ── Low-level I/O helpers ────────────────────────────────────────────────────

def _snap_path(wkd, res_dir, k, g):
    """
    Return the path to sem_field.{g}.h5 for snapshot index k.

    Parameters
    ----------
    wkd     : str   simulation root directory
    res_dir : str   name of the results subdirectory (e.g. 'res' or 'res_adj')
    k       : int   snapshot index  (1-based, matches Rsem directory numbering)
    g       : int   geometry-file / SEM3D-rank index
    """
    return osj(wkd, res_dir, 'Rsem{:>04d}'.format(k), 'sem_field.{:>04d}.h5'.format(g))


def _read_var(path, varname):
    """
    Read a single dataset from an HDF5 file and return it as a 1-D float64 array.

    Parameters
    ----------
    path    : str   path to .h5 file
    varname : str   dataset name inside the file

    Returns
    -------
    np.ndarray  shape (N_gll_in_file,)  float64
    """
    with h5py.File(path, 'r') as f:
        return f[varname][...].ravel().astype(np.float64)


def _read_evol_edev(wkd, res_dir, k, geo_indices):
    """
    Read eps_vol and all eps_dev_* components from snapshot k for a list of
    geometry-file indices, and concatenate across those files.

    Parameters
    ----------
    wkd         : str        simulation root directory
    res_dir     : str        results subdirectory name
    k           : int        snapshot index (1-based)
    geo_indices : list[int]  geometry-file indices assigned to this MPI rank

    Returns
    -------
    evol : np.ndarray  shape (N_gll_local,)      tr(ε)
    edev : np.ndarray  shape (N_gll_local, 6)    dev(ε) components [xx,yy,zz,xy,xz,yz]
    """
    evol_parts = []
    edev_parts = []   # each entry will be shape (N_gll_in_file, 6)

    for g in geo_indices:
        path = _snap_path(wkd, res_dir, k, g)

        evol_parts.append(_read_var(path, VAR_EVOL))

        # Read all 6 edev components and stack as columns → (N_gll_in_file, 6)
        edev_parts.append(
            np.column_stack([_read_var(path, v) for v in VAR_EDEV])
        )

    evol = np.concatenate(evol_parts)                  # shape: (N_gll_local,)
    edev = np.concatenate(edev_parts, axis=0)          # shape: (N_gll_local, 6)
    return evol, edev


# ── MPI distribution of geometry files ──────────────────────────────────────

def _distribute_geo_files(wkd, res_fwd, rank, size):
    """
    Distribute geometry-file indices (0..n_geo-1) across MPI ranks.

    The distribution mirrors SnapshotsSEM3D.setup() in parse_sem3d_snapshots.py:
    geometry files are numbered contiguously and split as evenly as possible.

    Parameters
    ----------
    wkd     : str   simulation root directory
    res_fwd : str   forward results subdirectory (used to discover sem_field files)
    rank    : int   this MPI rank
    size    : int   total number of MPI ranks

    Returns
    -------
    local_indices : list[int]  geometry-file indices for this rank
    n_geo         : int        total number of geometry files
    """
    # Discover all sem_field files for snapshot 1 to count geometry partitions
    snap1_files = sorted(
        glob.glob(osj(wkd, res_fwd, 'Rsem{:>04d}'.format(1), 'sem_field.*.h5'))
    )
    n_geo = len(snap1_files)

    if n_geo == 0:
        raise RuntimeError(
            f"No sem_field files found in {osj(wkd, res_fwd, 'Rsem0001')}. "
            "Check @@wkd and @@res_fwd."
        )

    # Extract integer indices from filenames: sem_field.{g:>04d}.h5
    all_indices = sorted(
        int(os.path.splitext(os.path.basename(f))[0].split('.')[1])
        for f in snap1_files
    )

    # Round-robin distribution: same logic as SnapshotsSEM3D.setup()
    q, r = divmod(n_geo, size)
    if rank < r:
        local_indices = all_indices[rank * (q + 1) : rank * (q + 1) + (q + 1)]
    else:
        local_indices = all_indices[r * (q + 1) + (rank - r) * q :
                                    r * (q + 1) + (rank - r) * q + q]

    return local_indices, n_geo


# ── Core gradient computation ────────────────────────────────────────────────

def compute_gradient(comm, size, rank, wkd, res_fwd, res_adj, n_snap, dt_snap, out_file):
    """
    Compute g_lambda and g_mu for all GLL points, then gather to rank 0 and write.

    Algorithm (per MPI rank):
        g_lambda_local = 0
        g_mu_local     = 0
        for k = 1..n_snap:
            evol_fwd = tr(ε[u])  at snapshot k         (from res_fwd/Rsem{k})
            evol_adj = tr(ε[Λ])  at snapshot n_snap+1-k (from res_adj/Rsem{n_snap+1-k})
            edev_fwd = dev(ε[u])                        shape (N_gll_local, 6)
            edev_adj = dev(ε[Λ])                        shape (N_gll_local, 6)
            g_lambda_local += evol_fwd * evol_adj * dt_snap
            g_mu_local     += (WEIGHTS * edev_fwd * edev_adj).sum(axis=1) * dt_snap

    The adjoint snapshots are indexed in reverse because SEM3D saves them in the
    order they are computed (from T→0), so Rsem1 of the adjoint corresponds to
    physical time T and Rsem{n_snap} corresponds to physical time dt_snap:

        Forward Rsem{k}          → physical time  t = k * dt_snap
        Adjoint Rsem{n_snap+1-k} → physical time  t = k * dt_snap  (time-reversed)

    Parameters
    ----------
    comm     : MPI.Comm
    size     : int    total MPI ranks
    rank     : int    this rank
    wkd      : str    simulation root directory
    res_fwd  : str    forward results subdirectory name
    res_adj  : str    adjoint results subdirectory name
    n_snap   : int    number of snapshots
    dt_snap  : float  time interval between snapshots [s]
    out_file : str    path for output HDF5 file
    """

    # ── 1. Distribute geometry files ─────────────────────────────────────────
    local_indices, n_geo = _distribute_geo_files(wkd, res_fwd, rank, size)

    if rank == 0:
        print(f"[gradient_compute] geometry files: {n_geo}, "
              f"MPI ranks: {size}, snapshots: {n_snap}, dt_snap: {dt_snap} s")
    print(f"  Rank {rank:02d}: geometry files {local_indices}")
    comm.Barrier()

    # ── 2. Determine local GLL count by reading snapshot k=1 ─────────────────
    evol_probe, _ = _read_evol_edev(wkd, res_fwd, 1, local_indices)
    n_gll_local   = evol_probe.size   # number of GLL integration points on this rank

    # ── 3. Accumulate gradient over all snapshots ─────────────────────────────
    # g_lambda[i] = Σ_k  evol_fwd[i,k] * evol_adj[i,k] * dt_snap
    # g_mu[i]     = Σ_k  (EDEV_WEIGHTS * edev_fwd[i,:,k] * edev_adj[i,:,k]).sum() * dt_snap
    g_lambda_local = np.zeros(n_gll_local, dtype=np.float64)
    g_mu_local     = np.zeros(n_gll_local, dtype=np.float64)

    for k in range(1, n_snap + 1):

        # Forward snapshot k → physical time t = k * dt_snap
        fwd_snap = k

        # Adjoint snapshot (n_snap + 1 - k) → same physical time t = k * dt_snap
        # (adjoint is saved T→0, so Rsem1 = t=T, Rsem{n_snap} = t=dt_snap)
        adj_snap = n_snap + 1 - k

        evol_fwd, edev_fwd = _read_evol_edev(wkd, res_fwd, fwd_snap, local_indices)
        evol_adj, edev_adj = _read_evol_edev(wkd, res_adj, adj_snap, local_indices)
        # evol_fwd/adj : shape (n_gll_local,)
        # edev_fwd/adj : shape (n_gll_local, 6)

        # g_λ contribution at this timestep — pointwise scalar product of evol
        g_lambda_local += evol_fwd * evol_adj * dt_snap
        # result shape: (n_gll_local,)

        # g_μ contribution — weighted double-dot product of deviatoric tensors
        # edev[u] : edev[Λ] = Σ_ij w_ij * edev_ij[u] * edev_ij[Λ]
        # EDEV_WEIGHTS = [1,1,1,2,2,2] accounts for off-diagonal symmetry
        dd = np.sum(EDEV_WEIGHTS * edev_fwd * edev_adj, axis=1)
        # dd shape: (n_gll_local,)
        g_mu_local += dd * dt_snap

        if rank == 0 and k % 10 == 0:
            print(f"  Rank 0: processed snapshot {k}/{n_snap}")

    comm.Barrier()
    if rank == 0:
        print(f"[gradient_compute] accumulation done, gathering...")

    # ── 4. Gather local GLL counts from all ranks ─────────────────────────────
    # n_gll_per_rank[p] = number of GLL points on rank p
    n_gll_per_rank = np.array(comm.allgather(n_gll_local), dtype=np.int64)
    n_gll_total    = int(n_gll_per_rank.sum())
    displacements  = [int(n_gll_per_rank[:p].sum()) for p in range(size)]

    # ── 5. Gather g_lambda and g_mu to rank 0 ────────────────────────────────
    if rank == 0:
        g_lambda_global = np.empty(n_gll_total, dtype=np.float64)
        g_mu_global     = np.empty(n_gll_total, dtype=np.float64)
    else:
        g_lambda_global = None
        g_mu_global     = None

    comm.Gatherv(
        sendbuf=g_lambda_local,
        recvbuf=[g_lambda_global, n_gll_per_rank.tolist(), displacements, MPI.DOUBLE],
        root=0
    )
    comm.Gatherv(
        sendbuf=g_mu_local,
        recvbuf=[g_mu_global, n_gll_per_rank.tolist(), displacements, MPI.DOUBLE],
        root=0
    )

    # ── 6. Write output HDF5 on rank 0 ────────────────────────────────────────
    # Output layout:
    #   /g_lambda          shape (n_gll_total,)  ∂J/∂λ per GLL point (element support)
    #   /g_mu              shape (n_gll_total,)  ∂J/∂μ per GLL point (element support)
    #   /n_gll_per_rank    shape (size,)         GLL count per MPI rank (for reassembly)
    #   attrs: n_snap, dt_snap, n_geo, n_gll_total
    #
    # NOTE: the gradient is stored in the same GLL-point order as the sem_field files
    # (element support, concatenated by rank in the order defined by n_gll_per_rank).
    # To map back to the material grid (example_la.h5, example_mu.h5) an interpolation
    # step using node coordinates from geometry*.h5 is required.
    if rank == 0:
        with h5py.File(out_file, 'w') as f:
            f.create_dataset('g_lambda',       data=g_lambda_global)
            f.create_dataset('g_mu',           data=g_mu_global)
            f.create_dataset('n_gll_per_rank', data=n_gll_per_rank)
            f.attrs['n_snap']      = n_snap
            f.attrs['dt_snap']     = dt_snap
            f.attrs['n_geo']       = n_geo
            f.attrs['n_gll_total'] = n_gll_total

        print(f"\n[gradient_compute] written to {out_file}")
        print(f"  g_lambda : shape {g_lambda_global.shape}  "
              f"norm = {np.linalg.norm(g_lambda_global):.6e}")
        print(f"  g_mu     : shape {g_mu_global.shape}  "
              f"norm = {np.linalg.norm(g_mu_global):.6e}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def _parse_cl():
    parser = argparse.ArgumentParser(prefix_chars='@')
    parser.add_argument('@@wkd',      type=str,   default='.',
                        help="Simulation root dir (contains geometry*.h5 and res*/)")
    parser.add_argument('@@res_fwd',  type=str,   default='res',
                        help="Forward results subdirectory name  (default: res)")
    parser.add_argument('@@res_adj',  type=str,   default='res_adj',
                        help="Adjoint results subdirectory name  (default: res_adj)")
    parser.add_argument('@@out',      type=str,   default='gradient.h5',
                        help="Output HDF5 file path              (default: gradient.h5)")
    parser.add_argument('@@n_snap',   type=int,   default=-1,
                        help="Number of snapshots (-1 = auto-detect from res_fwd)")
    parser.add_argument('@@dt_snap',  type=float, default=0.5,
                        help="Snapshot time interval [s]         (default: 0.5)")
    return parser.parse_args().__dict__


def main():
    MPI.Init()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    opt = _parse_cl()

    # Auto-detect number of snapshots from the forward results directory
    if opt['n_snap'] == -1:
        rsem_dirs  = glob.glob(osj(opt['wkd'], opt['res_fwd'], 'Rsem*'))
        opt['n_snap'] = len(rsem_dirs)
        if rank == 0:
            print(f"[gradient_compute] auto-detected {opt['n_snap']} snapshots "
                  f"in {osj(opt['wkd'], opt['res_fwd'])}")

    compute_gradient(
        comm     = comm,
        size     = size,
        rank     = rank,
        wkd      = opt['wkd'],
        res_fwd  = opt['res_fwd'],
        res_adj  = opt['res_adj'],
        n_snap   = opt['n_snap'],
        dt_snap  = opt['dt_snap'],
        out_file = opt['out'],
    )

    MPI.Finalize()


if __name__ == '__main__':
    main()
