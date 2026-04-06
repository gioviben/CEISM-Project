# -*- mode: perl -*-
run_name = "Test_name";

# duration of the run
sim_time = 10.0;
mesh_file = "mesh4spec"; # input mesh file
mat_file = "material.input";
dim=3;
fmax=0.1;
ngll=5;

snapshots {
    save_snap = true;
    snap_interval = 1.0; # in seconds
    select box = -1200.0 -1200.0 -10.0 1200.0 1200.0 1.0;  
};

# Mpml attenuation
mpml_atn_param = 0.02;

# Monitor structure
save_traces   = true;
traces_format = hdf5;
#traces_format = text;

capteurs "Uobs" {
    type   = points;
    file   = "stations.txt";
    period = 68; # number of iterations
};

# Fichier protection reprise
prorep=false;
prorep_iter=200000;
restart_iter=0;

# ADJOINT_SOURCES_PLACEHOLDER

time_scheme {
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta =  0.5;           # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
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

