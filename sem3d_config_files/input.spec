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

source {
    coords = -7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_0_x.txt";
};

source {
    coords = -7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_0_y.txt";
};

source {
    coords = -7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_0_z.txt";
};

source {
    coords = -5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_1_x.txt";
};

source {
    coords = -5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_1_y.txt";
};

source {
    coords = -5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_1_z.txt";
};

source {
    coords = -4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_2_x.txt";
};

source {
    coords = -4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_2_y.txt";
};

source {
    coords = -4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_2_z.txt";
};

source {
    coords = -2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_3_x.txt";
};

source {
    coords = -2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_3_y.txt";
};

source {
    coords = -2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_3_z.txt";
};

source {
    coords = -1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_4_x.txt";
};

source {
    coords = -1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_4_y.txt";
};

source {
    coords = -1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_4_z.txt";
};

source {
    coords = 0.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_5_x.txt";
};

source {
    coords = 0.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_5_y.txt";
};

source {
    coords = 0.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_5_z.txt";
};

source {
    coords = 1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_6_x.txt";
};

source {
    coords = 1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_6_y.txt";
};

source {
    coords = 1400.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_6_z.txt";
};

source {
    coords = 2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_7_x.txt";
};

source {
    coords = 2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_7_y.txt";
};

source {
    coords = 2800.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_7_z.txt";
};

source {
    coords = 4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_8_x.txt";
};

source {
    coords = 4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_8_y.txt";
};

source {
    coords = 4200.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_8_z.txt";
};

source {
    coords = 5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_9_x.txt";
};

source {
    coords = 5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_9_y.txt";
};

source {
    coords = 5600.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_9_z.txt";
};

source {
    coords = 7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_10_x.txt";
};

source {
    coords = 7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_10_y.txt";
};

source {
    coords = 7000.000000 -7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_10_z.txt";
};

source {
    coords = -7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_11_x.txt";
};

source {
    coords = -7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_11_y.txt";
};

source {
    coords = -7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_11_z.txt";
};

source {
    coords = -5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_12_x.txt";
};

source {
    coords = -5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_12_y.txt";
};

source {
    coords = -5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_12_z.txt";
};

source {
    coords = -4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_13_x.txt";
};

source {
    coords = -4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_13_y.txt";
};

source {
    coords = -4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_13_z.txt";
};

source {
    coords = -2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_14_x.txt";
};

source {
    coords = -2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_14_y.txt";
};

source {
    coords = -2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_14_z.txt";
};

source {
    coords = -1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_15_x.txt";
};

source {
    coords = -1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_15_y.txt";
};

source {
    coords = -1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_15_z.txt";
};

source {
    coords = 0.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_16_x.txt";
};

source {
    coords = 0.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_16_y.txt";
};

source {
    coords = 0.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_16_z.txt";
};

source {
    coords = 1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_17_x.txt";
};

source {
    coords = 1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_17_y.txt";
};

source {
    coords = 1400.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_17_z.txt";
};

source {
    coords = 2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_18_x.txt";
};

source {
    coords = 2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_18_y.txt";
};

source {
    coords = 2800.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_18_z.txt";
};

source {
    coords = 4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_19_x.txt";
};

source {
    coords = 4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_19_y.txt";
};

source {
    coords = 4200.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_19_z.txt";
};

source {
    coords = 5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_20_x.txt";
};

source {
    coords = 5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_20_y.txt";
};

source {
    coords = 5600.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_20_z.txt";
};

source {
    coords = 7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_21_x.txt";
};

source {
    coords = 7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_21_y.txt";
};

source {
    coords = 7000.000000 -5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_21_z.txt";
};

source {
    coords = -7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_22_x.txt";
};

source {
    coords = -7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_22_y.txt";
};

source {
    coords = -7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_22_z.txt";
};

source {
    coords = -5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_23_x.txt";
};

source {
    coords = -5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_23_y.txt";
};

source {
    coords = -5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_23_z.txt";
};

source {
    coords = -4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_24_x.txt";
};

