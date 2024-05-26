import os
import subprocess

setup_sh_path = "/home/assetManagement/backend/etc/cronjob/set_up.sh"
stock_jobs_sh_path = "/home/assetManagement/backend/etc/cronjob/stock_jobs.sh"


def make_executable(script_path):
    os.chmod(script_path, 0o755)


def run_script(script_path):
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully ran {script_path}")
        print(result.stdout)
    else:
        print(f"Error running {script_path}")
        print(result.stderr)


make_executable(setup_sh_path)
make_executable(stock_jobs_sh_path)

run_script(setup_sh_path)
run_script(stock_jobs_sh_path)