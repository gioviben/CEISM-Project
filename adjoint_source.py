# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
adjoint_source.py — Generate adjoint sources for RTM backward simulation.

Per ogni ricevitore r e direzione c in {x, y, z}, calcola la sorgente
aggiunta time-reversed (slide 14, ST7_Reverse_Time_Migration_SEM3D.pdf):

    s_{r,c}(t) = u_sim_{r,c}(T-t) - d_obs_{r,c}(T-t)

e produce:
  - <out_dir>/misfit_{r}_{c}.txt  : file due colonne [t, s(t)] per SEM3D
  - <out_dir>/input_backward.spec : input SEM3D con N_r×3 blocchi source

Usage:
    python3 adjoint_source.py                                        \\
        @@capteurs_fwd  prot/Protection_00000001/Capteurs            \\
        @@capteurs_obs  /path/to/dobs/Capteurs                       \\
        @@input_spec    SEM3D_ST7_project2026_todo/input.spec        \\
        @@out_dir       adjoint_sources/                             \\
        @@monitor_name  Uobs

    @@capteurs_fwd  : cartella Capteurs del forward corrente
    @@capteurs_obs  : cartella Capteurs di d_obs (tutorial2)
    @@input_spec    : percorso dell'input.spec forward (template)
    @@out_dir       : cartella di output per i file misfit e backward.spec
    @@monitor_name  : nome del monitor in input.spec (default: Uobs)
