import numpy as np
import os

def write_time_reversed_residual_files(time_reversed_residual, t_sim, OUTPUT_DIR):
    """
    Write one adjoint source file per receiver and per component.

    Parameters
    ----------
    residual : np.ndarray
        Tensor with shape (Nt, 3, Nr)
    t_sim : np.ndarray
        Time vector with shape (Nt,)
    OUTPUT_DIR : str
        Output directory where misfit files will be written

    Returns
    -------
    file_names : dict
        Mapping (receiver_index, component_name) -> file name
    """

    time_reversed_residual = np.asarray(time_reversed_residual, dtype=np.float64)
    t_sim = np.asarray(t_sim, dtype=np.float64)

    #--------------
    # Basic Checks
    #--------------
    if time_reversed_residual.ndim != 3:
        raise ValueError(f"time reversed residual must have shape (Nt, 3, Nr), got {time_reversed_residual.shape}")

    if time_reversed_residual.shape[1] != 3:
        raise ValueError(f"time reversed residual second axis must have size 3, got {time_reversed_residual.shape}")

    if t_sim.ndim != 1:
        raise ValueError(f"t_sim must be 1D, got {t_sim.shape}")

    if time_reversed_residual.shape[0] != t_sim.shape[0]:
        raise ValueError(
            f"Inconsistent shapes: time reversed residual has Nt={time_reversed_residual.shape[0]}, "
            f"but t_sim has length {t_sim.shape[0]}"
        )

    if not np.all(np.isfinite(time_reversed_residual)):
        raise ValueError("time reversed residual contains NaN or inf values")

    if not np.all(np.isfinite(t_sim)):
        raise ValueError("t_sim contains NaN or inf values")

    #--------------

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    components = ["x", "y", "z"]
    n_receivers = time_reversed_residual.shape[2]
    n_direction = time_reversed_residual.shape[1]
    file_names = {}

    for receiver in range(n_receivers):
        for direction in range(n_direction):
            current_source = time_reversed_residual[:, direction, receiver]
            
            file_name = f"misfit_{receiver}_{components[direction]}.txt"
            file_path = os.path.join(OUTPUT_DIR, file_name)

            to_write = np.column_stack((t_sim, current_source))
            np.savetxt(file_path, to_write, fmt="%.15e")
            
            file_names[(receiver, components[direction])] = file_name

    return file_names