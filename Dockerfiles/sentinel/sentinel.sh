#!/bin/bash

set -e
python /gopath/src/github.com/CodisLabs/codis/Dockerfiles/sentinel/sentinel_env_check.py
envtpl -o /opt/codis/sentinel.conf --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/sentinel/sentinel.conf.tpl
/gopath/src/github.com/CodisLabs/codis/bin/codis-server /opt/codis/sentinel.conf --sentinel --port $CODIS_SENTINEL_PORT $CODIS_SENTINEL_ARGS
