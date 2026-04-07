import os
from pathlib import Path

def write_backward_spec_from_template(template_backward_spec_path, output_backward_spec_path, adjoint_sources_folder_path, stations, file_names):
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
            rel_file_path = os.path.join(adjoint_sources_folder_path, fname)
            
            file_path_for_adjoint_prob = os.path.join(Path(adjoint_sources_folder_path).name, fname)

            if not os.path.isfile(rel_file_path):
                raise FileNotFoundError(
                    f"Adjoint source file not found for receiver {r}, component {cname}: {rel_file_path}"
                )
            
            block = (
                "source {\n"
                f"    coords = {x:.6f} {y:.6f} {z:.6f};\n"
                "    type = impulse;\n"
                f"    dir = {DVECS[cname]};\n"
                "    func = file;\n"
                f'    time_file = "{file_path_for_adjoint_prob}";\n'
                "};\n"
            )
            source_blocks.append(block)

    sources_text = "\n".join(source_blocks)

    if "# ADJOINT_SOURCES_PLACEHOLDER" not in template_text:
        raise ValueError("Template spec does not contain ADJOINT_SOURCES_PLACEHOLDER")

    final_text = template_text.replace("# ADJOINT_SOURCES_PLACEHOLDER", sources_text)

    output_file_path = os.path.join(output_backward_spec_path, "input.spec")

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(final_text)