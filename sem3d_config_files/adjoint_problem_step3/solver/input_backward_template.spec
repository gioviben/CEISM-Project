# -*- mode: perl -*-
run_name = "adjoint_run";

sim_time = 10.0;
mesh_file = "mesh4spec";
mat_file = "material.input";
dim=3;
#fmax=0.1
ngll=5;

snapshots {
    save_snap = true;
    snap_interval = 0.5;
    select box = -1200.0 -1200.0 -10.0 1200.0 1200.0 1.0;
    #select material = 0;
};

save_traces = false;
traces_format = hdf5;

prorep=false;
prorep_iter=1000;

# ADJOINT_SOURCES_PLACEHOLDER

time_scheme {
    accel_scheme = false;
    veloc_scheme = true;
    alpha = 0.5;
    beta = 0.5;
    gamma = 1;
    courant=0.2;
};

pml_infos {
pml_type = CPML;
cpml_kappa0 = 10.0;
cpml_kappa1 = 10.0;
cpml_rc = 0.000000001;
cpml_integration = Order2;
};

# output fields to be saved
out_variables {
    enP  = 0;   # P-wave energy (scalar field)
    enS  = 0;   # S-wave energy (scalar field)
    evol = 1;   # volumetric strain (scalar field)
    pre  = 0;   # pressure (scalar field)
    dis  = 1;   # displacement (vector field)
    vel  = 1;   # velocity (vector field)
    acc  = 1;   # acceleration (vector field)
    edev = 1;   # deviatoric strain (tensor field)
    sdev = 0;   # deviatoric stress (tensor field)
    edevpl = 0; # deviatoric strain (tensor field)
    gradla = 1; # gradient Lambda (for regularizer)
    gradmu = 1; # gradient Mu (for regularizer)
};