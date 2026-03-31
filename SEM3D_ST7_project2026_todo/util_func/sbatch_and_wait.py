import subprocess
import time
import re

def sbatch_and_wait(script):
    result = subprocess.run(["sbatch", script], check=True, capture_output=True, text=True)
    job_id = re.search(r"(\d+)", result.stdout).group(1)
    print(f"Submitted {script} → job {job_id}")
    
    while True:
        check = subprocess.run(["squeue", "--job", job_id], capture_output=True, text=True)
        if job_id not in check.stdout:
            print(f"Job {job_id} completato.")
            break
        time.sleep(15)