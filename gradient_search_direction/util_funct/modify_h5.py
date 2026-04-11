'''
import h5py
import numpy as np

def modify_h5_g(h5_path, vec_to_add, mapping_list, strict_bounds=False):
    """
    Add values from vec_to_add to the HDF5 material grid 'samples'
    at positions specified by mapping_list.

    Parameters
    ----------
    h5_path : str
        Path to the HDF5 material file.
    vec_to_add : array-like, shape (N,)
        Values to add.
    mapping_list : iterable of array-like, each of shape (3,)
        Physical coordinates [(x,y,z), ...] associated with vec_to_add.
    strict_bounds : bool, optional
        If True, raise an error when a coordinate is outside the domain.
        If False, clip indices to the valid grid range.

    Returns
    -------
    None
    """
    vec_to_add = np.asarray(vec_to_add, dtype=float)

    if vec_to_add.ndim != 1:
        raise ValueError(
            f"vec_to_add must be a 1D array, got shape {vec_to_add.shape}"
        )

    mapping_list = [np.asarray(coord, dtype=float) for coord in mapping_list]

    if len(mapping_list) != len(vec_to_add):
        raise ValueError(
            f"Length mismatch: len(mapping_list)={len(mapping_list)} "
            f"but len(vec_to_add)={len(vec_to_add)}"
        )

    if len(mapping_list) == 0:
        raise ValueError("mapping_list is empty")

    for i, coord in enumerate(mapping_list):
        if coord.shape != (3,):
            raise ValueError(
                f"mapping_list[{i}] must have shape (3,), got {coord.shape}"
            )

    with h5py.File(h5_path, "r+") as fmesh:
        if "samples" not in fmesh:
            raise KeyError(f"'samples' dataset not found in {h5_path}")

        if "xMinGlob" not in fmesh.attrs:
            raise KeyError(f"'xMinGlob' attribute not found in {h5_path}")

        if "xMaxGlob" not in fmesh.attrs:
            raise KeyError(f"'xMaxGlob' attribute not found in {h5_path}")

        ds = fmesh["samples"]
        mat = ds[...]

        if mat.ndim != 3:
            raise ValueError(
                f"'samples' must be a 3D dataset, got shape {mat.shape}"
            )

        xMinGlob = np.asarray(fmesh.attrs["xMinGlob"], dtype=float)
        xMaxGlob = np.asarray(fmesh.attrs["xMaxGlob"], dtype=float)

        if xMinGlob.shape != (3,) or xMaxGlob.shape != (3,):
            raise ValueError(
                f"xMinGlob and xMaxGlob must have shape (3,), got "
                f"{xMinGlob.shape} and {xMaxGlob.shape}"
            )

        npts = np.array(mat.shape, dtype=int)

        if np.any(npts < 2):
            raise ValueError(
                f"Each grid dimension must have at least 2 points, got {mat.shape}"
            )

        extent = xMaxGlob - xMinGlob
        if np.any(extent <= 0):
            raise ValueError(
                f"Invalid domain bounds: xMinGlob={xMinGlob}, xMaxGlob={xMaxGlob}"
            )

        # Step inferred from grid shape because xStep is not present in the file
        xStep = extent / (npts - 1)

        n_clipped = 0

        for i, (coord, val) in enumerate(zip(mapping_list, vec_to_add)):
            # Convert physical coordinates -> nearest grid index
            idx_float = (coord - xMinGlob) / xStep
            idx = np.rint(idx_float).astype(int)

            if strict_bounds:
                if np.any(idx < 0) or np.any(idx >= npts):
                    raise IndexError(
                        f"Point {i} with coord={coord} is outside the domain. "
                        f"Computed index={idx}, valid range: [0, {npts - 1}]"
                    )
            else:
                clipped_idx = np.clip(idx, 0, npts - 1)
                if not np.array_equal(idx, clipped_idx):
                    n_clipped += 1
                idx = clipped_idx

            mat[tuple(idx)] += val

        # Overwrite in place, do not delete/recreate dataset
        ds[...] = mat

    if n_clipped > 0:
        print(
            f"[modify_h5_g] Warning: {n_clipped} point(s) were outside the grid "
            f"and were clipped to the nearest valid index."
        )

'''
import h5py
import numpy as np

def modify_h5_g(h5_path, vec_to_add, mapping_list):    
    with h5py.File(h5_path, "r+") as fmesh:
        mat = fmesh["samples"][...]
        
        xMinGlob = fmesh.attrs["xMinGlob"]
        xMaxGlob = fmesh.attrs["xMaxGlob"]
        n__elems = fmesh.attrs["n"]  # attention au nom, voir remarque plus bas
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
