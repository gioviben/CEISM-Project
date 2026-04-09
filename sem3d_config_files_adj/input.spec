# -*- mode: perl -*-
run_name = "Test_name";

# duration of the run
sim_time = 5.0;
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
    file = "stations.txt";
    period = 68; # number of iterations
};

# Fichier protection reprise
prorep=false;
prorep_iter=200000;
restart_iter=0;

source {
    coords = -17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_0_x.txt";
};

source {
    coords = -17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_0_y.txt";
};

source {
    coords = -17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_0_z.txt";
};

source {
    coords = -17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_1_x.txt";
};

source {
    coords = -17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_1_y.txt";
};

source {
    coords = -17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_1_z.txt";
};

source {
    coords = -17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_2_x.txt";
};

source {
    coords = -17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_2_y.txt";
};

source {
    coords = -17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_2_z.txt";
};

source {
    coords = -17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_3_x.txt";
};

source {
    coords = -17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_3_y.txt";
};

source {
    coords = -17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_3_z.txt";
};

source {
    coords = -17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_4_x.txt";
};

source {
    coords = -17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_4_y.txt";
};

source {
    coords = -17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_4_z.txt";
};

source {
    coords = -17.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_5_x.txt";
};

source {
    coords = -17.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_5_y.txt";
};

source {
    coords = -17.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_5_z.txt";
};

source {
    coords = -17.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_6_x.txt";
};

source {
    coords = -17.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_6_y.txt";
};

source {
    coords = -17.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_6_z.txt";
};

source {
    coords = -17.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_7_x.txt";
};

source {
    coords = -17.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_7_y.txt";
};

source {
    coords = -17.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_7_z.txt";
};

source {
    coords = -17.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_8_x.txt";
};

source {
    coords = -17.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_8_y.txt";
};

source {
    coords = -17.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_8_z.txt";
};

source {
    coords = -17.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_9_x.txt";
};

source {
    coords = -17.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_9_y.txt";
};

source {
    coords = -17.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_9_z.txt";
};

source {
    coords = -17.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_10_x.txt";
};

source {
    coords = -17.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_10_y.txt";
};

source {
    coords = -17.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_10_z.txt";
};

source {
    coords = -14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_11_x.txt";
};

source {
    coords = -14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_11_y.txt";
};

source {
    coords = -14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_11_z.txt";
};

source {
    coords = -14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_12_x.txt";
};

source {
    coords = -14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_12_y.txt";
};

source {
    coords = -14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_12_z.txt";
};

source {
    coords = -14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_13_x.txt";
};

source {
    coords = -14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_13_y.txt";
};

source {
    coords = -14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_13_z.txt";
};

source {
    coords = -14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_14_x.txt";
};

source {
    coords = -14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_14_y.txt";
};

source {
    coords = -14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_14_z.txt";
};

source {
    coords = -14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_15_x.txt";
};

source {
    coords = -14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_15_y.txt";
};

source {
    coords = -14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_15_z.txt";
};

source {
    coords = -14.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_16_x.txt";
};

source {
    coords = -14.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_16_y.txt";
};

source {
    coords = -14.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_16_z.txt";
};

source {
    coords = -14.000000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_17_x.txt";
};

source {
    coords = -14.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_17_y.txt";
};

source {
    coords = -14.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_17_z.txt";
};

source {
    coords = -14.000000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_18_x.txt";
};

source {
    coords = -14.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_18_y.txt";
};

source {
    coords = -14.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_18_z.txt";
};

source {
    coords = -14.000000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_19_x.txt";
};

source {
    coords = -14.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_19_y.txt";
};

source {
    coords = -14.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_19_z.txt";
};

source {
    coords = -14.000000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_20_x.txt";
};

source {
    coords = -14.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_20_y.txt";
};

source {
    coords = -14.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_20_z.txt";
};

source {
    coords = -14.000000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_21_x.txt";
};

source {
    coords = -14.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_21_y.txt";
};

source {
    coords = -14.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_21_z.txt";
};

source {
    coords = -10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_22_x.txt";
};

source {
    coords = -10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_22_y.txt";
};

