import numpy as np
from scipy.interpolate import interp1d
from pysem.parse_sem3d_traces import ParseSEM3DH5Traces

def compute_misfit(TRACES_SIMULATED_FOLDER_PATH, obs_monitor):
    """
    Compute the L2 misfit between simulated and observed displacement traces.

    The observed traces are interpolated onto the simulated time grid before
    computing the residual.

    Parameters
    ----------
    TRACES_SIMULATED_FOLDER_PATH : str
        Path to the folder containing simulated SEM3D trace .h5 files.
    obs_monitor : SEM3DMonitor
        Observed monitor object, typically obtained with:
            obs_monitor = obs_stream['Uobs']

    Returns
    -------
    J : float
        Misfit value:
            J = 0.5 * sum(residual^2) * dt_sim
    """

    # -----------------------------
    # Extract observed data ( + checks )
    # -----------------------------
    if not hasattr(obs_monitor, "data") or "Displ" not in obs_monitor.data:
        raise ValueError("obs_monitor does not contain 'Displ' data")

    if not hasattr(obs_monitor, "Time"):
        raise ValueError("obs_monitor does not contain a valid time vector")

    obs_u = np.asarray(obs_monitor.data["Displ"], dtype=np.float64)
    t_obs = np.asarray(obs_monitor.Time, dtype=np.float64)

    if obs_u.ndim != 3:
        raise ValueError(
            f"Observed displacement tensor must have shape (Nt_obs, 3, Nr), got {obs_u.shape}"
        )

    if obs_u.shape[1] != 3:
        raise ValueError(
            f"Observed displacement tensor must have 3 components along axis 1, got {obs_u.shape}"
        )

    if t_obs.ndim != 1:
        raise ValueError(f"Observed time vector must be 1D, got {t_obs.shape}")

    if obs_u.shape[0] != t_obs.shape[0]:
        raise ValueError(
            f"Inconsistent observed data: obs_u.shape[0]={obs_u.shape[0]} "
            f"but t_obs.shape[0]={t_obs.shape[0]}"
        )

    if t_obs.size < 2:
        raise ValueError("Observed time vector must contain at least two samples")

    if not np.all(np.isfinite(obs_u)):
        raise ValueError("Observed displacement tensor contains NaN or inf values")

    if not np.all(np.isfinite(t_obs)):
        raise ValueError("Observed time vector contains NaN or inf values")

    if not np.all(np.diff(t_obs) > 0):
        raise ValueError("Observed time vector must be strictly increasing")

    # -----------------------------
    # Parse simulated traces ( + checks )
    # -----------------------------

    sim_stream = ParseSEM3DH5Traces(                #4683*3*121
        wkdir=TRACES_SIMULATED_FOLDER_PATH,
        format='h5',
        names=['Uobs'],
        variables=['Displ'],
        components=['x', 'y', 'z']
    )

    if "Uobs" not in sim_stream:
        raise RuntimeError("No 'Uobs' monitor set found in simulated traces")

    sim_monitor = sim_stream["Uobs"]

    if not hasattr(sim_monitor, "data") or "Displ" not in sim_monitor.data:
        raise RuntimeError("Simulated monitor does not contain 'Displ' data")

    if not hasattr(sim_monitor, "Time"):
        raise RuntimeError("Simulated monitor does not contain a valid time vector")

    if not hasattr(sim_monitor, "dTime"):
        raise RuntimeError("Simulated monitor does not contain 'dTime'")

    sim_u = np.asarray(sim_monitor.data["Displ"], dtype=np.float64)
    t_sim = np.asarray(sim_monitor.Time, dtype=np.float64)
    dt_sim = float(sim_monitor.dTime)

    if sim_u.ndim != 3:
        raise RuntimeError(
            f"Simulated displacement tensor must have shape (Nt_sim, 3, Nr), got {sim_u.shape}"
        )

    if sim_u.shape[1] != 3:
        raise RuntimeError(
            f"Simulated displacement tensor must have 3 components along axis 1, got {sim_u.shape}"
        )

    if t_sim.ndim != 1:
        raise RuntimeError(f"Simulated time vector must be 1D, got {t_sim.shape}")

    if sim_u.shape[0] != t_sim.shape[0]:
        raise RuntimeError(
            f"Inconsistent simulated data: sim_u.shape[0]={sim_u.shape[0]} "
            f"but t_sim.shape[0]={t_sim.shape[0]}"
        )

    if t_sim.size < 2:
        raise RuntimeError("Simulated time vector must contain at least two samples")

    if not np.all(np.isfinite(sim_u)):
        raise RuntimeError("Simulated displacement tensor contains NaN or inf values")

    if not np.all(np.isfinite(t_sim)):
        raise RuntimeError("Simulated time vector contains NaN or inf values")

    if not np.all(np.diff(t_sim) > 0):
        raise RuntimeError("Simulated time vector must be strictly increasing")

    if dt_sim <= 0.0:
        raise RuntimeError(f"Invalid simulated time step: dt_sim = {dt_sim}")

    # -----------------------------
    # Compatibility checks
    # -----------------------------
    if sim_u.shape[2] != obs_u.shape[2]:
        raise ValueError(
            f"Different number of stations: simulated has {sim_u.shape[2]}, "
            f"observed has {obs_u.shape[2]}"
        )

    ''' TODO check
    # Better to fail than silently inject zeros outside time support
    if t_sim[0] < t_obs[0] or t_sim[-1] > t_obs[-1]:
        raise ValueError(
            "Simulated time range lies outside observed time range. "
            "Interpolation with zero padding would bias the misfit."
        )
    '''

    # -----------------------------
    # Interpolate observed data
    # onto simulated time grid
    # -----------------------------
    
    interp_obs = interp1d(
        t_obs,
        obs_u,
        axis=0,
        kind="linear",
        bounds_error=False,
        fill_value=0.0,
        assume_sorted=True
    )
    
    obs_u_interp = interp_obs(t_sim)

    # -----------------------------
    # Residual and misfit
    # -----------------------------
    residual = sim_u - obs_u_interp
    J = 0.5 * np.sum(residual ** 2) * dt_sim

    return J, residual, t_sim, dt_sim


