# Cloudy Batch Downloader

![GitHub repo size](https://img.shields.io/github/repo-size/tbhaxor/CloudyPlasmaServer) |
![GitHub repo file count](https://img.shields.io/github/directory-file-count/tbhaxor/CloudyPlasmaServer)

<p align="center">

<img src="https://results.pre-commit.ci/badge/github/tbhaxor/CloudyPlasmaServer/main.svg" /> | <img src="https://github.com/tbhaxor/CloudyPlasmaServer/actions/workflows/ci.yml/badge.svg?branch=main" />

</p>

This repository is used to download the batch files for astro plasma datasets: Emission spectrum and Ionization.

## Screenshots

### Home Page

![](https://i.imgur.com/cjDgnfe.png)

### Plasma Ionization Interpolation

![](https://i.imgur.com/Q3TcxPZ.png)

### Plasma Emission Spectrum

![](https://i.imgur.com/tFIX3Y5.png)

## Setup

1. Clone the repository

    ```sh
    git clone git@github.com:tbhaxor/CloudyPlasmaServer.git
    ```

2. Create and source a virtual environment (recommonded, but optional)

    ```sh
    virtualenv .venv
    source .venv/bin/activate
    ```

3. Upgrade pip and install dependencies

    ```sh
    pip install -U pip
    pip install -r requirements.txt
    ```

    > **Note** If you are maintaining or into development of this repository, please consider using [poetry](https://python-poetry.org/).

4. Provide environment file

    ```sh
    cat <<EOF > .env
    IONIZATION_DATASET_DIR='/path/to/directory/containing/ionization-batches'
    EMISSION_DATASET_DIR='/path/to/directory/containing/emission-batches'
    EOF
    ```


5. Migrate the database

    ```sh
    python manage.py migrate
    ```

## Getting started

Once you have performed the steps from the **Setup**, you are good to go

```sh
python manage.py runserver
```

This will open the `8000` port by default, but you can change it using the following command

```sh
python manage.py runserver 127.0.0.1:<PORT>
```

Replace the placeholder `<PORT>` with the port number of your choice.


### Using Docker Container

Get rid of all the hassle of [setup](#setup) and [getting started](#getting-started). You can use the following

**Requirements** Docker runtime installed on your system

1. Pull the image
    ```sh
    docker pull ghcr.io/tbhaxor/astro-data:latest
    ```
2. Run the docker container with appropriate container. This will iniitally create a container and start it
    ```sh
    docker run -d -p 5000:5000 \
    -e EMISSION_DATASET_DIR=/data/emission-data -e IONIZATION_DATASET_DIR=/data/ionization-data \
    -v /path/of/emission/batches:/data/emission-data:ro -v /path/of/ionization/batches:/data/ionization-data:ro \
    --name astro-data ghcr.io/tbhaxor/astro-data:latest
    ```

    > **Note** Replace the /path/* placeholder with the actual path of emission and ionization data on your host system.

    This will start the server on the http://localhost:5000, you can open this url in the browser to interact with the server.

3. Stop and restart the server
    ```sh
    # stop the container
    docker stop astro-data

    # restart the container
    docker start astro-data
    ```

> **Note** On updates, all you need to do is follow [docker setup](#using-docker-container) from step 1. Make sure you delete the container (`docker rm -f astro-data`) before moving forward.