source {
    coords = -10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_22_z.txt";
};

source {
    coords = -10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_23_x.txt";
};

source {
    coords = -10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_23_y.txt";
};

source {
    coords = -10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_23_z.txt";
};

source {
    coords = -10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_24_x.txt";
};

source {
    coords = -10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_24_y.txt";
};

source {
    coords = -10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_24_z.txt";
};

source {
    coords = -10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_25_x.txt";
};

source {
    coords = -10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_25_y.txt";
};

source {
    coords = -10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_25_z.txt";
};

source {
    coords = -10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_26_x.txt";
};

source {
    coords = -10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_26_y.txt";
};

source {
    coords = -10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_26_z.txt";
};

source {
    coords = -10.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_27_x.txt";
};

source {
    coords = -10.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_27_y.txt";
};

source {
    coords = -10.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_27_z.txt";
};

source {
    coords = -10.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_28_x.txt";
};

source {
    coords = -10.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_28_y.txt";
};

source {
    coords = -10.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_28_z.txt";
};

source {
    coords = -10.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_29_x.txt";
};

source {
    coords = -10.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_29_y.txt";
};

source {
    coords = -10.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_29_z.txt";
};

source {
    coords = -10.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_30_x.txt";
};

source {
    coords = -10.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_30_y.txt";
};

source {
    coords = -10.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_30_z.txt";
};

source {
    coords = -10.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_31_x.txt";
};

source {
    coords = -10.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_31_y.txt";
};

source {
    coords = -10.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_31_z.txt";
};

source {
    coords = -10.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_32_x.txt";
};

source {
    coords = -10.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_32_y.txt";
};

source {
    coords = -10.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_32_z.txt";
};

source {
    coords = -7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_33_x.txt";
};

source {
    coords = -7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_33_y.txt";
};

source {
    coords = -7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_33_z.txt";
};

source {
    coords = -7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_34_x.txt";
};

source {
    coords = -7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_34_y.txt";
};

source {
    coords = -7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_34_z.txt";
};

source {
    coords = -7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_35_x.txt";
};

source {
    coords = -7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_35_y.txt";
};

source {
    coords = -7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_35_z.txt";
};

source {
    coords = -7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_36_x.txt";
};

source {
    coords = -7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_36_y.txt";
};

source {
    coords = -7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_36_z.txt";
};

source {
    coords = -7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_37_x.txt";
};

source {
    coords = -7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_37_y.txt";
};

source {
    coords = -7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_37_z.txt";
};

source {
    coords = -7.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_38_x.txt";
};

source {
    coords = -7.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_38_y.txt";
};

source {
    coords = -7.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_38_z.txt";
};

source {
    coords = -7.000000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_39_x.txt";
};

source {
    coords = -7.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_39_y.txt";
};

source {
    coords = -7.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_39_z.txt";
};

source {
    coords = -7.000000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_40_x.txt";
};

source {
    coords = -7.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_40_y.txt";
};

source {
    coords = -7.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_40_z.txt";
};

source {
    coords = -7.000000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_41_x.txt";
};

source {
    coords = -7.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_41_y.txt";
};

source {
    coords = -7.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_41_z.txt";
};

source {
    coords = -7.000000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_42_x.txt";
};

source {
    coords = -7.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_42_y.txt";
};

source {
    coords = -7.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_42_z.txt";
};

source {
    coords = -7.000000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_43_x.txt";
};

source {
    coords = -7.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_43_y.txt";
};

source {
    coords = -7.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_43_z.txt";
};

source {
    coords = -3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_44_x.txt";
};

source {
    coords = -3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_44_y.txt";
};

source {
    coords = -3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_44_z.txt";
};

source {
    coords = -3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_45_x.txt";
};

source {
    coords = -3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_45_y.txt";
};

source {
    coords = -3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_45_z.txt";
};

source {
    coords = -3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_46_x.txt";
};

source {
    coords = -3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_46_y.txt";
};

source {
    coords = -3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_46_z.txt";
};

source {
    coords = -3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_47_x.txt";
};

source {
    coords = -3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_47_y.txt";
};

