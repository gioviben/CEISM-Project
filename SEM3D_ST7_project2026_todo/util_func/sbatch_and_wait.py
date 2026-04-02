from pathlib import Path
import subprocess
import time
import re

def sbatch_and_wait(script):
    script = Path(script).resolve()
    workdir = script.parent

    result = subprocess.run(
        ["sbatch", script.name],
        cwd=workdir,
        check=True,
        capture_output=True,
        text=True
    )

    match = re.search(r"Submitted batch job (\d+)", result.stdout)
    if not match:
        raise RuntimeError(f"Could not parse job id from sbatch output: {result.stdout}")

    job_id = match.group(1)
    print(f"Submitted {script.name} from {workdir} -> job {job_id}")

    while True:
        check = subprocess.run(
            ["squeue", "--job", job_id],
            capture_output=True,
            text=True
        )
        if job_id not in check.stdout:
            print(f"Job {job_id} completed.")
            break
        time.sleep(15)