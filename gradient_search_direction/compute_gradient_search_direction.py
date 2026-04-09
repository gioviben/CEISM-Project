#!/usr/bin/env python3
"""
MPI script to compute local gradients and L-BFGS search directions
from distributed SEM3D snapshots.

This script is meant to be launched with mpirun from a sequential main script.
Each MPI rank:
- computes its local gradients,
- reloads its previous optimizer state from disk,
- updates local L-BFGS memory,
- computes the local search direction,
- saves directions and updated state back to disk.

At iteration 0 only:
- it also computes x_gl, y_gl, z_gl,
- reduces them to rank 0,
- rank 0 saves them once as a list of tuples:
  [(x1, y1, z1), (x2, y2, z2), ...]
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path
from typing import Any
from util_funct.compute_dir_parallel import compute_dir_parallel
import numpy as np
from mpi4py import MPI
from pysem.src.pysem.parse_sem3d_snapshots import compute_gradients_main

# ---------------------------------------------------------------------
# Helpers for persistent rank-local optimizer state
# ---------------------------------------------------------------------
def get_rank_state_path(state_dir: Path, rank: int) -> Path:
    """Return the path of the optimizer state file for one MPI rank."""
    return state_dir / f"lbfgs_state_rank_{rank:04d}.pkl"


def load_rank_state(state_dir: Path, rank: int) -> dict[str, Any]:
    """
    Load rank-local L-BFGS state from disk.

    If the state does not exist yet, return an empty initialized state.
    """
    state_path = get_rank_state_path(state_dir, rank)

    if not state_path.exists():
        return {
            "m_lam_old_chunk": None,
            "m_mu_old_chunk": None,
            "g_lam_old_chunk": None,
            "g_mu_old_chunk": None,
            "s_queue_lam": [],
            "y_queue_lam": [],
            "s_queue_mu": [],
            "y_queue_mu": [],
        }

    with open(state_path, "rb") as f:
        return pickle.load(f)


def save_rank_state(state_dir: Path, rank: int, state: dict[str, Any]) -> None:
    """Save rank-local L-BFGS state to disk."""
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path = get_rank_state_path(state_dir, rank)

    with open(state_path, "wb") as f:
        pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)


# ---------------------------------------------------------------------
# Helpers for chunk outputs
# ---------------------------------------------------------------------
def save_rank_outputs(
    output_dir: Path,
    iteration: int,
    rank: int,
    g_lam_chunk: np.ndarray,
    g_mu_chunk: np.ndarray,
    dir_lam_chunk: np.ndarray,
    dir_mu_chunk: np.ndarray,
) -> None:
    """
    Save rank-local outputs for this iteration.

    These files can later be read either by the sequential main script
    or by another MPI script dedicated to model update.
    """
    iter_dir = output_dir / f"iter_{iteration:04d}"
    iter_dir.mkdir(parents=True, exist_ok=True)

    out_path = iter_dir / f"rank_{rank:04d}.npz"
    np.savez_compressed(
        out_path,
        g_lam_chunk=g_lam_chunk,
        g_mu_chunk=g_mu_chunk,
        dir_lam_chunk=dir_lam_chunk,
        dir_mu_chunk=dir_mu_chunk,
    )

def save_global_xyz_tuples(
    output_dir: Path,
    x_tot: np.ndarray,
    y_tot: np.ndarray,
    z_tot: np.ndarray,
) -> None:
    """
    Save global reduced coordinates as a Python list of tuples:
    [(x1, y1, z1), (x2, y2, z2), ...]
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    xyz_tuples = list(zip(x_tot.tolist(), y_tot.tolist(), z_tot.tolist()))

    out_path = output_dir / "global_xyz_tuples.pkl"
    with open(out_path, "wb") as f:
        pickle.dump(xyz_tuples, f, protocol=pickle.HIGHEST_PROTOCOL)



