# Ray cluster dashboard at NERSC 

-----

The web-based Ray dashboard can be accessed via [NERSC JupyterHub](https://jupyter.nersc.gov/) in order to monitor and debug any Ray application. The latest version of Ray **(2.3.0)** includes a "Metrics View" which enables users to visualise Ray time series metrics. This guide walks through how to connect to the Ray dashboard via JupyterHub. Also included is how to deploy the Prometheus + Grafana services on Perlmutter via shifter which are required for Ray metrics.


|<img src="https://raw.githubusercontent.com/ray-project/Images/master/docs/new-dashboard/Dashboard-overview.png" width="90%">|
|:--|
|Screenshot of the latest Ray Dashboard. Figure from [Ray Docs](https://docs.ray.io/en/latest/ray-core/ray-dashboard.html).|


```python
import sys
!{sys.executable} -m pip install "ray[default]>=2.3.0"
```

    Defaulting to user installation because normal site-packages is not writeable
    Requirement already satisfied: ray[default]>=2.3.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (2.3.0)
    Requirement already satisfied: grpcio>=1.32.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.51.1)
    Requirement already satisfied: click>=7.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (8.0.4)
    Requirement already satisfied: attrs in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (21.4.0)
    Requirement already satisfied: numpy>=1.19.3 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.21.5)
    Requirement already satisfied: pyyaml in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (6.0)
    Requirement already satisfied: jsonschema in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (4.4.0)
    Requirement already satisfied: filelock in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (3.6.0)
    Requirement already satisfied: aiosignal in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.3.1)
    Requirement already satisfied: protobuf!=3.19.5,>=3.15.3 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (4.21.12)
    Requirement already satisfied: msgpack<2.0.0,>=1.0.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.0.3)
    Requirement already satisfied: frozenlist in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.3.3)
    Requirement already satisfied: virtualenv>=20.0.24 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (20.17.1)
    Requirement already satisfied: requests in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (2.28.1)
    Requirement already satisfied: prometheus-client>=0.7.1 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (0.13.1)
    Requirement already satisfied: smart-open in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (6.3.0)
    Requirement already satisfied: colorful in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (0.5.5)
    Requirement already satisfied: gpustat>=1.0.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.0.0)
    Requirement already satisfied: opencensus in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (0.11.0)
    Requirement already satisfied: pydantic in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (1.10.4)
    Requirement already satisfied: aiohttp-cors in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (0.7.0)
    Requirement already satisfied: aiohttp>=3.7 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (3.8.3)
    Requirement already satisfied: py-spy>=0.2.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from ray[default]>=2.3.0) (0.3.14)
    Requirement already satisfied: yarl<2.0,>=1.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from aiohttp>=3.7->ray[default]>=2.3.0) (1.8.2)
    Requirement already satisfied: charset-normalizer<3.0,>=2.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from aiohttp>=3.7->ray[default]>=2.3.0) (2.0.4)
    Requirement already satisfied: async-timeout<5.0,>=4.0.0a3 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from aiohttp>=3.7->ray[default]>=2.3.0) (4.0.2)
    Requirement already satisfied: multidict<7.0,>=4.5 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from aiohttp>=3.7->ray[default]>=2.3.0) (6.0.4)
    Requirement already satisfied: blessed>=1.17.1 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from gpustat>=1.0.0->ray[default]>=2.3.0) (1.19.1)
    Requirement already satisfied: six>=1.7 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from gpustat>=1.0.0->ray[default]>=2.3.0) (1.16.0)
    Requirement already satisfied: nvidia-ml-py<=11.495.46,>=11.450.129 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from gpustat>=1.0.0->ray[default]>=2.3.0) (11.495.46)
    Requirement already satisfied: psutil>=5.6.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from gpustat>=1.0.0->ray[default]>=2.3.0) (5.9.0)
    Requirement already satisfied: distlib<1,>=0.3.6 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from virtualenv>=20.0.24->ray[default]>=2.3.0) (0.3.6)
    Requirement already satisfied: platformdirs<3,>=2.4 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from virtualenv>=20.0.24->ray[default]>=2.3.0) (2.6.2)
    Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from jsonschema->ray[default]>=2.3.0) (0.18.0)
    Requirement already satisfied: google-api-core<3.0.0,>=1.0.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from opencensus->ray[default]>=2.3.0) (2.11.0)
    Requirement already satisfied: opencensus-context>=0.1.3 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from opencensus->ray[default]>=2.3.0) (0.1.3)
    Requirement already satisfied: typing-extensions>=4.2.0 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from pydantic->ray[default]>=2.3.0) (4.3.0)
    Requirement already satisfied: idna<4,>=2.5 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from requests->ray[default]>=2.3.0) (3.3)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from requests->ray[default]>=2.3.0) (1.26.11)
    Requirement already satisfied: certifi>=2017.4.17 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from requests->ray[default]>=2.3.0) (2022.6.15)
    Requirement already satisfied: wcwidth>=0.1.4 in /global/common/software/nersc/pm-2022q3/sw/python/3.9-anaconda-2021.11/lib/python3.9/site-packages (from blessed>=1.17.1->gpustat>=1.0.0->ray[default]>=2.3.0) (0.2.5)
    Requirement already satisfied: googleapis-common-protos<2.0dev,>=1.56.2 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (1.58.0)
    Requirement already satisfied: google-auth<3.0dev,>=2.14.1 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (2.16.0)
    Requirement already satisfied: cachetools<6.0,>=2.0.0 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from google-auth<3.0dev,>=2.14.1->google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (5.2.1)
    Requirement already satisfied: pyasn1-modules>=0.2.1 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from google-auth<3.0dev,>=2.14.1->google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (0.2.8)
    Requirement already satisfied: rsa<5,>=3.1.4 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from google-auth<3.0dev,>=2.14.1->google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (4.9)
    Requirement already satisfied: pyasn1<0.5.0,>=0.4.6 in /global/u2/a/asnaylor/.local/perlmutter/3.9-anaconda-2021.11/lib/python3.9/site-packages (from pyasn1-modules>=0.2.1->google-auth<3.0dev,>=2.14.1->google-api-core<3.0.0,>=1.0.0->opencensus->ray[default]>=2.3.0) (0.4.8)


