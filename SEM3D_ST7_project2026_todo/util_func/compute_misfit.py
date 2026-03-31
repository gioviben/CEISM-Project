import numpy as np
from pysem import ParseSEM3DH5Traces

def compute_misfit(TRACES_SIMULATED_FOLDER_PATH, obs_u):

    sim_stream = ParseSEM3DH5Traces(                #4683*3*121
        wkdir=TRACES_SIMULATED_FOLDER_PATH,
        format='h5',
        names=['Uobs'],
        variables=['Displ'],
        components=['x', 'y', 'z']
    )
    sim_monitor = sim_stream['Uobs']
    sim_u = sim_monitor.data['Displ']
    residual = sim_u - obs_u                        #(time, n_components, stations)
    J = 0.5 * np.sum(residual**2)
    return J