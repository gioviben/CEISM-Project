# Definition materiaux
# Solid material
material 0 {
    domain    =         solid;
    deftype   =     Lambda_Mu;
    spacedef  =          file;
    filename0 = "example_la.h5"; 
    filename1 = "example_mu.h5";
    filename2 = "example_ds.h5";
};

material 3 { copy = 0; };
material 4 { copy = 0; };
material 5 { copy = 0; };
material 6 { copy = 0; };
material 7 { copy = 0; };
material 8 { copy = 0; };
material 9 { copy = 0; };
material 10 { copy = 0; };
