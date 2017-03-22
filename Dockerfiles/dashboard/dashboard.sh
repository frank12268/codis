#!/bin/bash

set -e
python /gopath/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard_env_check.py
envtpl -o /opt/codis/dashboard-config.toml --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/dashboard/dashboard-config.toml.tpl
/gopath/src/github.com/CodisLabs/codis/bin/codis-dashboard -c /opt/codis/dashboard-config.toml --host-admin=$CODIS_DASHBOARD_HOST_HOST:$CODIS_DASHBOARD_HOST_PORT $CODIS_DASHBOARD_ARGS
