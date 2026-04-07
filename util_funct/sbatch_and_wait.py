from pathlib import Path
import subprocess
import time
import re

def sbatch_and_wait(script):
    script = Path(script).resolve()
    workdir = script.parent

    start_time = time.time()

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
        if not any(job_id == word for word in check.stdout.split()):
            time.sleep(3)  # attendi che sacct aggiorni lo stato
            break

        time.sleep(15)

    elapsed = time.time() - start_time

    sacct = subprocess.run(
        ["sacct", "-j", job_id, "--format=JobID,State", "--noheader"],
        capture_output=True,
        text=True
    )

    lines = [line.strip() for line in sacct.stdout.splitlines() if line.strip()]

    final_state = "UNKNOWN"
    for line in lines:
        parts = line.split()
        if parts and parts[0] == job_id:
            final_state = parts[1]
            break

    print(f"Job {job_id} finished with state: {final_state}")
    print(f"{script.name} executed in {elapsed:.2f} seconds")
    print("")

    if final_state != "COMPLETED":
        raise RuntimeError(f"Job {job_id} did not complete successfully: {final_state}")