----

## Connecting to the ray dashboard


```python
import logging
import os
import ray

from utils import get_grafana_url, start_prometheus, start_grafana, get_ray_dashboard, get_grafana_dashboard
```

Start the Ray head node:

> **Warning**
> If you want to use metrics in your Ray dashboard the Ray head node needs to know about the Grafana Host url (`RAY_GRAFANA_IFRAME_HOST`).



```python
os.environ["RAY_GRAFANA_IFRAME_HOST"] = get_grafana_url()

if ray.is_initialized:
    ray.shutdown()
ray.init(logging_level=logging.ERROR)
```




<div>
    <div style="margin-left: 50px;display: flex;flex-direction: row;align-items: center">
        <h3 style="color: var(--jp-ui-font-color0)">Ray</h3>
        <svg version="1.1" id="ray" width="3em" viewBox="0 0 144.5 144.6" style="margin-left: 3em;margin-right: 3em">
            <g id="layer-1">
                <path fill="#00a2e9" class="st0" d="M97.3,77.2c-3.8-1.1-6.2,0.9-8.3,5.1c-3.5,6.8-9.9,9.9-17.4,9.6S58,88.1,54.8,81.2c-1.4-3-3-4-6.3-4.1
                    c-5.6-0.1-9.9,0.1-13.1,6.4c-3.8,7.6-13.6,10.2-21.8,7.6C5.2,88.4-0.4,80.5,0,71.7c0.1-8.4,5.7-15.8,13.8-18.2
                    c8.4-2.6,17.5,0.7,22.3,8c1.3,1.9,1.3,5.2,3.6,5.6c3.9,0.6,8,0.2,12,0.2c1.8,0,1.9-1.6,2.4-2.8c3.5-7.8,9.7-11.8,18-11.9
                    c8.2-0.1,14.4,3.9,17.8,11.4c1.3,2.8,2.9,3.6,5.7,3.3c1-0.1,2,0.1,3,0c2.8-0.5,6.4,1.7,8.1-2.7s-2.3-5.5-4.1-7.5
                    c-5.1-5.7-10.9-10.8-16.1-16.3C84,38,81.9,37.1,78,38.3C66.7,42,56.2,35.7,53,24.1C50.3,14,57.3,2.8,67.7,0.5
                    C78.4-2,89,4.7,91.5,15.3c0.1,0.3,0.1,0.5,0.2,0.8c0.7,3.4,0.7,6.9-0.8,9.8c-1.7,3.2-0.8,5,1.5,7.2c6.7,6.5,13.3,13,19.8,19.7
                    c1.8,1.8,3,2.1,5.5,1.2c9.1-3.4,17.9-0.6,23.4,7c4.8,6.9,4.6,16.1-0.4,22.9c-5.4,7.2-14.2,9.9-23.1,6.5c-2.3-0.9-3.5-0.6-5.1,1.1
                    c-6.7,6.9-13.6,13.7-20.5,20.4c-1.8,1.8-2.5,3.2-1.4,5.9c3.5,8.7,0.3,18.6-7.7,23.6c-7.9,5-18.2,3.8-24.8-2.9
                    c-6.4-6.4-7.4-16.2-2.5-24.3c4.9-7.8,14.5-11,23.1-7.8c3,1.1,4.7,0.5,6.9-1.7C91.7,98.4,98,92.3,104.2,86c1.6-1.6,4.1-2.7,2.6-6.2
                    c-1.4-3.3-3.8-2.5-6.2-2.6C99.8,77.2,98.9,77.2,97.3,77.2z M72.1,29.7c5.5,0.1,9.9-4.3,10-9.8c0-0.1,0-0.2,0-0.3
                    C81.8,14,77,9.8,71.5,10.2c-5,0.3-9,4.2-9.3,9.2c-0.2,5.5,4,10.1,9.5,10.3C71.8,29.7,72,29.7,72.1,29.7z M72.3,62.3
                    c-5.4-0.1-9.9,4.2-10.1,9.7c0,0.2,0,0.3,0,0.5c0.2,5.4,4.5,9.7,9.9,10c5.1,0.1,9.9-4.7,10.1-9.8c0.2-5.5-4-10-9.5-10.3
                    C72.6,62.3,72.4,62.3,72.3,62.3z M115,72.5c0.1,5.4,4.5,9.7,9.8,9.9c5.6-0.2,10-4.8,10-10.4c-0.2-5.4-4.6-9.7-10-9.7
                    c-5.3-0.1-9.8,4.2-9.9,9.5C115,72.1,115,72.3,115,72.5z M19.5,62.3c-5.4,0.1-9.8,4.4-10,9.8c-0.1,5.1,5.2,10.4,10.2,10.3
                    c5.6-0.2,10-4.9,9.8-10.5c-0.1-5.4-4.5-9.7-9.9-9.6C19.6,62.3,19.5,62.3,19.5,62.3z M71.8,134.6c5.9,0.2,10.3-3.9,10.4-9.6
                    c0.5-5.5-3.6-10.4-9.1-10.8c-5.5-0.5-10.4,3.6-10.8,9.1c0,0.5,0,0.9,0,1.4c-0.2,5.3,4,9.8,9.3,10
                    C71.6,134.6,71.7,134.6,71.8,134.6z"/>
            </g>
        </svg>
        <table>
            <tr>
                <td style="text-align: left"><b>Python version:</b></td>
                <td style="text-align: left"><b>3.9.7</b></td>
            </tr>
            <tr>
                <td style="text-align: left"><b>Ray version:</b></td>
                <td style="text-align: left"><b> 2.3.0</b></td>
            </tr>
            <tr>
    <td style="text-align: left"><b>Dashboard:</b></td>
    <td style="text-align: left"><b><a href="http://127.0.0.1:8265" target="_blank">http://127.0.0.1:8265</a></b></td>
