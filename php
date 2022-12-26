#!/usr/bin/env bash

source wrapper

function main() {
    if [[ -z $PHP_SERVICE ]]; then
        echo "Could not find PHP service."

        exit 1
    fi

    exec_service \
        -u="$(id -u):$(id -g)" \
        $PHP_SERVICE \
        php \
        "$@"
}

wrapper main "$@"
