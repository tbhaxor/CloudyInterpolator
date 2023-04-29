#!/bin/bash

set -e

git_base_dir=$(git rev-parse --show-toplevel)
ionization_dir=""
emission_dir=""
source_config="$git_base_dir/docker-compose.remote.yml"
dest_config="$git_base_dir/docker-compose.yml"
csrf_trusted_origins=""

while [[ $# -gt 0 ]]; do
    case "$1" in
    -i)
        shift
        ionization_dir="${1%/}"
        ;;
    -e)
        shift
        emission_dir="${1%/}"
        ;;
    -s)
        shift
        source_config="$1"
        if [[ ! -f "$source_config" ]]; then
            echo "[x] Source config file does not exist" >&2
        fi
        ;;
    -c)
        shift
        csrf_trusted_origins="$1"
        ;;
    -d)
        shift
        dest_config="$1"
        ;;
    *)
        echo "usage: $0 -i DIR -e DIR -c CSRF_TRUSTED_ORIGINS [-s FILE] [-d FILE]"
        echo "Arguments"
        echo -e "\t-i DIR\n\t\tIonization dataset directory"
        echo -e "\t-e DIR\n\t\tEmission dataset directory"
        echo -e "\t-c FILE\n\t\tComma seprated list of origins for CSRF validation"
        echo -e "\t-s FILE\n\t\tSource docker-compose file (default: $source_config)"
        echo -e "\t-d FILE\n\t\tDestination docker-compose file (default: $dest_config)"
        exit 1
        ;;
    esac
    shift
done

set -x

if [[ -z "$csrf_trusted_origins" ]]; then
    echo "[x] CSRF trusted origins are required" >&2
    exit 1
fi

if [[ -z "$emission_dir" ]]; then
    echo "[x] Emission dataset directory required" >&2
    exit 1
elif [[ ! -d "$emission_dir" ]]; then
    echo "[x] Invalid emission dataset directory" >&2
    exit 1
fi

if [[ -z "$ionization_dir" ]]; then
    echo "[x] Ionization dataset directory required" >&2
    exit 1
elif [[ ! -d "$ionization_dir" ]]; then
    echo "[x] Invalid ionization dataset directory" >&2
    exit 1
fi

cp "$source_config" "$dest_config"

sed_args=(-i)
if [[ $(uname) == "Darwin" ]]; then
    sed_args+=('')
fi

sed "${sed_args[@]}" "s|SOURCE_IONIZATION_DIR_PLACEHOLDER|$ionization_dir|g" "$dest_config"
sed "${sed_args[@]}" "s|SOURCE_EMISSION_DIR_PLACEHOLDER|$emission_dir|g" "$dest_config"
sed "${sed_args[@]}" "s|CSRF_TRUSTED_ORIGINS_PLACEHOLDER|$csrf_trusted_origins|g" "$dest_config"
