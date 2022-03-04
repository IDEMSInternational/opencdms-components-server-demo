# OpenCDMS Component Server Demo

## Pre-Requisites

The documentation requires python to be installed:  
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

## Running in Docker

### Build

docker build -f DOCKERFILE --tag idems/opencdms-components-api:1.0.0 .

### Docker Run (interactive)

docker run -i --rm -p 8000:8000 idems/opencdms-components-api:1.0.0