source {
    coords = -4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_24_y.txt";
};

source {
    coords = -4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_24_z.txt";
};

source {
    coords = -2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_25_x.txt";
};

source {
    coords = -2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_25_y.txt";
};

source {
    coords = -2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_25_z.txt";
};

source {
    coords = -1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_26_x.txt";
};

source {
    coords = -1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_26_y.txt";
};

source {
    coords = -1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_26_z.txt";
};

source {
    coords = 0.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_27_x.txt";
};

source {
    coords = 0.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_27_y.txt";
};

source {
    coords = 0.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_27_z.txt";
};

source {
    coords = 1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_28_x.txt";
};

source {
    coords = 1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_28_y.txt";
};

source {
    coords = 1400.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_28_z.txt";
};

source {
    coords = 2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_29_x.txt";
};

source {
    coords = 2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_29_y.txt";
};

source {
    coords = 2800.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_29_z.txt";
};

source {
    coords = 4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_30_x.txt";
};

source {
    coords = 4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_30_y.txt";
};

source {
    coords = 4200.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_30_z.txt";
};

source {
    coords = 5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_31_x.txt";
};

source {
    coords = 5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_31_y.txt";
};

source {
    coords = 5600.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_31_z.txt";
};

source {
    coords = 7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_32_x.txt";
};

source {
    coords = 7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_32_y.txt";
};

source {
    coords = 7000.000000 -4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_32_z.txt";
};

source {
    coords = -7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_33_x.txt";
};

source {
    coords = -7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_33_y.txt";
};

source {
    coords = -7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_33_z.txt";
};

source {
    coords = -5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_34_x.txt";
};

source {
    coords = -5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_34_y.txt";
};

source {
    coords = -5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_34_z.txt";
};

source {
    coords = -4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_35_x.txt";
};

source {
    coords = -4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_35_y.txt";
};

source {
    coords = -4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_35_z.txt";
};

source {
    coords = -2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_36_x.txt";
};

source {
    coords = -2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_36_y.txt";
};

source {
    coords = -2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_36_z.txt";
};

source {
    coords = -1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_37_x.txt";
};

source {
    coords = -1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_37_y.txt";
};

source {
    coords = -1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_37_z.txt";
};

source {
    coords = 0.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_38_x.txt";
};

source {
    coords = 0.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_38_y.txt";
};

source {
    coords = 0.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_38_z.txt";
};

source {
    coords = 1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_39_x.txt";
};

source {
    coords = 1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_39_y.txt";
};

source {
    coords = 1400.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_39_z.txt";
};

source {
    coords = 2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_40_x.txt";
};

source {
    coords = 2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_40_y.txt";
};

source {
    coords = 2800.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_40_z.txt";
};

source {
    coords = 4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_41_x.txt";
};

source {
    coords = 4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_41_y.txt";
};

source {
    coords = 4200.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_41_z.txt";
};

source {
    coords = 5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_42_x.txt";
};

source {
    coords = 5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_42_y.txt";
};

source {
    coords = 5600.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_42_z.txt";
};

source {
    coords = 7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_43_x.txt";
};

source {
    coords = 7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_43_y.txt";
};

source {
    coords = 7000.000000 -2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_43_z.txt";
};

source {
    coords = -7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_44_x.txt";
};

source {
    coords = -7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_44_y.txt";
};

source {
    coords = -7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_44_z.txt";
};

source {
    coords = -5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_45_x.txt";
};

source {
    coords = -5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_45_y.txt";
};

source {
    coords = -5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_45_z.txt";
};

source {
    coords = -4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_46_x.txt";
};

source {
    coords = -4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_46_y.txt";
};

source {
    coords = -4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_46_z.txt";
};

source {
    coords = -2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_47_x.txt";
};

source {
    coords = -2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_47_y.txt";
};

source {
    coords = -2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_47_z.txt";
};

source {
    coords = -1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_48_x.txt";
};

source {
    coords = -1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_48_y.txt";
};

