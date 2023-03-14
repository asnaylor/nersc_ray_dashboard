import os
import time

from pathlib import Path
from subprocess import Popen, DEVNULL
from shlex import split

scratch_dir = os.getenv('SCRATCH')
user_jupyter = os.getenv('JUPYTERHUB_SERVICE_PREFIX')
jupyterhub = 'https://jupyter.nersc.gov'
grafana_port = '3000'
ray_dashboard_port = '8265'

prometheus_image = "prom/prometheus:v2.42.0"
prometheus_config = "/tmp/ray/session_latest/metrics/prometheus/prometheus.yml"

grafana_image = "grafana/grafana-oss:9.4.3"
grafana_config = "/tmp/ray/session_latest/metrics/grafana/grafana.ini"
grafana_provisioning = "/tmp/ray/session_latest/metrics/grafana/provisioning"

def get_grafana_url():
    return f"{jupyterhub}{user_jupyter}proxy/{grafana_port}"


def start_prometheus():
    prometheus_db_dir = os.path.join(f"{scratch_dir}", "ray_cluster/prometheus")
    Path(prometheus_db_dir).mkdir(parents=True, exist_ok=True)

    process = Popen(
        split(
            "shifter " \
            f"--image={prometheus_image} "\
            f"--volume={prometheus_db_dir}:/prometheus "\
            "/bin/prometheus "\
            f"--config.file={prometheus_config} "\
            "--storage.tsdb.path=/prometheus"
        ),
        stdout=DEVNULL, stderr=DEVNULL
    )
    print("Starting prometheus...")
    time.sleep(1)
    return process


def start_grafana():
    grafana_db_dir = os.path.join(f"{scratch_dir}", "ray_cluster/grafana")
    Path(grafana_db_dir).mkdir(parents=True, exist_ok=True)

    process = Popen(
        split(
            "shifter " \
            f"--image={grafana_image} "\
            f"--volume={grafana_db_dir}:/grafana "\
            "--env GF_PATHS_DATA=/grafana "\
            "--env GF_PATHS_PLUGINS=/grafana/plugins "\
            f"--env GF_SERVER_ROOT_URL={get_grafana_url()}/ "\
            f"--env GF_PATHS_CONFIG={grafana_config} "\
            f"--env GF_PATHS_PROVISIONING={grafana_provisioning} "
            "--entrypoint"
        ),
        stdout=DEVNULL, stderr=DEVNULL
    )
    print("Starting grafana...")
    time.sleep(1)
    return process

def get_ray_dashboard():
    return f'{jupyterhub}{user_jupyter}proxy/localhost:{ray_dashboard_port}/#/new/overview'

def get_grafana_dashboard():
    return f'{jupyterhub}{user_jupyter}proxy/{grafana_port}/d/rayDefaultDashboard'