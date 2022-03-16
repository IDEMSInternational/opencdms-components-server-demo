# OpenCDMS Component Server Demo

This is a small proof-of-concept API that receives requests for python code to execute and runs them, returning the result

## Pre-Requisites

The documentation requires python >=3.10 to be installed:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)

## Installation

The scripts below will create a python [virtual environment](https://docs.python.org/3/library/venv.html), activate, install required dependencies and start local server

=== "Windows (powershell)"

    ``` ps1
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

=== "Linux (bash)"

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## R installation

The server requires R to be installed. Instructions for installing R can be found at [https://cran.r-project.org/](https://cran.r-project.org/).
Extra guidance for installing R on Ubuntu 20.04 can be found at [https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-20-04).
The server has been tested with 'R version 4.1.2 (2021-11-01) -- "Bird Hippie"'.

When R is installed start R:

=== "Windows (powershell)"
Additionally you will have to install r-tools:
https://cran.r-project.org/bin/windows/Rtools/rtools40.html

Once installed you will need to call R from an elevated shell (run as administrator)

```ps1
Rscript install_packages.R
```

=== "Linux (bash)"
from the R prompt, install the `cdms.products` package, and then exit the R prompt.

```sh
sudo -i R
source("install_packages.R")
```

## Running locally

Once installed, subsequent server starts can skip installation steps

=== "Windows (powershell)"

    ``` ps1 linenums="1"
    .\.venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload
    ```

=== "Linux (bash)"

    ```sh linenums="1"
    source .venv/bin/activate
    uvicorn app.main:app --reload
    ```

The server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive docs available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

=== "Running in VS Code debugger"

See [https://fastapi.tiangolo.com/tutorial/debugging/](https://fastapi.tiangolo.com/tutorial/debugging/)

## Running in Docker

### Build

docker build -f DOCKERFILE --tag idems/opencdms-components-api:1.0.0 .

### Docker Run (interactive)

docker run -i --rm -p 80:80 idems/opencdms-components-api:1.0.0

## Troubleshooting

### Windows

**Cannot Run R Installation**
Make sure you have added R to the environment path (as per installation documentation), and are running powershell (or the R program) as an administrator. You may also need to deactivate any active python environment.

if you have added R to path environment variable and try to call directly you may have to resolve conflict with in-built powershell `r` command (see https://stackoverflow.com/questions/50190995/trying-to-add-r-exe-to-the-path), or just call via `R.exe` or `Rscript`
