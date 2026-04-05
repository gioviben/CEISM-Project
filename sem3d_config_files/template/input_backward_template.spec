# -*- mode: perl -*-
run_name = "adjoint_run";

sim_time = 2.0;
mesh_file = "mesh4spec";
mat_file = "material.input";
dim = 3;
ngll = 5;

snapshots {
    save_snap = true;
    snap_interval = 0.02;
    select material = 0;
};

save_traces = false;
traces_format = hdf5;

prorep = false;
prorep_iter = 1000;

# ADJOINT_SOURCES_PLACEHOLDER

time_scheme {
    accel_scheme = false;
    veloc_scheme = true;
    alpha = 0.5;
    beta = 0.5;
    gamma = 1;
    courant = 0.2;
};

out_variables {
    evol = 1;
    dis  = 1;
    vel  = 1;
    acc  = 1;
    edev = 1;
};