def read_stations_pos(STATIONS_FILE_PATH):
    with open(STATIONS_FILE_PATH, "r") as f:
        return f.read()