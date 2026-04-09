from pathlib import Path
import pickle

def load_global_xyz_tuples(output_dir: Path):
    path = output_dir / "global_xyz_tuples.pkl"
    if not path.is_file():
        raise FileNotFoundError(f"Global xyz tuples file not found: {path}")

    with open(path, "rb") as f:
        return pickle.load(f)