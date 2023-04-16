# Web Interface of [`AstroPlasma`](https://github.com/dutta-alankar/AstroPlasma)

<div align="center">

<p>
<img src="https://img.shields.io/github/repo-size/tbhaxor/CloudyPlasmaServer?style=for-the-badge"/>
<img src="https://img.shields.io/github/directory-file-count/tbhaxor/CloudyPlasmaServer?style=for-the-badge&logo=files&logoColor=white"/>
<img src="https://img.shields.io/tokei/lines/github.com/tbhaxor/CloudyPlasmaServer?style=for-the-badge"/>
<img src="https://img.shields.io/github/last-commit/tbhaxor/CloudyPlasmaServer/main?style=for-the-badge"/>
<br>
<img src="https://results.pre-commit.ci/badge/github/tbhaxor/CloudyPlasmaServer/main.svg?style=for-the-badge" />
<img src="https://github.com/tbhaxor/CloudyPlasmaServer/actions/workflows/ci.yml/badge.svg?branch=main&style=for-the-badge" />
</p>

</div>

This is a web interface for the [AstroPlasma](https://github.com/dutta-alankar/AstroPlasma) repository which allows you to interpolate the plasma properties from the pre-computed dataset from the cloudy.

## Features

- [x] Compute Ionization Fraction of the Specific Element and Ion
- [x] Plot Ion fraction vs temperature graph for both CIE and PIE modes
- [x] Plot emission spectrum of the elements
- [x] Interactive graphs
- [x] Simple file server to download the batch file on demand (used internally in upstream AstroPlasma repository)

## Setup

1. Clone the repository

   ```sh
   https://github.com/tbhaxor/CloudyPlasmaServer.git
   ```

2. Install the packages

   ```sh
   poetry install
   ```

   > **Note** This command will automatically set-up virtual environment for you.

3. Provide environment file

   ```sh
   cat <<EOF > .env
   IONIZATION_DATASET_DIR='/path/to/directory/containing/ionization-batches'
   EMISSION_DATASET_DIR='/path/to/directory/containing/emission-batches'
   PY_ENV=dev
   EOF
   ```

   > **Note** Omit `PY_ENV=dev` if you want to deploy it on the production

4. Migrate the database

   ```sh
   poetry run python manage.py migrate
   ```

## Getting started

Once you have performed the steps from the **Setup**, you are good to go

```sh
poetry run python manage.py runserver
```

This will open the `8000` port by default, but you can change it using the following command

```sh
poetry run python manage.py runserver 127.0.0.1:<PORT>
```

Replace the placeholder `<PORT>` with the port number of your choice.

### Using Docker Containers

Get rid of all the hassle of [setup](#setup) and [getting started](#getting-started). You can use the following

**Requirements** Docker runtime and docker compose installed on your system

1.  Generate docker compose file from the template file

    ```sh
    bash deployment/scripts/gen-docker-compose.bash -i /path/to/ionization/dataset -e /path/to/emission/dataset
    ```

2.  Provide the **`CSRF_TRUSTED_ORIGINS`** configuration the environment of `web_app` service.

    Let's suppose I am hosting my webserver on the http://example.com, so it should be

    ```diff
    DB_URI: postgres://astrodata:astrodata@db/astrodata
    + CSRF_TRUSTED_ORIGINS: http://example.com
    ```

    > **Note** You can provide multiple origins separated by comma.

3.  Run the workload

    ```sh
    docker-compose up --pull always
    ```

    > **Note** You can access the server at port 8000.