def save_rank_metadata_once(
    output_dir: Path,
    iteration: int,
    size: int,
) -> None:
    """
    Let rank 0 write a small metadata file for convenience.
    """
    meta_path = output_dir / f"iter_{iteration:04d}" / "metadata.txt"
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(
        f"iteration={iteration}\n"
        f"n_ranks={size}\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------
def run_parallel_direction_step(
    iteration: int,
    lbfgs_mem: int,
    state_dir: Path,
    output_dir: Path,
) -> None:
    """
    Perform one MPI-distributed iteration step:
    - compute local gradients,
    - update L-BFGS queues,
    - compute local search directions,
    - save outputs and updated state.

    At iteration 0 only, compute and save global xyz tuples.
    """
    initialized_here = False
    if not MPI.Is_initialized():
        MPI.Init()
        initialized_here = True

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    compute_xyz = (iteration == 0)

    try:
        
        # -------------------------------------------------------------
        # 1. Compute local gradients & Current local model chunk
        # -------------------------------------------------------------
        
        g_lam_chunk, g_mu_chunk, m_lam_chunk, m_mu_chunk, x_gl, y_gl, z_gl = compute_gradients_main(compute_xyz)

        # -------------------------------------------------------------
        # 2. Reload previous rank-local L-BFGS state
        # -------------------------------------------------------------
        state = load_rank_state(state_dir, rank)

        m_lam_old_chunk = state["m_lam_old_chunk"]
        m_mu_old_chunk = state["m_mu_old_chunk"]
        g_lam_old_chunk = state["g_lam_old_chunk"]
        g_mu_old_chunk = state["g_mu_old_chunk"]

        s_queue_lam = state["s_queue_lam"]
        y_queue_lam = state["y_queue_lam"]
        s_queue_mu = state["s_queue_mu"]
        y_queue_mu = state["y_queue_mu"]

        # -------------------------------------------------------------
        # 3. Update L-BFGS memory
        # -------------------------------------------------------------
        if iteration > 0:
            if (
                m_lam_old_chunk is None
                or m_mu_old_chunk is None
                or g_lam_old_chunk is None
                or g_mu_old_chunk is None
            ):
                raise RuntimeError(
                    f"Rank {rank}: missing previous L-BFGS state "
                    f"for iteration {iteration}."
                )

            s_lam = m_lam_chunk - m_lam_old_chunk
            s_mu = m_mu_chunk - m_mu_old_chunk
            y_lam = g_lam_chunk - g_lam_old_chunk
            y_mu = g_mu_chunk - g_mu_old_chunk

            s_queue_lam.insert(0, s_lam)
            y_queue_lam.insert(0, y_lam)
            s_queue_mu.insert(0, s_mu)
            y_queue_mu.insert(0, y_mu)

            if len(s_queue_lam) > lbfgs_mem:
                s_queue_lam.pop()
                y_queue_lam.pop()

            if len(s_queue_mu) > lbfgs_mem:
                s_queue_mu.pop()
                y_queue_mu.pop()

        # -------------------------------------------------------------
        # 4. Compute local search directions
        # -------------------------------------------------------------
        M_len_lam = len(s_queue_lam)
        M_len_mu = len(s_queue_mu)

        dir_lam_chunk = compute_dir_parallel(
            g_lam_chunk,
            y_queue_lam,
            s_queue_lam,
            M_len_lam,
            comm,
        )

        dir_mu_chunk = compute_dir_parallel(
            g_mu_chunk,
            y_queue_mu,
            s_queue_mu,
            M_len_mu,
            comm,
        )

        # -------------------------------------------------------------
        # 5. Compute and save global xyz only once (iteration 0)
        # -------------------------------------------------------------
        if compute_xyz:
            if x_gl is None or y_gl is None or z_gl is None:
                raise RuntimeError(
                    f"Rank {rank}: iteration == 0 but x_gl/y_gl/z_gl is None."
                )

            # Elementwise sum of NumPy arrays across ranks.
            # Only rank 0 receives the final reduced vectors.
            if rank == 0:
                x_gl_tot = np.empty_like(x_gl)
                y_gl_tot = np.empty_like(y_gl)
                z_gl_tot = np.empty_like(z_gl)
            else:
                x_gl_tot = None
                y_gl_tot = None
                z_gl_tot = None

            comm.Reduce(x_gl, x_gl_tot, op=MPI.SUM, root=0)
            comm.Reduce(y_gl, y_gl_tot, op=MPI.SUM, root=0)
            comm.Reduce(z_gl, z_gl_tot, op=MPI.SUM, root=0)

            if rank == 0:
                save_global_xyz_tuples(output_dir, x_gl_tot, y_gl_tot, z_gl_tot)

        # -------------------------------------------------------------
        # 6. Save local outputs
        # -------------------------------------------------------------
        save_rank_outputs(
            output_dir=output_dir,
            iteration=iteration,
            rank=rank,
            g_lam_chunk=g_lam_chunk,
            g_mu_chunk=g_mu_chunk,
            dir_lam_chunk=dir_lam_chunk,
            dir_mu_chunk=dir_mu_chunk,
        )

        # -------------------------------------------------------------
        # 7. Save updated state for next outer iteration
        # -------------------------------------------------------------
        new_state = {
            "m_lam_old_chunk": m_lam_chunk.copy(),
            "m_mu_old_chunk": m_mu_chunk.copy(),
            "g_lam_old_chunk": g_lam_chunk.copy(),
            "g_mu_old_chunk": g_mu_chunk.copy(),
            "s_queue_lam": s_queue_lam,
            "y_queue_lam": y_queue_lam,
            "s_queue_mu": s_queue_mu,
            "y_queue_mu": y_queue_mu,
        }
        save_rank_state(state_dir, rank, new_state)

        # Optional metadata by rank 0

        if rank == 0:
            save_rank_metadata_once(output_dir, iteration, size)
            print(
                f"[MPI] Iteration {iteration} completed. "
                f"Directions saved in: {output_dir / f'iter_{iteration:04d}'}"
            )

    finally:
        if initialized_here and not MPI.Is_finalized():
            MPI.Finalize()


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute gradients and L-BFGS search directions in parallel with MPI."
    )
    parser.add_argument(
        "--iter",
        dest="iteration",
        type=int,
        required=True,
        help="Outer inversion iteration index.",
    )
    parser.add_argument(
        "--lbfgs-mem",
        dest="lbfgs_mem",
        type=int,
        required=True,
        help="Maximum L-BFGS memory length.",
    )
    parser.add_argument(
        "--state-dir",
        dest="state_dir",
        type=Path,
        required=True,
        help="Directory where rank-local optimizer states are stored.",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        type=Path,
        required=True,
        help="Directory where rank-local outputs are written.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    run_parallel_direction_step(
        iteration=args.iteration,
        lbfgs_mem=args.lbfgs_mem,
        state_dir=args.state_dir,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()