source {
    coords = -1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_48_z.txt";
};

source {
    coords = 0.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_49_x.txt";
};

source {
    coords = 0.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_49_y.txt";
};

source {
    coords = 0.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_49_z.txt";
};

source {
    coords = 1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_50_x.txt";
};

source {
    coords = 1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_50_y.txt";
};

source {
    coords = 1400.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_50_z.txt";
};

source {
    coords = 2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_51_x.txt";
};

source {
    coords = 2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_51_y.txt";
};

source {
    coords = 2800.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_51_z.txt";
};

source {
    coords = 4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_52_x.txt";
};

source {
    coords = 4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_52_y.txt";
};

source {
    coords = 4200.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_52_z.txt";
};

source {
    coords = 5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_53_x.txt";
};

source {
    coords = 5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_53_y.txt";
};

source {
    coords = 5600.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_53_z.txt";
};

source {
    coords = 7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_54_x.txt";
};

source {
    coords = 7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_54_y.txt";
};

source {
    coords = 7000.000000 -1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_54_z.txt";
};

source {
    coords = -7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_55_x.txt";
};

source {
    coords = -7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_55_y.txt";
};

source {
    coords = -7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_55_z.txt";
};

source {
    coords = -5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_56_x.txt";
};

source {
    coords = -5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_56_y.txt";
};

source {
    coords = -5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_56_z.txt";
};

source {
    coords = -4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_57_x.txt";
};

source {
    coords = -4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_57_y.txt";
};

source {
    coords = -4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_57_z.txt";
};

source {
    coords = -2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_58_x.txt";
};

source {
    coords = -2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_58_y.txt";
};

source {
    coords = -2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_58_z.txt";
};

source {
    coords = -1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_59_x.txt";
};

source {
    coords = -1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_59_y.txt";
};

source {
    coords = -1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_59_z.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_60_x.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_60_y.txt";
};

source {
    coords = 0.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_60_z.txt";
};

source {
    coords = 1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_61_x.txt";
};

source {
    coords = 1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_61_y.txt";
};

source {
    coords = 1400.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_61_z.txt";
};

source {
    coords = 2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_62_x.txt";
};

source {
    coords = 2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_62_y.txt";
};

source {
    coords = 2800.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_62_z.txt";
};

source {
    coords = 4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_63_x.txt";
};

source {
    coords = 4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_63_y.txt";
};

source {
    coords = 4200.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_63_z.txt";
};

source {
    coords = 5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_64_x.txt";
};

source {
    coords = 5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_64_y.txt";
};

source {
    coords = 5600.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_64_z.txt";
};

source {
    coords = 7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_65_x.txt";
};

source {
    coords = 7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_65_y.txt";
};

source {
    coords = 7000.000000 0.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_65_z.txt";
};

source {
    coords = -7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_66_x.txt";
};

source {
    coords = -7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_66_y.txt";
};

source {
    coords = -7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_66_z.txt";
};

source {
    coords = -5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_67_x.txt";
};

source {
    coords = -5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_67_y.txt";
};

source {
    coords = -5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_67_z.txt";
};

source {
    coords = -4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_68_x.txt";
};

source {
    coords = -4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_68_y.txt";
};

source {
    coords = -4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_68_z.txt";
};

source {
    coords = -2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_69_x.txt";
};

source {
    coords = -2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_69_y.txt";
};

source {
    coords = -2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_69_z.txt";
};

source {
    coords = -1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_70_x.txt";
};

source {
    coords = -1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_70_y.txt";
};

source {
    coords = -1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_70_z.txt";
};

source {
    coords = 0.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_71_x.txt";
};

source {
    coords = 0.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_71_y.txt";
};

source {
    coords = 0.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_71_z.txt";
};

source {
    coords = 1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_72_x.txt";
};

source {
    coords = 1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_72_y.txt";
};

source {
    coords = 1400.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_72_z.txt";
};

source {
    coords = 2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_73_x.txt";
};

source {
    coords = 2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_73_y.txt";
};