source {
    coords = -3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_47_z.txt";
};

source {
    coords = -3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_48_x.txt";
};

source {
    coords = -3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_48_y.txt";
};

source {
    coords = -3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_48_z.txt";
};

source {
    coords = -3.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_49_x.txt";
};

source {
    coords = -3.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_49_y.txt";
};

source {
    coords = -3.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_49_z.txt";
};

source {
    coords = -3.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_50_x.txt";
};

source {
    coords = -3.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_50_y.txt";
};

source {
    coords = -3.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_50_z.txt";
};

source {
    coords = -3.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_51_x.txt";
};

source {
    coords = -3.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_51_y.txt";
};

source {
    coords = -3.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_51_z.txt";
};

source {
    coords = -3.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_52_x.txt";
};

source {
    coords = -3.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_52_y.txt";
};

source {
    coords = -3.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_52_z.txt";
};

source {
    coords = -3.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_53_x.txt";
};

source {
    coords = -3.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_53_y.txt";
};

source {
    coords = -3.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_53_z.txt";
};

source {
    coords = -3.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_54_x.txt";
};

source {
    coords = -3.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_54_y.txt";
};

source {
    coords = -3.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_54_z.txt";
};

source {
    coords = 0.000000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_55_x.txt";
};

source {
    coords = 0.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_55_y.txt";
};

source {
    coords = 0.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_55_z.txt";
};

source {
    coords = 0.000000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_56_x.txt";
};

source {
    coords = 0.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_56_y.txt";
};

source {
    coords = 0.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_56_z.txt";
};

source {
    coords = 0.000000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_57_x.txt";
};

source {
    coords = 0.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_57_y.txt";
};

source {
    coords = 0.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_57_z.txt";
};

source {
    coords = 0.000000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_58_x.txt";
};

source {
    coords = 0.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_58_y.txt";
};

source {
    coords = 0.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_58_z.txt";
};

source {
    coords = 0.000000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_59_x.txt";
};

source {
    coords = 0.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_59_y.txt";
};

source {
    coords = 0.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_59_z.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_60_x.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_60_y.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_60_z.txt";
};

source {
    coords = 0.000000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_61_x.txt";
};

source {
    coords = 0.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_61_y.txt";
};

source {
    coords = 0.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_61_z.txt";
};

source {
    coords = 0.000000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_62_x.txt";
};

source {
    coords = 0.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_62_y.txt";
};

source {
    coords = 0.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_62_z.txt";
};

source {
    coords = 0.000000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_63_x.txt";
};

source {
    coords = 0.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_63_y.txt";
};

source {
    coords = 0.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_63_z.txt";
};

source {
    coords = 0.000000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_64_x.txt";
};

source {
    coords = 0.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_64_y.txt";
};

source {
    coords = 0.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_64_z.txt";
};

source {
    coords = 0.000000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_65_x.txt";
};

source {
    coords = 0.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_65_y.txt";
};

source {
    coords = 0.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_65_z.txt";
};

source {
    coords = 3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_66_x.txt";
};

source {
    coords = 3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_66_y.txt";
};

source {
    coords = 3.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_66_z.txt";
};

source {
    coords = 3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_67_x.txt";
};

source {
    coords = 3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_67_y.txt";
};

source {
    coords = 3.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_67_z.txt";
};

source {
    coords = 3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_68_x.txt";
};

source {
    coords = 3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_68_y.txt";
};

source {
    coords = 3.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_68_z.txt";
};

source {
    coords = 3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_69_x.txt";
};

source {
    coords = 3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_69_y.txt";
};

source {
    coords = 3.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_69_z.txt";
};

source {
    coords = 3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_70_x.txt";
};

source {
    coords = 3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_70_y.txt";
};

source {
    coords = 3.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_70_z.txt";
};

source {
    coords = 3.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_71_x.txt";
};

source {
    coords = 3.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_71_y.txt";
};

source {
    coords = 3.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_71_z.txt";
};

source {
    coords = 3.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_72_x.txt";
};

source {
    coords = 3.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_72_y.txt";
};

source {
    coords = 3.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_72_z.txt";
};

