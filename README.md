# OpenCDMS Component Server Demo

This is a small proof-of-concept designed to produce specific data-products from opencdms data

## Pre-Requisites

The documentation requires python 3.8 to be installed:  
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
sudo Rscript install_packages.R
```

## Test database installation

The test database only needs to be installed if you plan to use the `test_data_api` endpoint.
You will first need to configure the `.env` file to provide a database_uri

```sh
cp .env.example .env
```
You will then need to either populate with an existing database endpoint, or run a local copy to connect to using the default uri. A docker template has been created to facilitate this, see notes in [test-data-server/REAMDE.md](test-data-server/README.md)
```
docker-compose --file test-data-server/docker-compose.yml up
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

The server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000) which will also host interactive documentation


=== "Running in VS Code debugger"

See [https://fastapi.tiangolo.com/tutorial/debugging/](https://fastapi.tiangolo.com/tutorial/debugging/)

## Running in Docker

### Build

docker build --tag idems/opencdms-components-api:1.0.0 .

### Docker Run (interactive)

docker run -i --rm -p 80:80 idems/opencdms-components-api:1.0.0

## Known Issues and Limitations

## Troubleshooting

### Address already in use
This can happen if multiple instances of server running, or one instance failed to close completely.
Kill the process running on the port

`sudo fuser -k 8000/tcp`

### Python 3.10

To run on python 3.10 the package `backports.zoneinfo` may need to be removed

### Additional packages (possibly) required
https://pypi.org/project/mysqlclient/
`sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

https://www.psycopg.org/docs/install.html
`pip install psycopg2-binary`

https://pypi.org/project/launchpadlib/
`sudo apt install python3-testresources` or `sudo apt-get install python3-launchpadlib`

`sudo apt-get install python3.8-dev`

### R install fail
Errors aren't automatically passed back from script so will need to check install output. Possibly will require   
`sudo apt-get install libxml2-dev`

### Pip slow install

e.g.

> pip is looking at multiple versions of pytz to determine which version is compatible with other
> requirements. This could take a while.

https://stackoverflow.com/questions/65122957/resolving-new-pip-backtracking-runtime-issue
`pip install -r requirements.txt --use-deprecated=legacy-resolver`



### Windows

Getting the demo server running on windows is particularly tricky and not recommended. A better approach would likely to use windows subsytem for linux instead.

If still determined, see links below for a few issues that may be encountered and possible workarounds

**Cannot Run R Installation**
Make sure you have added R to the environment path (as per installation documentation), and are running powershell (or the R program) as an administrator. You may also need to deactivate any active python environment.

if you have added R to path environment variable and try to call directly you may have to resolve conflict with in-built powershell `r` command (see https://stackoverflow.com/questions/50190995/trying-to-add-r-exe-to-the-path), or just call via `R.exe` or `Rscript`

**Filenames too long**
Whilst checking out the data repo you may find that filepaths are too long dependent on your base directory. For modern versions of windows this filepath length limitation can be removed and git configured to accept longer paths

https://confluence.atlassian.com/bamkb/git-checkouts-fail-on-windows-with-filename-too-long-error-unable-to-create-file-errors-867363792.html

**Mysql failed install**
https://stackoverflow.com/questions/51294268/pip-install-mysqlclient-returns-fatal-error-c1083-cannot-open-file-mysql-h

https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017


## Useful Links

- Climsoft API (whose methods these are loosely based on and may in the future be integrated with)   
https://github.com/openclimateinitiative/climsoft-api

- PyOpenCDMS python packages (used for linking to data)
https://github.com/opencdms/pyopencdms

- OpenCDMS test data repo (adapted to provide local testing capability)
https://github.com/opencdms/opencdms-test-data

- SQLAlchemy ORM (used for interrogating data)   
https://www.sqlalchemy.org/

- Pydantic (definining data models)
https://pydantic-docs.helpmanual.io/