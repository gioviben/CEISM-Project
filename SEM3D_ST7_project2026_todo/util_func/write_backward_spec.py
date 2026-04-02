import os

def write_backward_spec_from_template(template_backward_spec_path, output_backward_spec_path, stations, file_names, misfit_rel_dir="adjoint_sources"):
    DIRS = ["x", "y", "z"]
    DVECS = {
        "x": "1 0 0",
        "y": "0 1 0",
        "z": "0 0 1",
    }

    #------------
    # Basic Check
    #------------
    
    if stations.ndim != 2 or stations.shape[1] < 3:
        raise ValueError(
            f"stations must have shape (Nr, 3) or at least 3 columns, got {stations.shape}"
        )
    
    #------------

    with open(template_backward_spec_path, "r", encoding="utf-8") as f:
        template_text = f.read()

    output_dir = os.path.dirname(os.path.abspath(output_backward_spec_path))

    source_blocks = []
    nr = stations.shape[0]

    for r in range(nr):
        x, y, z = stations[r]
        for cname in DIRS:
            key = (r, cname)
            if key not in file_names:
                raise KeyError(f"Missing file name for receiver {r}, component {cname}")

            fname = file_names[key]

            # path for the .spec
            rel_path = os.path.join(misfit_rel_dir, fname).replace("\\", "/")

            real_path = os.path.join(output_dir, misfit_rel_dir, fname)

            if not os.path.isfile(real_path):
                raise FileNotFoundError(
                    f"Adjoint source file not found for receiver {r}, component {cname}: {real_path}"
                )

            block = (
                "source {\n"
                f"    coords = {x:.6f} {y:.6f} {z:.6f};\n"
                "    type = impulse;\n"
                f"    dir = {DVECS[cname]};\n"
                "    func = file;\n"
                f'    time_file = "{rel_path}";\n'
                "};\n"
            )
            source_blocks.append(block)

    sources_text = "\n".join(source_blocks)

    if "# ADJOINT_SOURCES_PLACEHOLDER" not in template_text:
        raise ValueError("Template spec does not contain ADJOINT_SOURCES_PLACEHOLDER")

    final_text = template_text.replace("# ADJOINT_SOURCES_PLACEHOLDER", sources_text)

    with open(output_backward_spec_path, "w", encoding="utf-8") as f:
        f.write(final_text)