import h5py
import numpy as np

def modify_h5_g(h5_path, vec_to_add, mapping_list):    
    with h5py.File(h5_path, "r+") as fmesh:
        mat = fmesh["samples"][...]
        
        xMinGlob = fmesh.attrs["xMinGlob"]
        xMaxGlob = fmesh.attrs["xMaxGlob"]
        n__elems = fmesh.attrs["xStep"]  # attention au nom, voir remarque plus bas
        xStep = np.array([
            (xMaxGlob[k] - xMinGlob[k]) / n__elems[k]
            for k in range(3)
        ])

        for coord, val in zip(mapping_list, vec_to_add):
            # Conversion coord physique → indice grille
            coord_int = ((coord - xMinGlob) / xStep).astype(int)
            # Option: sécuriser les indices (éviter out of bounds)
            coord_int = tuple(np.clip(coord_int, 0, np.array(mat.shape) - 1))
            mat[coord_int] += val
        del fmesh["samples"]
        fmesh.create_dataset('samples', data=mat)
    return None