source {
    coords = 2800.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_73_z.txt";
};

source {
    coords = 4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_74_x.txt";
};

source {
    coords = 4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_74_y.txt";
};

source {
    coords = 4200.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_74_z.txt";
};

source {
    coords = 5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_75_x.txt";
};

source {
    coords = 5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_75_y.txt";
};

source {
    coords = 5600.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_75_z.txt";
};

source {
    coords = 7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_76_x.txt";
};

source {
    coords = 7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_76_y.txt";
};

source {
    coords = 7000.000000 1400.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_76_z.txt";
};

source {
    coords = -7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_77_x.txt";
};

source {
    coords = -7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_77_y.txt";
};

source {
    coords = -7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_77_z.txt";
};

source {
    coords = -5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_78_x.txt";
};

source {
    coords = -5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_78_y.txt";
};

source {
    coords = -5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_78_z.txt";
};

source {
    coords = -4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_79_x.txt";
};

source {
    coords = -4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_79_y.txt";
};

source {
    coords = -4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_79_z.txt";
};

source {
    coords = -2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_80_x.txt";
};

source {
    coords = -2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_80_y.txt";
};

source {
    coords = -2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_80_z.txt";
};

source {
    coords = -1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_81_x.txt";
};

source {
    coords = -1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_81_y.txt";
};

source {
    coords = -1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_81_z.txt";
};

source {
    coords = 0.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_82_x.txt";
};

source {
    coords = 0.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_82_y.txt";
};

source {
    coords = 0.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_82_z.txt";
};

source {
    coords = 1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_83_x.txt";
};

source {
    coords = 1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_83_y.txt";
};

source {
    coords = 1400.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_83_z.txt";
};

source {
    coords = 2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_84_x.txt";
};

source {
    coords = 2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_84_y.txt";
};

source {
    coords = 2800.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_84_z.txt";
};

source {
    coords = 4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_85_x.txt";
};

source {
    coords = 4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_85_y.txt";
};

source {
    coords = 4200.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_85_z.txt";
};

source {
    coords = 5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_86_x.txt";
};

source {
    coords = 5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_86_y.txt";
};

source {
    coords = 5600.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_86_z.txt";
};

source {
    coords = 7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_87_x.txt";
};

source {
    coords = 7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_87_y.txt";
};

source {
    coords = 7000.000000 2800.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_87_z.txt";
};

source {
    coords = -7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_88_x.txt";
};

source {
    coords = -7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_88_y.txt";
};

source {
    coords = -7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_88_z.txt";
};

source {
    coords = -5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_89_x.txt";
};

source {
    coords = -5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_89_y.txt";
};

source {
    coords = -5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_89_z.txt";
};

source {
    coords = -4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_90_x.txt";
};

source {
    coords = -4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_90_y.txt";
};

source {
    coords = -4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_90_z.txt";
};

source {
    coords = -2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_91_x.txt";
};

source {
    coords = -2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_91_y.txt";
};

source {
    coords = -2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_91_z.txt";
};

source {
    coords = -1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_92_x.txt";
};

source {
    coords = -1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_92_y.txt";
};

source {
    coords = -1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_92_z.txt";
};

source {
    coords = 0.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_93_x.txt";
};

source {
    coords = 0.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_93_y.txt";
};

source {
    coords = 0.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_93_z.txt";
};

source {
    coords = 1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_94_x.txt";
};

source {
    coords = 1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_94_y.txt";
};

source {
    coords = 1400.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_94_z.txt";
};

source {
    coords = 2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_95_x.txt";
};

source {
    coords = 2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_95_y.txt";
};

source {
    coords = 2800.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_95_z.txt";
};

source {
    coords = 4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_96_x.txt";
};

source {
    coords = 4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_96_y.txt";
};

source {
    coords = 4200.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_96_z.txt";
};

source {
    coords = 5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_97_x.txt";
};

source {
    coords = 5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_97_y.txt";
};

source {
    coords = 5600.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_97_z.txt";
};

source {
    coords = 7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_98_x.txt";
};

