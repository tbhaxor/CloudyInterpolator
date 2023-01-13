# Cloudy Batch Downloader

This repository is used to download the batch files for astro plasma datasets: Emission spectrum and Ionization.

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

![](https://i.imgur.com/wgYz36E.png)