#!/usr/bin/env bash

if [[ -z $COMPOSE_FILE ]]; then
    /usr/bin/php "$@"
    exit $!
fi

if [[ -z $PHP_SERVICE ]]; then
    php_service='php'
else
    php_service=$PHP_SERVICE
fi

source wrapper

function main() {
    exec_service \
        "$php_service" \
        php \
        "$@"
}

function trap_hooks() {
    script=$(cat "$(which "${*}")")

    exec_service "$php_service" sh -c "$script"

    # time run_service \
    #     -v "$(which "${*}")":/hook.sh \
    #     "$php_service" \
    #     /hook.sh &> null
}

wrapper main "$@"