</tr>

        </table>
    </div>
</div>




> **Note**
> If your ray head node is not running on the same machine as this Jupyter notebook then forward the Ray dashboard port (`8265`) to this machine (example: `ssh -N -L localhost:8265:localhost:8265 nid02010`). 
> Port forward can be easily done with the subprocess Python library.

Once the Ray head node is running then start the prometheus service:


```python
prometheus = start_prometheus()
```

    Starting prometheus...


The `start_prometheus` function starts prometheus in a shifter container with the relevant configration file generated by the Ray head process.

```bash
shifter \
--image={prometheus_image} \
--volume={prometheus_db_dir}:/prometheus \
/bin/prometheus \
--config.file=/tmp/ray/session_latest/metrics/prometheus/prometheus.yml \
--storage.tsdb.path=/prometheus
```

Once the prometheus service is running then start the grafana service:


```python
grafana = start_grafana()
```

    Starting grafana...


The `start_grafana` function starts grafana in a shifter container with the relevant configration file generated by the Ray head process.

```bash
shifter
--image={grafana_image} \
--volume={grafana_db_dir}:/grafana \
--env GF_PATHS_DATA=/grafana \
--env GF_PATHS_PLUGINS=/grafana/plugins \
--env GF_SERVER_ROOT_URL={grafana_root_url}/ \
--env GF_PATHS_CONFIG=/tmp/ray/session_latest/metrics/grafana/grafana.ini \
--env GF_PATHS_PROVISIONING=/tmp/ray/session_latest/metrics/grafana/provisioning \
--entrypoint
```

### Access Ray Dashboard


```python
get_ray_dashboard()
```




    'https://jupyter.nersc.govNoneproxy/localhost:8265/#/new/overview'



### Access Grafana Dashboard

```
username: admin
password: admin
```


```python
get_grafana_dashboard()
```




    'https://jupyter.nersc.govNoneproxy/3000/d/rayDefaultDashboard'



### Shutdown processes


```python
ray.shutdown()
prometheus.kill()
grafana.kill()
```


```python

```