"""

import argparse
import glob
import os
from os.path import join as osj

import numpy as np
from scipy.interpolate import interp1d
import h5py


# ── Costanti ──────────────────────────────────────────────────────────────────

DIRS  = ['x', 'y', 'z']                         # direzioni
DVECS = {'x': '1 0 0', 'y': '0 1 0', 'z': '0 0 1'}  # vettori direzione SEM3D


# ── Lettura file capteurs HDF5 ────────────────────────────────────────────────

def _parse_variables(h5file):
    """
    Legge il dataset 'Variables' da un file capteurs.h5 e restituisce
    un dizionario  (varname, component) -> indice di colonna (1-based, dopo il tempo).

    Esempio di riga nel dataset Variables: b"Displ x 1"
    → ('Displ', 'x') : 1  (colonna 1 del dataset dati, colonna 0 e' il tempo)
    """
    col_map = {}
    for entry in h5file['Variables'][...]:
        parts = entry.decode('utf-8').split()
        if len(parts) == 3:
            varname, component, col = parts[0], parts[1], int(parts[2])
        elif len(parts) == 2:
            varname, col = parts[0], int(parts[1])
            component = 'p'
        else:
            continue
        col_map[(varname, component)] = col  # 1-based
    return col_map


def read_capteurs(capteurs_dir, monitor_name='Uobs'):
    """
    Legge gli spostamenti (Displ x, y, z) da tutti i file capteurs.*.h5
    in capteurs_dir per il monitor chiamato monitor_name.

    Returns
    -------
    time      : np.ndarray  shape (nt,)
    positions : np.ndarray  shape (n_recv, 3)   coordinate (x,y,z) di ogni ricevitore
    displ     : np.ndarray  shape (nt, 3, n_recv)  spostamento [x,y,z] per ogni ricevitore
    recv_ids  : list[int]   indici dei ricevitori nell'ordine in cui appaiono in positions/displ
    """
    h5_files = sorted(glob.glob(osj(capteurs_dir, '*.h5')))
    if not h5_files:
        raise FileNotFoundError(f"Nessun file .h5 trovato in: {capteurs_dir}")

    # ── Primo passaggio: raccolta indici ricevitori, posizioni e asse temporale
    pos_dict  = {}   # recv_idx -> np.array shape (3,)
    time_arr  = None
    col_displ = None  # colonne (1-based) per Displ x/y/z

    for fpath in h5_files:
        with h5py.File(fpath, 'r') as f:
            # Mappa variabili → colonne (solo dal primo file)
            if col_displ is None and 'Variables' in f:
                col_map = _parse_variables(f)
                col_displ = [col_map.get(('Displ', c), None) for c in DIRS]
                if any(ci is None for ci in col_displ):
                    raise RuntimeError(
                        f"Variabile 'Displ' non trovata in Variables di {fpath}. "
                        f"Chiavi disponibili: {list(col_map.keys())}"
                    )

            for key in f.keys():
                if key == 'Variables':
                    continue

                if '_pos' in key and monitor_name in key:
                    # Dataset posizione: {monitor_name}_{recv_idx}_pos
                    parts = key.replace('_pos', '').split('_')
                    recv_idx = int(parts[-1]) if parts[-1].isdigit() else 0
                    pos_dict[recv_idx] = f[key][...].ravel()[:3]  # (3,)

                elif '_pos' not in key and monitor_name in key:
                    # Dataset dati: {monitor_name}_{recv_idx}
                    data = f[key][...]  # shape (nt, nvar+1)
                    if data.shape[0] >= 300 and time_arr is None:
                        time_arr = data[:, 0]

    if not pos_dict:
        raise RuntimeError(
            f"Nessun ricevitore trovato per monitor '{monitor_name}' in {capteurs_dir}"
        )
    if time_arr is None:
        raise RuntimeError(f"Asse temporale non trovato in {capteurs_dir}")

    # ── Costruzione arrays ordinati
    sorted_ids = sorted(pos_dict.keys())
    n_recv     = len(sorted_ids)
    nt         = len(time_arr)
    positions  = np.array([pos_dict[i] for i in sorted_ids])       # (n_recv, 3)
    displ      = np.zeros((nt, 3, n_recv), dtype=np.float64)       # (nt, 3, n_recv)
    id_to_local = {rid: li for li, rid in enumerate(sorted_ids)}

    # ── Secondo passaggio: lettura spostamenti
    for fpath in h5_files:
        with h5py.File(fpath, 'r') as f:
            for key in f.keys():
                if key == 'Variables' or '_pos' in key or monitor_name not in key:
                    continue
                data = f[key][...]
                if data.shape[0] < 300:
                    continue
                parts    = key.split('_')
                recv_idx = int(parts[-1]) if parts[-1].isdigit() else 0
                if recv_idx not in id_to_local:
                    continue
                lr = id_to_local[recv_idx]
                for ci, col in enumerate(col_displ):
                    displ[:, ci, lr] = data[:, col]  # col e' 1-based → colonna corretta

    return time_arr, positions, displ, sorted_ids


# ── Calcolo residui e time-reversal ──────────────────────────────────────────

def compute_adjoint_sources(time_fwd, displ_fwd, pos_fwd,
                             time_obs, displ_obs, pos_obs):
    """
    Calcola s_{r,c}(t) = u_sim_{r,c}(T-t) - d_obs_{r,c}(T-t)
    per ogni ricevitore r e direzione c.

    I ricevitori di fwd e obs vengono abbinati per posizione (distanza minima).
    Se le griglie temporali differiscono, d_obs viene interpolato su time_fwd.

    Returns
    -------
    time_rev : np.ndarray  shape (nt,)       asse temporale (uguale a time_fwd)
    sources  : np.ndarray  shape (nt, 3, n_recv)  sorgenti aggiunte
    """
    n_recv = displ_fwd.shape[2]
    nt     = len(time_fwd)

    # Abbina ricevitori fwd ↔ obs per posizione più vicina
    match = []
    for r in range(n_recv):
        dists   = np.linalg.norm(pos_obs - pos_fwd[r], axis=1)
        r_match = int(np.argmin(dists))
        if dists[r_match] > 1.0:  # tolleranza 1 metro
            print(f"  Attenzione: ricevitore {r} a distanza {dists[r_match]:.2f} m dal più vicino in d_obs")
        match.append(r_match)

    # Interpola d_obs su time_fwd se necessario
    if not np.allclose(time_fwd, time_obs, atol=1e-9):
        print("  Interpolazione d_obs sulla griglia temporale del forward...")
        displ_obs_interp = np.zeros_like(displ_fwd)
        for c in range(3):
            for r in range(n_recv):
                r_obs = match[r]
                interp_fn = interp1d(time_obs, displ_obs[:, c, r_obs],
                                     kind='linear', bounds_error=False, fill_value=0.0)
                displ_obs_interp[:, c, r] = interp_fn(time_fwd)
    else:
        displ_obs_interp = displ_obs[:, :, [match[r] for r in range(n_recv)]]

    # Residuo: r(t) = u_sim(t) - d_obs(t)
    residual = displ_fwd - displ_obs_interp   # (nt, 3, n_recv)

    # Time-reversal: s(t) = r(T-t) → flip asse temporale
    # Il primo valore di s corrisponde a r(T), l'ultimo a r(0)
    sources = residual[::-1, :, :].copy()     # (nt, 3, n_recv)

    return time_fwd, sources


# ── Scrittura file misfit_{r}_{c}.txt ────────────────────────────────────────

def write_misfit_files(time_rev, sources, out_dir):
    """
    Scrive un file misfit_{r}_{c}.txt per ogni (ricevitore r, direzione c).
    Formato: due colonne [t  s(t)], stesso formato di gaussian_stf.txt.

    Returns
    -------
    file_names : dict  (r, c) -> nome del file (senza percorso)
    """
    os.makedirs(out_dir, exist_ok=True)
    n_recv = sources.shape[2]
    file_names = {}

    for r in range(n_recv):
        for ci, cname in enumerate(DIRS):
            fname = f"misfit_{r}_{cname}.txt"
            fpath = osj(out_dir, fname)
            data  = np.column_stack([time_rev, sources[:, ci, r]])
            np.savetxt(fpath, data, fmt='%.15f')
            file_names[(r, cname)] = fname

    print(f"  Scritti {n_recv * 3} file misfit in {out_dir}/")
    return file_names


# ── Generazione input_backward.spec ──────────────────────────────────────────

def _strip_source_and_capteurs(spec_text):
    """
    Rimuove tutti i blocchi source { ... } e capteurs { ... } dall'input.spec.
    Restituisce il testo pulito.
    """
    lines  = spec_text.splitlines(keepends=True)
    result = []
    depth  = 0
    inside_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Individua inizio di un blocco source o capteurs
        if not inside_block:
            if (stripped.startswith('source') or stripped.startswith('capteurs')) \
                    and '{' in stripped:
                inside_block = True
                depth = stripped.count('{') - stripped.count('}')
                if depth <= 0:
                    inside_block = False
                i += 1
                continue
            elif (stripped.startswith('source') or stripped.startswith('capteurs')) \
                    and i + 1 < len(lines) and '{' in lines[i + 1]:
                inside_block = True
                depth = lines[i + 1].count('{') - lines[i + 1].count('}')
                if depth <= 0:
                    inside_block = False
                i += 2
                continue
        else:
            depth += stripped.count('{') - stripped.count('}')
            if depth <= 0:
                inside_block = False
            i += 1
            continue

        result.append(line)
        i += 1

    return ''.join(result)


def _disable_gradla_gradmu(spec_text):
    """
    Imposta gradla=0 e gradmu=0 nell'input backward (non servono nell'adjoint).
    """
    spec_text = spec_text.replace('gradla = 1', 'gradla = 0')
    spec_text = spec_text.replace('gradmu = 1', 'gradmu = 0')
    return spec_text


def write_backward_spec(positions, file_names, input_spec_path, out_dir, misfit_rel_path=''):
    """
    Genera input_backward.spec copiando input_spec_path e:
    - Rimuove il blocco source originale e il blocco capteurs
    - Aggiunge N_r × 3 blocchi source (uno per ricevitore per direzione)
    - Disabilita gradla/gradmu (non necessari nell'adjoint)
    - Mantiene evol=1 e edev=1 (necessari per gradient_compute.py)

    Parameters
    ----------
    positions       : np.ndarray  shape (n_recv, 3)
    file_names      : dict  (r, c) -> nome file misfit
    input_spec_path : str   percorso dell'input.spec del forward
    out_dir         : str   cartella di output
    misfit_rel_path : str   prefisso relativo da aggiungere ai nomi dei file misfit
                            (es. "adjoint_sources/" se i file sono in una sottocartella)
    """
    with open(input_spec_path, 'r') as f:
        spec_text = f.read()

    # Rimuovi sorgente forward e capteurs, disabilita gradla/gradmu
    spec_text = _strip_source_and_capteurs(spec_text)
    spec_text = _disable_gradla_gradmu(spec_text)

    # Costruisci i blocchi source adjoint
    n_recv = len(positions)
    source_blocks = []
    for r in range(n_recv):
        x, y, z = positions[r]
        for cname in DIRS:
            fname    = file_names[(r, cname)]
            rel_path = osj(misfit_rel_path, fname).replace('\\', '/') if misfit_rel_path else fname
            block = (
                f"source {{\n"
                f"    coords = {x:.6f} {y:.6f} {z:.6f};\n"
                f"    type   = impulse;\n"
                f"    dir    = {DVECS[cname]};\n"
                f"    func   = file;\n"
                f"    time_file = \"{rel_path}\";\n"
                f"    amplitude = 1.0;\n"
                f"}};\n"
            )
            source_blocks.append(block)

    sources_text = '\n'.join(source_blocks)
    backward_spec = spec_text.rstrip() + '\n\n# Sorgenti aggiunte (adjoint)\n' + sources_text + '\n'

    out_path = osj(out_dir, 'input_backward.spec')
    with open(out_path, 'w') as f:
        f.write(backward_spec)

    print(f"  input_backward.spec scritto in {out_path}")
    print(f"  Totale blocchi source: {n_recv * 3}  ({n_recv} ricevitori × 3 direzioni)")
    return out_path


# ── CLI ──────────────────────────────────────────────────────────────────────

def _parse_cl():
    parser = argparse.ArgumentParser(prefix_chars='@')
    parser.add_argument('@@capteurs_fwd',  type=str, required=True,
                        help="Cartella Capteurs del forward corrente")
    parser.add_argument('@@capteurs_obs',  type=str, required=True,
                        help="Cartella Capteurs di d_obs (es. tutorial2)")
    parser.add_argument('@@input_spec',    type=str, required=True,
                        help="Percorso dell'input.spec forward (template)")
    parser.add_argument('@@out_dir',       type=str, default='adjoint_sources',
                        help="Cartella output per file misfit e backward.spec")
    parser.add_argument('@@monitor_name',  type=str, default='Uobs',
                        help="Nome del monitor in input.spec (default: Uobs)")
    return parser.parse_args().__dict__


def main():
    opt = _parse_cl()

    print(f"[adjoint_source] Lettura forward: {opt['capteurs_fwd']}")
    time_fwd, pos_fwd, displ_fwd, _ = read_capteurs(opt['capteurs_fwd'], opt['monitor_name'])
    print(f"  Ricevitori: {pos_fwd.shape[0]}  |  Timestep: {len(time_fwd)}  |  T = {time_fwd[-1]:.3f} s")

    print(f"[adjoint_source] Lettura d_obs:   {opt['capteurs_obs']}")
    time_obs, pos_obs, displ_obs, _ = read_capteurs(opt['capteurs_obs'], opt['monitor_name'])
    print(f"  Ricevitori: {pos_obs.shape[0]}  |  Timestep: {len(time_obs)}  |  T = {time_obs[-1]:.3f} s")

    print("[adjoint_source] Calcolo residui e time-reversal...")
    time_rev, sources = compute_adjoint_sources(
        time_fwd, displ_fwd, pos_fwd,
        time_obs, displ_obs, pos_obs
    )
    print(f"  Norma residuo (dir x, recv 0): {np.linalg.norm(sources[:, 0, 0]):.4e}")

    print("[adjoint_source] Scrittura file misfit...")
    file_names = write_misfit_files(time_rev, sources, opt['out_dir'])

    print("[adjoint_source] Generazione input_backward.spec...")
    write_backward_spec(
        positions       = pos_fwd,
        file_names      = file_names,
        input_spec_path = opt['input_spec'],
        out_dir         = opt['out_dir'],
        misfit_rel_path = '',
    )

    print("\n[adjoint_source] Completato.")
    print(f"  Prossimo passo: copiare input_backward.spec e i file misfit nella")
    print(f"  cartella di simulazione SEM3D, poi lanciare SEM3D con input_backward.spec")


if __name__ == '__main__':
    main()