source {
    coords = 7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_98_y.txt";
};

source {
    coords = 7000.000000 4200.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_98_z.txt";
};

source {
    coords = -7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_99_x.txt";
};

source {
    coords = -7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_99_y.txt";
};

source {
    coords = -7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_99_z.txt";
};

source {
    coords = -5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_100_x.txt";
};

source {
    coords = -5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_100_y.txt";
};

source {
    coords = -5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_100_z.txt";
};

source {
    coords = -4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_101_x.txt";
};

source {
    coords = -4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_101_y.txt";
};

source {
    coords = -4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_101_z.txt";
};

source {
    coords = -2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_102_x.txt";
};

source {
    coords = -2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_102_y.txt";
};

source {
    coords = -2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_102_z.txt";
};

source {
    coords = -1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_103_x.txt";
};

source {
    coords = -1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_103_y.txt";
};

source {
    coords = -1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_103_z.txt";
};

source {
    coords = 0.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_104_x.txt";
};

source {
    coords = 0.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_104_y.txt";
};

source {
    coords = 0.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_104_z.txt";
};

source {
    coords = 1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_105_x.txt";
};

source {
    coords = 1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_105_y.txt";
};

source {
    coords = 1400.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_105_z.txt";
};

source {
    coords = 2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_106_x.txt";
};

source {
    coords = 2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_106_y.txt";
};

source {
    coords = 2800.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_106_z.txt";
};

source {
    coords = 4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_107_x.txt";
};

source {
    coords = 4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_107_y.txt";
};

source {
    coords = 4200.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_107_z.txt";
};

source {
    coords = 5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_108_x.txt";
};

source {
    coords = 5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_108_y.txt";
};

source {
    coords = 5600.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_108_z.txt";
};

source {
    coords = 7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_109_x.txt";
};

source {
    coords = 7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_109_y.txt";
};

source {
    coords = 7000.000000 5600.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_109_z.txt";
};

source {
    coords = -7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_110_x.txt";
};

source {
    coords = -7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_110_y.txt";
};

source {
    coords = -7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_110_z.txt";
};

source {
    coords = -5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_111_x.txt";
};

source {
    coords = -5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_111_y.txt";
};

source {
    coords = -5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_111_z.txt";
};

source {
    coords = -4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_112_x.txt";
};

source {
    coords = -4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_112_y.txt";
};

source {
    coords = -4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_112_z.txt";
};

source {
    coords = -2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_113_x.txt";
};

source {
    coords = -2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_113_y.txt";
};

source {
    coords = -2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_113_z.txt";
};

source {
    coords = -1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_114_x.txt";
};

source {
    coords = -1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_114_y.txt";
};

source {
    coords = -1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_114_z.txt";
};

source {
    coords = 0.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_115_x.txt";
};

source {
    coords = 0.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_115_y.txt";
};

source {
    coords = 0.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_115_z.txt";
};

source {
    coords = 1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_116_x.txt";
};

source {
    coords = 1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_116_y.txt";
};

source {
    coords = 1400.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_116_z.txt";
};

source {
    coords = 2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_117_x.txt";
};

source {
    coords = 2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_117_y.txt";
};

source {
    coords = 2800.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_117_z.txt";
};

source {
    coords = 4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_118_x.txt";
};

source {
    coords = 4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_118_y.txt";
};

source {
    coords = 4200.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_118_z.txt";
};

source {
    coords = 5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_119_x.txt";
};

source {
    coords = 5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_119_y.txt";
};

source {
    coords = 5600.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_119_z.txt";
};

source {
    coords = 7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 1 0 0;
    func = file;
    time_file = "ad_s/misfit_120_x.txt";
};

source {
    coords = 7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 1 0;
    func = file;
    time_file = "ad_s/misfit_120_y.txt";
};

source {
    coords = 7000.000000 7000.000000 0.000000;
    type = impulse;
    dir = 0 0 1;
    func = file;
    time_file = "ad_s/misfit_120_z.txt";
};


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