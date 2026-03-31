from pathlib import Path
import numpy as np

def parse_SEM3D_output(FOLDER_PATH, n_time_samples, number_stations, n_components = 3):
    data = np.zeros((n_time_samples, n_components, number_stations))
    folder = Path(FOLDER_PATH)
    for file in folder.iterdir():
        if file.is_file():
            parts = file.stem.split("_")
            station_number = int(parts[1])
            component = int(parts[3]) - 1
            with open(file, "r", encoding="utf-8") as f:
                lines = np.array([float(r.strip()) for r in f])
            data[:, component, station_number] = lines
    
    return data
                    




