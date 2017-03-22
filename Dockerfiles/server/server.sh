#!/bin/bash

set -e
python /gopath/src/github.com/CodisLabs/codis/Dockerfiles/server/server_env_check.py
envtpl -o /opt/codis/redis.conf --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/server/redis.conf.tpl
if [[ $ALLOW_METRICS_COLLECTION == "1" ]]; then
	envtpl -o /etc/collectd/collectd.conf --keep-template /gopath/src/github.com/CodisLabs/codis/Dockerfiles/collectd/redis_info_collectd.conf.tpl
	service collectd start
fi
/gopath/src/github.com/CodisLabs/codis/bin/codis-server /opt/codis/redis.conf --port $CODIS_SERVER_PORT --maxmemory $CODIS_SERVER_MAX_MEMORY $CODIS_SERVER_ARGS
