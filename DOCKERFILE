# Base image is Debian 11 (bullseye) with python installed
FROM python:3.10-bullseye

# Install core dependencies for adding R and python dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common build-essential libpq-dev libnetcdf-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install R v4
# https://cran.r-project.org/bin/linux/debian/
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
RUN add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian bullseye-cran40/'
RUN apt update
RUN apt-get install -y --no-install-recommends r-base r-base-dev

# Setup virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /code

# Install app dependencies and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --default-timeout=100 --upgrade -r /code/requirements.txt

## Install R dependencies
COPY ./install_packages.R /code/install_packages.R
RUN Rscript /code/install_packages.R

# Copy RInstat code
COPY ./rinstat /code/rinstat

# Copy Test code
COPY ./test /code/test

# Copy app code
COPY ./app /code/app

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# TODOS
# Reduce overall size (https://www.peterspython.com/en/blog/reducing-the-size-of-a-python-application-docker-image-using-python-wheels)
# Confirm if build-essentials, libpq-dev and gcc required