source {
    coords = 3.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_73_x.txt";
};

source {
    coords = 3.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_73_y.txt";
};

source {
    coords = 3.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_73_z.txt";
};

source {
    coords = 3.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_74_x.txt";
};

source {
    coords = 3.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_74_y.txt";
};

source {
    coords = 3.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_74_z.txt";
};

source {
    coords = 3.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_75_x.txt";
};

source {
    coords = 3.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_75_y.txt";
};

source {
    coords = 3.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_75_z.txt";
};

source {
    coords = 3.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_76_x.txt";
};

source {
    coords = 3.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_76_y.txt";
};

source {
    coords = 3.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_76_z.txt";
};

source {
    coords = 7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_77_x.txt";
};

source {
    coords = 7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_77_y.txt";
};

source {
    coords = 7.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_77_z.txt";
};

source {
    coords = 7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_78_x.txt";
};

source {
    coords = 7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_78_y.txt";
};

source {
    coords = 7.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_78_z.txt";
};

source {
    coords = 7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_79_x.txt";
};

source {
    coords = 7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_79_y.txt";
};

source {
    coords = 7.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_79_z.txt";
};

source {
    coords = 7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_80_x.txt";
};

source {
    coords = 7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_80_y.txt";
};

source {
    coords = 7.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_80_z.txt";
};

source {
    coords = 7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_81_x.txt";
};

source {
    coords = 7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_81_y.txt";
};

source {
    coords = 7.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_81_z.txt";
};

source {
    coords = 7.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_82_x.txt";
};

source {
    coords = 7.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_82_y.txt";
};

source {
    coords = 7.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_82_z.txt";
};

source {
    coords = 7.000000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_83_x.txt";
};

source {
    coords = 7.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_83_y.txt";
};

source {
    coords = 7.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_83_z.txt";
};

source {
    coords = 7.000000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_84_x.txt";
};

source {
    coords = 7.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_84_y.txt";
};

source {
    coords = 7.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_84_z.txt";
};

source {
    coords = 7.000000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_85_x.txt";
};

source {
    coords = 7.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_85_y.txt";
};

source {
    coords = 7.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_85_z.txt";
};

source {
    coords = 7.000000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_86_x.txt";
};

source {
    coords = 7.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_86_y.txt";
};

source {
    coords = 7.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_86_z.txt";
};

source {
    coords = 7.000000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_87_x.txt";
};

source {
    coords = 7.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_87_y.txt";
};

source {
    coords = 7.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_87_z.txt";
};

source {
    coords = 10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_88_x.txt";
};

source {
    coords = 10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_88_y.txt";
};

source {
    coords = 10.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_88_z.txt";
};

source {
    coords = 10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_89_x.txt";
};

source {
    coords = 10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_89_y.txt";
};

source {
    coords = 10.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_89_z.txt";
};

source {
    coords = 10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_90_x.txt";
};

source {
    coords = 10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_90_y.txt";
};

source {
    coords = 10.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_90_z.txt";
};

source {
    coords = 10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_91_x.txt";
};

source {
    coords = 10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_91_y.txt";
};

source {
    coords = 10.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_91_z.txt";
};

source {
    coords = 10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_92_x.txt";
};

source {
    coords = 10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_92_y.txt";
};

source {
    coords = 10.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_92_z.txt";
};

source {
    coords = 10.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_93_x.txt";
};

source {
    coords = 10.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_93_y.txt";
};

source {
    coords = 10.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_93_z.txt";
};

source {
    coords = 10.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_94_x.txt";
};

source {
    coords = 10.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_94_y.txt";
};

source {
    coords = 10.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_94_z.txt";
};

source {
    coords = 10.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_95_x.txt";
};

source {
    coords = 10.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_95_y.txt";
};

source {
    coords = 10.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_95_z.txt";
};

source {
    coords = 10.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_96_x.txt";
};

source {
    coords = 10.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_96_y.txt";
};

source {
    coords = 10.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_96_z.txt";
};

source {
    coords = 10.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_97_x.txt";
};

source {
    coords = 10.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_97_y.txt";
};

source {
    coords = 10.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_97_z.txt";
};

source {
    coords = 10.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_98_x.txt";
};

source {
    coords = 10.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_98_y.txt";
};

source {
    coords = 10.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_98_z.txt";
};

source {
    coords = 14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_99_x.txt";
};

source {
    coords = 14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_99_y.txt";
};

source {
    coords = 14.000000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_99_z.txt";
};

source {
    coords = 14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_100_x.txt";
};

source {
    coords = 14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_100_y.txt";
};

source {
    coords = 14.000000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_100_z.txt";
};

source {
    coords = 14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_101_x.txt";
};

source {
    coords = 14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_101_y.txt";
};

source {
    coords = 14.000000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_101_z.txt";
};

source {
    coords = 14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_102_x.txt";
};

source {
    coords = 14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_102_y.txt";
};

source {
    coords = 14.000000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_102_z.txt";
};

source {
    coords = 14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_103_x.txt";
};

source {
    coords = 14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_103_y.txt";
};

source {
    coords = 14.000000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_103_z.txt";
};

source {
    coords = 14.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_104_x.txt";
};

source {
    coords = 14.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_104_y.txt";
};

source {
    coords = 14.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_104_z.txt";
};

source {
    coords = 14.000000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_105_x.txt";
};

source {
    coords = 14.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_105_y.txt";
};

source {
    coords = 14.000000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_105_z.txt";
};

source {
    coords = 14.000000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_106_x.txt";
};

source {
    coords = 14.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_106_y.txt";
};

source {
    coords = 14.000000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_106_z.txt";
};

source {
    coords = 14.000000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_107_x.txt";
};

source {
    coords = 14.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_107_y.txt";
};

source {
    coords = 14.000000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_107_z.txt";
};

source {
    coords = 14.000000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_108_x.txt";
};

source {
    coords = 14.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_108_y.txt";
};

source {
    coords = 14.000000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_108_z.txt";
};

source {
    coords = 14.000000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_109_x.txt";
};

source {
    coords = 14.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_109_y.txt";
};

source {
    coords = 14.000000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_109_z.txt";
};

source {
    coords = 17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_110_x.txt";
};

source {
    coords = 17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_110_y.txt";
};

source {
    coords = 17.500000 -17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_110_z.txt";
};

source {
    coords = 17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_111_x.txt";
};

source {
    coords = 17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_111_y.txt";
};

source {
    coords = 17.500000 -14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_111_z.txt";
};

source {
    coords = 17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_112_x.txt";
};

source {
    coords = 17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_112_y.txt";
};

source {
    coords = 17.500000 -10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_112_z.txt";
};

source {
    coords = 17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_113_x.txt";
};

source {
    coords = 17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_113_y.txt";
};

source {
    coords = 17.500000 -7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_113_z.txt";
};

source {
    coords = 17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_114_x.txt";
};

source {
    coords = 17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_114_y.txt";
};

source {
    coords = 17.500000 -3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_114_z.txt";
};

source {
    coords = 17.500000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_115_x.txt";
};

source {
    coords = 17.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_115_y.txt";
};

source {
    coords = 17.500000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_115_z.txt";
};

source {
    coords = 17.500000 3.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_116_x.txt";
};

source {
    coords = 17.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_116_y.txt";
};

source {
    coords = 17.500000 3.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_116_z.txt";
};

source {
    coords = 17.500000 7.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_117_x.txt";
};

source {
    coords = 17.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_117_y.txt";
};

source {
    coords = 17.500000 7.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_117_z.txt";
};

source {
    coords = 17.500000 10.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_118_x.txt";
};

source {
    coords = 17.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_118_y.txt";
};

source {
    coords = 17.500000 10.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_118_z.txt";
};

source {
    coords = 17.500000 14.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_119_x.txt";
};

source {
    coords = 17.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_119_y.txt";
};

source {
    coords = 17.500000 14.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_119_z.txt";
};

source {
    coords = 17.500000 17.500000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "misfit_120_x.txt";
};

source {
    coords = 17.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "misfit_120_y.txt";
};

source {
    coords = 17.500000 17.500000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "misfit_120_z.txt";
};


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
